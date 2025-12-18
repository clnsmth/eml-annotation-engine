from itertools import groupby
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import requests
import smtplib
from pydantic import BaseModel, EmailStr
from webapp.config import Config
from webapp.utils import merge_recommender_results

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
    elements: dict = {}

def send_email_notification(proposal: ProposalRequest):
    recipient = Config.VOCABULARY_PROPOSAL_RECIPIENT
    smtp_server = Config.SMTP_SERVER
    smtp_port = Config.SMTP_PORT
    smtp_user = Config.SMTP_USER
    smtp_password = Config.SMTP_PASSWORD
    if not recipient:
        print("Warning: VOCABULARY_PROPOSAL_RECIPIENT not set. Skipping email dispatch.")
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

def recommend_for_attribute(attributes):
    BASE_URL = 'http://98.88.80.17:5000'
    ANNOTATE_ENDPOINT = '/api/annotate'
    API_URL = f"{BASE_URL}{ANNOTATE_ENDPOINT}"
    attributes.sort(key=lambda x: x.get("objectName", "unknown"))
    final_output = []
    for object_name, group_iter in groupby(attributes, key=lambda x: x.get("objectName", "unknown")):
        file_attributes = list(group_iter)
        recommender_response = []
        if Config.USE_MOCK_RECOMMENDATIONS:
            from webapp.mock_objects import MOCK_RAW_ATTRIBUTE_RECOMMENDATIONS_BY_FILE
            recommender_response = MOCK_RAW_ATTRIBUTE_RECOMMENDATIONS_BY_FILE.get(object_name, [])
            file_results = merge_recommender_results(file_attributes, recommender_response, "ATTRIBUTE")
            final_output.extend(file_results)
        else:
            api_payload = [{k: v for k, v in i.items() if k != 'id'} for i in file_attributes]
            try:
                response = requests.post(API_URL, json=api_payload)
                response.raise_for_status()
                raw_response = response.json()
                if isinstance(raw_response, dict):
                    for col_name, recs in raw_response.items():
                        for r in recs[:5]:
                            if 'column_name' not in r: r['column_name'] = col_name
                            recommender_response.append(r)
                elif isinstance(raw_response, list):
                    recommender_response = raw_response
                file_results = merge_recommender_results(file_attributes, recommender_response, "ATTRIBUTE")
                final_output.extend(file_results)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred for {object_name}: {e}")
                continue
    return final_output

def recommend_for_geographic_coverage(geos):
    if Config.USE_MOCK_RECOMMENDATIONS:
        from webapp.mock_objects import MOCK_GEOGRAPHICCOVERAGE_RECOMMENDATIONS
        return MOCK_GEOGRAPHICCOVERAGE_RECOMMENDATIONS
    return []
