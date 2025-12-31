from fastapi import APIRouter, UploadFile, File
import uuid
from pathlib import Path

from vision.inference import run_inference
from vision.utils import draw_boxes
from api.schemas.vision_schema import VisionResponse

router = APIRouter(prefix="/detect", tags=["Detect"])

OUTPUT_DIR = Path("static/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@router.post("", response_model= VisionResponse)
async def detect_disease(file: UploadFile = File(...) ):
    image_bytes = await file.read()
    detections,image = run_inference(image_bytes)
    annotated_img = draw_boxes(image, detections)

    file_name = f"{uuid.uuid4()}.jpg"
    output_path = OUTPUT_DIR / file_name
    annotated_img.save(output_path)

    diseases = list({d["label"] for d in detections})

    return VisionResponse(
        detected_disease = diseases,
        boxes=detections,
        annotated_image = f"/static/outputs/{file_name}"
    )


