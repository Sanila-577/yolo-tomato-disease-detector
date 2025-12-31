from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    detected_disease: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str