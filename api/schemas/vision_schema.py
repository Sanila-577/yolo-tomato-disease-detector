from pydantic import BaseModel
from typing import List

class DetectionBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float
    label: str

class VisionResponse(BaseModel):
    detected_disease: str
    detections: List[DetectionBox]
    output_image_path: str