import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from fastapi import FastAPI, BackgroundTasks, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from webapp.config import Config

app = FastAPI(title="Semantic EML Annotator Backend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
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

MOCK_ATTRIBUTE_RECOMMENDATIONS = [
    {
        "id": f"attribute-0",
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
        ]
    }
]

MOCK_GEOGRAPHICCOVERAGE_RECOMMENDATIONS = [
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
]


# --- Mock Switch ---
USE_MOCK_RECOMMENDATIONS = True  # Set to False to use real recommendation logic when implemented


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
    Stub recommender for attribute elements.
    """
    if USE_MOCK_RECOMMENDATIONS:
        return MOCK_ATTRIBUTE_RECOMMENDATIONS
    # Real logic would go here
    return []

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


def parse_eml_elements(payload):
    """
    Parses the input payload and groups EML elements by type, applying reformatting for each group.
    Accepts the raw frontend payload (capitalized keys, e.g. 'ATTRIBUTE', 'GEOGRAPHICCOVERAGE').
    Returns a dict of group key -> list of reformatted elements.
    """
    grouped = {}
    if "ATTRIBUTE" in payload:
        items = payload["ATTRIBUTE"] if isinstance(payload["ATTRIBUTE"], list) else [payload["ATTRIBUTE"]]
        grouped["ATTRIBUTE"] = reformat_attribute_elements(items)
    if "GEOGRAPHICCOVERAGE" in payload:
        items = payload["GEOGRAPHICCOVERAGE"] if isinstance(payload["GEOGRAPHICCOVERAGE"], list) else [payload["GEOGRAPHICCOVERAGE"]]
        grouped["GEOGRAPHICCOVERAGE"] = reformat_geographic_coverage_elements(items)
    # Add more types as needed
    return grouped


@app.post("/api/recommendations")
def recommend_annotations(payload: dict = Body(...)):
    """
    Accepts a JSON payload of EML metadata elements grouped by type (e.g. ATTRIBUTE, GEOGRAPHICCOVERAGE),
    parses the types, fans out to respective recommendation engines, and combines the results.
    Implements a gateway aggregation pattern for annotation recommendations.
    If no recognized types are present, returns the original mock response for backward compatibility.
    """
    import json
    print("Received payload for recommendations: " + json.dumps(payload, indent=2, default=str))

    grouped = parse_eml_elements(payload)
    results = []
    if "ATTRIBUTE" in grouped:
        results.extend(recommend_for_attribute(grouped["ATTRIBUTE"]))
    if "GEOGRAPHICCOVERAGE" in grouped:
        results.extend(recommend_for_geographic_coverage(grouped["GEOGRAPHICCOVERAGE"]))
    # Add more types as needed

    if USE_MOCK_RECOMMENDATIONS:
        return ORIGINAL_MOCK_RESPONSE  # Just mocking for now
    if results:
        return results
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
    "parse_eml_elements",
    "app",
]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
