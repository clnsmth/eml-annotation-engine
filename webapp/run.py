import smtplib
import json
import re
from collections import defaultdict
from itertools import groupby
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

import requests
from fastapi import FastAPI, BackgroundTasks, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from webapp.config import Config

app = FastAPI(title="Semantic EML Annotator Backend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Constants ---

ORIGINAL_MOCK_RESPONSE = [
    {
        "id": "24632bb8dbdace8be4693baf5c9e4b97",
        "recommendations": [
            {
                "label": "Survey Dataset",
                "uri": "http://purl.obolibrary.org/obo/IAO_0000100",
                "ontology": "IAO",
                "confidence": 0.90,
                "description": "A data set that is a collection of data about a survey.",
                "propertyLabel": "contains",
                "propertyUri": "http://www.w3.org/ns/oa#hasBody",
            }
        ],
    },
    {
        "id": "cfe0601b-e76b-4f34-8a5a-655db3b0491c",
        "recommendations": [
            {
                "label": "Identifier",
                "uri": "http://purl.obolibrary.org/obo/IAO_0000578",
                "ontology": "IAO",
                "confidence": 0.95,
                "description": "An information content entity that identifies something.",
                "propertyLabel": "contains measurements of type",
                "propertyUri": "http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#containsMeasurementsOfType",
                "attributeName": "SurveyID",
                "objectName": "SurveyResults.csv",
            }
        ],
    },
    {
        "id": "d49be2c0-7b9e-41f4-ae07-387d3e1f14c8",
        "recommendations": [
            {
                "label": "Latitude",
                "uri": "http://purl.obolibrary.org/obo/GEO_00000016",
                "ontology": "GEO",
                "confidence": 0.99,
                "description": "The angular distance of a place north or south of the earth's equator.",
                "propertyLabel": "contains measurements of type",
                "propertyUri": "http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#containsMeasurementsOfType",
                "attributeName": "Latitude",
                "objectName": "SurveyResults.csv",
            }
        ],
    },
    {
        "id": "0673eb41-1b47-4d32-9d87-bf10e17c69b6",
        "recommendations": [
            {
                "label": "Air Temperature",
                "uri": "http://purl.obolibrary.org/obo/ENVO_00002006",
                "ontology": "ENVO",
                "confidence": 0.90,
                "description": "The temperature of the air.",
                "propertyLabel": "contains measurements of type",
                "propertyUri": "http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#containsMeasurementsOfType",
                "attributeName": "AirTemperature_F",
                "objectName": "SurveyResults.csv",
            },
            {
                "label": "Temperature",
                "uri": "http://purl.obolibrary.org/obo/PATO_0000146",
                "ontology": "PATO",
                "confidence": 0.85,
                "description": "A physical quality of the thermal energy of a system.",
                "propertyLabel": "contains measurements of type",
                "propertyUri": "http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#containsMeasurementsOfType",
                "attributeName": "AirTemperature_F",
                "objectName": "SurveyResults.csv",
            },
        ],
    },
    {
        "id": "dca8c4a4-472b-4998-bf35-82b9e4fb8f22",
        "recommendations": [
            {
                "label": "Water Temperature",
                "uri": "http://purl.obolibrary.org/obo/ENVO_00002010",
                "ontology": "ENVO",
                "confidence": 0.95,
                "description": "The temperature of water.",
                "propertyLabel": "contains measurements of type",
                "propertyUri": "http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#containsMeasurementsOfType",
                "attributeName": "WaterTemperature_F",
                "objectName": "SurveyResults.csv",
            }
        ],
    },
    {
        "id": "66c5e93d-7a8b-4dbf-989f-9294db3ec7b9",
        "recommendations": [
            {
                "label": "Lake",
                "uri": "http://purl.obolibrary.org/obo/ENVO_00000020",
                "ontology": "ENVO",
                "confidence": 0.92,
                "description": "A large body of water surrounded by land.",
                "propertyLabel": "contains measurements of type",
                "propertyUri": "http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#containsMeasurementsOfType",
                "attributeName": "Lake",
                "objectName": "SurveyResults.csv",
            }
        ],
    },
    {
        "id": "24b4badd-56b7-4dbf-8848-f6531f20c024",
        "recommendations": [
            {
                "label": "Taxon",
                "uri": "http://rs.tdwg.org/dwc/terms/Taxon",
                "ontology": "DWC",
                "confidence": 0.88,
                "description": "A group of one or more populations of an organism.",
                "propertyLabel": "contains measurements of type",
                "propertyUri": "http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#containsMeasurementsOfType",
                "attributeName": "SpeciesCode",
                "objectName": "SurveyResults.csv",
            },
            {
                "label": "Scientific Name",
                "uri": "http://rs.tdwg.org/dwc/terms/scientificName",
                "ontology": "DWC",
                "confidence": 0.80,
                "description": "The full scientific name.",
                "propertyLabel": "contains measurements of type",
                "propertyUri": "http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#containsMeasurementsOfType",
                "attributeName": "SpeciesCode",
                "objectName": "SurveyResults.csv",
            },
        ],
    },
    {
        "id": "3220828d-a9a3-4c98-89a6-36f4a740a57e",
        "recommendations": [
            {
                "label": "Surface Layer",
                "uri": "http://purl.obolibrary.org/obo/ENVO_00002005",
                "ontology": "ENVO",
                "confidence": 0.70,
                "description": "The layer of a material that is in contact with the surrounding medium.",
                "propertyLabel": "contains measurements of type",
                "propertyUri": "http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#containsMeasurementsOfType",
                "attributeName": "EggMassSubstrate",
                "objectName": "EggMasses.csv",
            }
        ],
    },
    {
        "id": "geo-1",
        "recommendations": [
            {
                "label": "Freshwater Lake Ecosystem",
                "uri": "http://purl.obolibrary.org/obo/ENVO_01000021",
                "ontology": "ENVO",
                "confidence": 0.75,
                "description": "An aquatic ecosystem that is part of a lake.",
                "propertyLabel": "contains",
                "propertyUri": "http://www.w3.org/ns/oa#hasBody",
            },
            {
                "label": "Temperate Climate",
                "uri": "http://purl.obolibrary.org/obo/ENVO_01000000",
                "ontology": "ENVO",
                "confidence": 0.80,
                "description": "A climate with moderate conditions",
                "propertyLabel": "contains",
                "propertyUri": "http://www.w3.org/ns/oa#hasBody",
            },
        ],
    },
    {
        "id": "befe3d845aea4510048251bd0079e3de",
        "recommendations": [
            {
                "label": "Technical Report",
                "uri": "http://purl.obolibrary.org/obo/IAO_0000088",
                "ontology": "IAO",
                "confidence": 0.85,
                "description": "A report concerning the results of a scientific investigation or technical development.",
                "propertyLabel": "contains",
                "propertyUri": "http://www.w3.org/ns/oa#hasBody",
            }
        ],
    },
]

# Changed to a Dictionary keyed by ObjectName
MOCK_ATTRIBUTE_RECOMMENDATIONS_BY_FILE = {
    "SurveyResults.csv": [
        {
            "column_name": "SurveyID",
            "concept_name": "Identifier",
            "concept_definition": "An information content entity that identifies something.",
            "concept_id": "http://purl.obolibrary.org/obo/IAO_0000578",
            "confidence": 0.95
        },
        {
            "column_name": "Latitude",
            "concept_name": "Latitude",
            "concept_definition": "The angular distance of a place north or south of the earth's equator.",
            "concept_id": "http://purl.obolibrary.org/obo/GEO_00000016",
            "confidence": 0.99
        },
        {
            "column_name": "AirTemperature_F",
            "concept_name": "Air Temperature",
            "concept_definition": "The temperature of the air.",
            "concept_id": "http://purl.obolibrary.org/obo/ENVO_00002006",
            "confidence": 0.9
        },
        {
            "column_name": "AirTemperature_F",
            "concept_name": "Temperature",
            "concept_definition": "A physical quality of the thermal energy of a system.",
            "concept_id": "http://purl.obolibrary.org/obo/PATO_0000146",
            "confidence": 0.85
        },
        {
            "column_name": "WaterTemperature_F",
            "concept_name": "Water Temperature",
            "concept_definition": "The temperature of water.",
            "concept_id": "http://purl.obolibrary.org/obo/ENVO_00002010",
            "confidence": 0.95
        },
        {
            "column_name": "Lake",
            "concept_name": "Lake",
            "concept_definition": "A large body of water surrounded by land.",
            "concept_id": "http://purl.obolibrary.org/obo/ENVO_00000020",
            "confidence": 0.92
        },
        {
            "column_name": "SpeciesCode",
            "concept_name": "Taxon",
            "concept_definition": "A group of one or more populations of an organism.",
            "concept_id": "http://rs.tdwg.org/dwc/terms/Taxon",
            "confidence": 0.88
        },
        {
            "column_name": "SpeciesCode",
            "concept_name": "Scientific Name",
            "concept_definition": "The full scientific name.",
            "concept_id": "http://rs.tdwg.org/dwc/terms/scientificName",
            "confidence": 0.8
        },
    ],
    "EggMasses.csv": [
        {
            "column_name": "EggMassSubstrate",
            "concept_name": "Surface Layer",
            "concept_definition": "The layer of a material that is in contact with the surrounding medium.",
            "concept_id": "http://purl.obolibrary.org/obo/ENVO_00002005",
            "confidence": 0.7
        }
    ]
}

MOCK_GEOGRAPHICCOVERAGE_RECOMMENDATIONS = [
    {
        "id": "geo-1",
        "recommendations": [
            {
                "label": "Freshwater Lake Ecosystem",
                "uri": "http://purl.obolibrary.org/obo/ENVO_01000021",
                "ontology": "ENVO",
                "confidence": 0.75,
                "description": "An aquatic ecosystem that is part of a lake.",
                "propertyLabel": "contains",
                "propertyUri": "http://www.w3.org/ns/oa#hasBody",
            },
            {
                "label": "Temperate Climate",
                "uri": "http://purl.obolibrary.org/obo/ENVO_01000000",
                "ontology": "ENVO",
                "confidence": 0.80,
                "description": "A climate with moderate conditions",
                "propertyLabel": "contains",
                "propertyUri": "http://www.w3.org/ns/oa#hasBody",
            },
        ],
    }
]

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


# --- Helper Logic for Merging ---

def extract_ontology(uri):
    """Parses the ontology code (ENVO, PATO, IAO) from a URI."""
    if not uri: return "UNKNOWN"
    match = re.search(r'/obo/([A-Z]+)_', uri)
    if match: return match.group(1)
    if "dwc/terms" in uri: return "DWC"
    return "UNKNOWN"


def merge_recommender_results(source_items, recommender_items, eml_type="ATTRIBUTE"):
    """
    Joins recommender response back to source items using 'column_name'.
    """
    config = MERGE_CONFIG.get(eml_type)
    if not config: return []

    # Index recommender items
    rec_lookup = defaultdict(list)
    for rec in recommender_items:
        key = rec.get('column_name')
        if key:
            rec_lookup[key].append(rec)

    merged_results = []

    # Iterate source items to preserve IDs
    for item in source_items:
        # Match using the key defined in reformat_attribute_elements (column_name)
        match_val = item.get("name")  # "name" in source == "column_name" in recommendations

        if match_val in rec_lookup:
            entry = {
                "id": item['id'],
                "recommendations": []
            }

            for rec_data in rec_lookup[match_val]:
                annot = {
                    "label": rec_data['concept_name'],
                    "uri": rec_data['concept_id'],
                    "ontology": extract_ontology(rec_data['concept_id']),
                    "confidence": rec_data['confidence'],
                    "description": rec_data['concept_definition'],
                    "propertyLabel": config['property_label'],
                    "propertyUri": config['property_uri'],
                    "attributeName": item.get('name'),  # "name" in source == "column_name" in recommendations
                    "objectName": item.get('objectName')
                }
                entry["recommendations"].append(annot)

            merged_results.append(entry)

    return merged_results


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
            recommender_response = MOCK_ATTRIBUTE_RECOMMENDATIONS_BY_FILE.get(object_name, [])

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

    # To visualize post by front end
    # import json
    # print("Received payload for recommendations: " + json.dumps(payload, indent=2, default=str))

    results = []
    if "ATTRIBUTE" in payload:
        recommended_attributes = recommend_for_attribute(payload["ATTRIBUTE"])
        results.append(recommended_attributes)
    if "GEOGRAPHICCOVERAGE" in payload:
        recommended_geographic_coverage = recommend_for_geographic_coverage(payload["GEOGRAPHICCOVERAGE"])
        results.append(recommended_geographic_coverage)
    # Add more types as needed

    if results:
        # Results is a list of lists (one per type). Flatten if your frontend expects a flat list,
        # or keep as is. Based on ORIGINAL_MOCK_RESPONSE, frontend expects a flat list of objects.
        flat_results = [item for sublist in results for item in sublist]
        return flat_results
    else:
        return []


def reformat_attribute_elements(attributes):
    """
    Transform attribute elements to the format expected by the attribute recommender.
    Converts each input dict to the output format:
    {
        "entity_name": <objectName>,
        "entity_description": <entityDescription>,
        "object_name": <objectName>,
        "column_name": <name>,
        "column_description": <description>
    }
    """
    reformatted = []
    for attr in attributes:
        reformatted.append({
            "entity_name": attr.get("objectName"),
            "entity_description": attr.get("entityDescription"),
            "object_name": attr.get("objectName"),
            "column_name": attr.get("name"),
            "column_description": attr.get("description"),
        })
    return reformatted


def reformat_geographic_coverage_elements(geos):
    """
    Stub: Transform geographic coverage elements to the format expected by the geographic coverage recommender.
    For now, returns input unchanged.
    """
    return geos


__all__ = [
    "recommend_for_attribute",
    "recommend_for_geographic_coverage",
    "reformat_attribute_elements",
    "reformat_geographic_coverage_elements",
    "app",
]

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)