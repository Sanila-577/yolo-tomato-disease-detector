from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    detected_disease: Optional[str] = None
    is_first_message: Optional[bool] = False
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    answer: str
    detected_disease: Optional[str] = None
    session_id: str = "default"
    