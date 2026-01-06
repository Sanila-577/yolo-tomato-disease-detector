from pydantic import BaseModel
from typing import List, Optional, Dict

class DetectionBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float
    label: str
    notes: Optional[List[str]] = []
    is_quarantine: Optional[bool] = False
    verification_needed: Optional[bool] = False

class VisionResponse(BaseModel):
    detected_disease: str
    detections: List[DetectionBox]
    output_image_path: str
    report: Optional[Dict] = None