import smtplib
import json
from itertools import groupby
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

import requests
from fastapi import FastAPI, BackgroundTasks, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr

from webapp.config import Config
from webapp.mock_objects import MOCK_RAW_ATTRIBUTE_RECOMMENDATIONS_BY_FILE, MOCK_GEOGRAPHICCOVERAGE_RECOMMENDATIONS
from webapp.utils import merge_recommender_results

app = FastAPI(title="Semantic EML Annotator Backend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Mock Switch ---
USE_MOCK_RECOMMENDATIONS = True  # Set to False to use real recommendation logic when implemented

# --- Helper Configuration ---
MERGE_CONFIG = {
    "ATTRIBUTE": {
        "property_label": "contains measurements of type",
        "property_uri": "http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#containsMeasurementsOfType",
        "join_key": "column_name"  # Field in Source to match Recommender's 'column_name'
    }
}


# --- Data Models ---


class TermDetails(BaseModel):
    label: str
    description: str
    evidence_source: Optional[str] = None


class SubmitterInfo(BaseModel):
    email: EmailStr
    orcid_id: Optional[str] = None
    attribution_consent: bool


class ProposalRequest(BaseModel):
    target_vocabulary: str
    term_details: TermDetails
    submitter_info: SubmitterInfo


class EMLMetadata(BaseModel):
    # Placeholder for EML metadata elements. Add fields as needed.
    elements: dict = {}


# --- Email Logic ---


def send_email_notification(proposal: ProposalRequest):
    """
    Sends an email with the proposal details to the configured recipient.
    Credentials and recipient are set via config.py only.
    """
    recipient = Config.VOCABULARY_PROPOSAL_RECIPIENT
    smtp_server = Config.SMTP_SERVER
    smtp_port = Config.SMTP_PORT
    smtp_user = Config.SMTP_USER
    smtp_password = Config.SMTP_PASSWORD

    if not recipient:
        print(
            "Warning: VOCABULARY_PROPOSAL_RECIPIENT not set. Skipping email dispatch."
        )
        print(f"Payload received: {proposal.model_dump_json(indent=2)}")
        return

    if not smtp_user or not smtp_password:
        print("Warning: SMTP credentials not set. Cannot send email.")
        return

    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = recipient
    msg["Subject"] = f"New Ontology Term Proposal: {proposal.term_details.label}"

    body = f"""
    New Term Proposal Received via Semantic EML Annotator

    --- Context ---
    Target Vocabulary/Category: {proposal.target_vocabulary}

    --- Term Details ---
    Label: {proposal.term_details.label}
    Description: 
    {proposal.term_details.description}

    Evidence Source: {proposal.term_details.evidence_source or 'None provided'}

    --- Submitter Information ---
    Email: {proposal.submitter_info.email}
    ORCID: {proposal.submitter_info.orcid_id or 'None provided'}
    Attribution Consent: {'Yes' if proposal.submitter_info.attribution_consent else 'No'}
    """

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_user, recipient, text)
        server.quit()
        print(f"Proposal email successfully sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email: {e}")


# --- Recommender Functions ---

def recommend_for_attribute(attributes):
    """
    Groups attributes by objectName, sends to API (or gets mock per file), and merges results.
    """

    BASE_URL = 'http://98.88.80.17:5000'
    ANNOTATE_ENDPOINT = '/api/annotate'
    API_URL = f"{BASE_URL}{ANNOTATE_ENDPOINT}"

    # Sort for groupby
    attributes.sort(key=lambda x: x.get("objectName", "unknown"))

    final_output = []

    # Group by File (object_name)
    for object_name, group_iter in groupby(attributes, key=lambda x: x.get("objectName", "unknown")):
        file_attributes = list(group_iter)
        recommender_response = []

        if USE_MOCK_RECOMMENDATIONS:
            # LOOK UP MOCK DATA BY FILENAME
            # Default to empty list if filename not found in mock
            recommender_response = MOCK_RAW_ATTRIBUTE_RECOMMENDATIONS_BY_FILE.get(object_name, [])

            # Merge results for this file group using the retrieved mock data
            file_results = merge_recommender_results(file_attributes, recommender_response, "ATTRIBUTE")
            final_output.extend(file_results)

        else:
            # REAL API LOGIC
            # Prepare payload (exclude ID if API is strict, otherwise just pass file_attributes)
            api_payload = [{k: v for k, v in i.items() if k != 'id'} for i in file_attributes]

            try:
                # Send the POST request to the API.
                response = requests.post(API_URL, json=api_payload)
                response.raise_for_status()

                raw_response = response.json()

                # Normalize response (Dict[col, list] -> List[dict])
                if isinstance(raw_response, dict):
                    for col_name, recs in raw_response.items():
                        # Take top 5
                        for r in recs[:5]:
                            if 'column_name' not in r: r['column_name'] = col_name
                            recommender_response.append(r)
                elif isinstance(raw_response, list):
                    recommender_response = raw_response

                # Merge results for this file group
                file_results = merge_recommender_results(file_attributes, recommender_response, "ATTRIBUTE")
                final_output.extend(file_results)

            except requests.exceptions.RequestException as e:
                print(f"An error occurred for {object_name}: {e}")
                continue

    return final_output


def recommend_for_geographic_coverage(geos):
    """
    Stub recommender for geographic coverage elements.
    """
    if USE_MOCK_RECOMMENDATIONS:
        return MOCK_GEOGRAPHICCOVERAGE_RECOMMENDATIONS
    # Real logic would go here
    return []


# --- Endpoints ---


@app.get("/")
def read_root():
    return {"message": "Semantic EML Annotator Backend is running."}


@app.post("/api/proposals")
async def submit_proposal(proposal: ProposalRequest, background_tasks: BackgroundTasks):
    """
    Receives a new term proposal and queues an email notification.
    """
    try:
        # In a real application, you might also save this to a database here.
        background_tasks.add_task(send_email_notification, proposal)
        return {"status": "success", "message": "Proposal received and processing."}
    except Exception as e:
        print(f"Error processing proposal: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error processing proposal."
        )


@app.post("/api/recommendations")
def recommend_annotations(payload: dict = Body(...)):
    """
    Accepts a JSON payload of EML metadata elements grouped by type (e.g. ATTRIBUTE, GEOGRAPHICCOVERAGE),
    parses the types, fans out to respective recommendation engines, and combines the results.
    Implements a gateway aggregation pattern for annotation recommendations.
    If no recognized types are present, returns the original mock response for backward compatibility.
    """

    # print the incoming payload for debugging
    print("Received recommendation payload:", json.dumps(payload, indent=2))

    results = []
    if "ATTRIBUTE" in payload:
        recommended_attributes = recommend_for_attribute(payload["ATTRIBUTE"])
        results.append(recommended_attributes)
    if "GEOGRAPHICCOVERAGE" in payload:
        recommended_geographic_coverage = recommend_for_geographic_coverage(payload["GEOGRAPHICCOVERAGE"])
        results.append(recommended_geographic_coverage)
    # Add more types as needed

    if results:
        flat_results = [item for sublist in results for item in sublist]
        return JSONResponse(content=flat_results, status_code=200)
    else:
        return JSONResponse(content=[], status_code=200)


__all__ = [
    "recommend_for_attribute",
    "recommend_for_geographic_coverage",
    "app",
]

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)