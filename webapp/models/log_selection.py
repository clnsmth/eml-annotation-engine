from pydantic import BaseModel
from typing import List

class SelectionItem(BaseModel):
    label: str
    uri: str
    property_label: str
    property_uri: str
    confidence: float

class LogSelection(BaseModel):
    request_id: str
    event_id: str
    timestamp: str  # ISO 8601 string, could use datetime with custom parsing
    element_id: str
    element_name: str
    element_type: str
    selected: SelectionItem
    not_selected: List[SelectionItem]
