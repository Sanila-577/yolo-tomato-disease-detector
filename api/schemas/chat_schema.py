from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    detected_disease: Optional[str] = None
    is_first_message: Optional[bool] = False

class ChatResponse(BaseModel):
    answer: str
    