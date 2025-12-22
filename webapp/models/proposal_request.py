from pydantic import BaseModel, EmailStr
from typing import Optional

class TermDetails(BaseModel):
    """
    Data model for ontology term details.
    """
    label: str
    description: str
    evidence_source: Optional[str] = None

class SubmitterInfo(BaseModel):
    """
    Data model for submitter information.
    """
    email: EmailStr
    orcid_id: Optional[str] = None
    attribution_consent: bool

class ProposalRequest(BaseModel):
    """
    Data model for a vocabulary proposal request.
    """
    target_vocabulary: str
    term_details: TermDetails
    submitter_info: SubmitterInfo
