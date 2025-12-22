from pydantic import BaseModel

class EMLMetadata(BaseModel):
    """
    Data model for EML metadata elements.
    """
    elements: dict = {}

