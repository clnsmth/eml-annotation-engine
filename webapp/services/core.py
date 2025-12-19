"""
Core business logic and data models for the Semantic EML Annotator Backend.
"""
from itertools import groupby
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List, Dict, Any
import smtplib
import requests
from pydantic import BaseModel, EmailStr
from webapp.config import Config
from webapp.utils.utils import merge_recommender_results
from webapp.models.mock_objects import (MOCK_RAW_ATTRIBUTE_RECOMMENDATIONS_BY_FILE,
                                        MOCK_GEOGRAPHICCOVERAGE_RECOMMENDATIONS)


class TermDetails(BaseModel):
    """
    Data model for ontology term details.

    :ivar label: The term label
    :ivar description: The term description
    :ivar evidence_source: Optional evidence source
    """

    label: str
    description: str
    evidence_source: Optional[str] = None


class SubmitterInfo(BaseModel):
    """
    Data model for submitter information.

    :ivar email: Submitter's email address
    :ivar orcid_id: Optional ORCID identifier
    :ivar attribution_consent: Whether submitter consents to attribution
    """

    email: EmailStr
    orcid_id: Optional[str] = None
    attribution_consent: bool


class ProposalRequest(BaseModel):
    """
    Data model for a vocabulary proposal request.

    :ivar target_vocabulary: Target vocabulary/category
    :ivar term_details: Details of the proposed term
    :ivar submitter_info: Information about the submitter
    """

    target_vocabulary: str
    term_details: TermDetails
    submitter_info: SubmitterInfo


class EMLMetadata(BaseModel):
    """
    Data model for EML metadata elements.

    :ivar elements: Dictionary of EML elements
    """

    elements: dict = {}


def send_email_notification(proposal: ProposalRequest) -> None:
    """
    Sends an email with the proposal details to the configured recipient.
    Credentials and recipient are set via config.py only.

    :param proposal: The proposal request payload
    :return: None
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


# pylint: disable=too-many-locals
def recommend_for_attribute(attributes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Groups attributes by objectName, sends to API (or gets mock per file), and merges results.

    :param attributes: List of attribute dictionaries
    :return: List of merged recommendation results for attributes
    """
    api_url = Config.API_URL
    attributes.sort(key=lambda x: x.get("objectName", "unknown"))
    final_output: List[Dict[str, Any]] = []
    # Group by File (object_name)
    for object_name, group_iter in groupby(
        attributes, key=lambda x: x.get("objectName", "unknown")
    ):
        file_attributes = list(group_iter)
        recommender_response: List[Dict[str, Any]] = []
        if Config.USE_MOCK_RECOMMENDATIONS:
            recommender_response = MOCK_RAW_ATTRIBUTE_RECOMMENDATIONS_BY_FILE.get(
                object_name, []
            )
            # Merge results for this file group using the retrieved mock data
            file_results = merge_recommender_results(
                file_attributes, recommender_response, "ATTRIBUTE"
            )
            final_output.extend(file_results)
        else:
            # REAL API LOGIC
            api_payload = [
                {k: v for k, v in i.items() if k != "id"} for i in file_attributes
            ]
            try:
                response = requests.post(api_url, json=api_payload, timeout=60)
                response.raise_for_status()
                raw_response = response.json()
                # Normalize response (Dict[col, list] -> List[dict])
                if isinstance(raw_response, dict):
                    for col_name, recs in raw_response.items():
                        for r in recs[:5]:
                            if "column_name" not in r:
                                r["column_name"] = col_name
                            recommender_response.append(r)
                elif isinstance(raw_response, list):
                    recommender_response = raw_response
                # Merge results for this file group
                file_results = merge_recommender_results(
                    file_attributes, recommender_response, "ATTRIBUTE"
                )
                final_output.extend(file_results)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred for {object_name}: {e}")
                continue
    return final_output


def recommend_for_geographic_coverage(
    geos: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Stub recommender for geographic coverage elements.

    :param geos: List of geographic coverage dictionaries
    :return: Mock recommendations if enabled, otherwise an empty list
    """
    #pylint: disable=unused-argument
    if Config.USE_MOCK_RECOMMENDATIONS:
        return MOCK_GEOGRAPHICCOVERAGE_RECOMMENDATIONS
    return []
