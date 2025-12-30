# models/privacy_report.py
from pydantic import BaseModel
from typing import Dict, List

class PrivacyReport(BaseModel):
    original_text: str
    masked_text: str
    detected_entities: Dict[str, List[str]]
    optimized_prompt: str
    status: str
