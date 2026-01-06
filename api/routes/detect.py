from fastapi import APIRouter, UploadFile, File, Request
import uuid
from pathlib import Path
import cv2

from vision.inference import run_yolo_inference
from vision.utils import draw_boxes
from api.schemas.vision_schema import VisionResponse

router = APIRouter(prefix="/detect", tags=["Detect"])

OUTPUT_DIR = Path("static/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@router.post("", response_model=VisionResponse)
async def detect_disease(request: Request, file: UploadFile = File(...)):
    # 1️⃣ Read image bytes from request
    image_bytes = await file.read()

    # 2️⃣ Run YOLO inference (UPDATED signature)
    detected_disease, detections, image = run_yolo_inference(image_bytes)

    # 3️⃣ Draw bounding boxes (OpenCV image)
    annotated_img = draw_boxes(image, detections)

    # 4️⃣ Save annotated image using OpenCV
    file_name = f"{uuid.uuid4()}.jpg"
    output_path = OUTPUT_DIR / file_name

    if annotated_img is None:
        raise ValueError("Annotated image is empty")

    cv2.imwrite(str(output_path), annotated_img)

    image_url = f"{request.base_url}static/outputs/{file_name}"

    # 5️⃣ Return validated response
    return VisionResponse(
        detected_disease=detected_disease,
        detections=detections,
        output_image_path=image_url
    )