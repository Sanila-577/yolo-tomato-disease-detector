from fastapi import APIRouter, UploadFile, File
import uuid
from pathlib import Path


router = APIRouter(prefix="/detect", tags=["Detect"])

OUTPUT_DIR = Path("static/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@router.post("")
async def detect_disease(file: UploadFile = File(...) ):
    image_bytes = await file.read()
    detections,image = run_inference(image_bytes)
    annotated_img = draw_boxes(image, detections)

    file_name = f"{uuid.uuid4()}.jpg"
    output_path = OUTPUT_DIR / file_name
    annotated_img.save(output_path)

    diseases = list({d["label"] for d in detections})

    return {
        "detected_diseases": diseases,
        "boxes": detections,
        "annotated_image": f"/static/outputs/{file_name}"
    
    }


