from fastapi import APIRouter, UploadFile, File, Request
import uuid
from pathlib import Path
import numpy as np
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

    # 2️⃣ Run YOLO inference (supports 3- or 4-value return)
    inference_result = run_yolo_inference(image_bytes)
    if not isinstance(inference_result, tuple):
        raise ValueError("run_yolo_inference did not return a tuple as expected")

    # Handle both legacy and updated signatures gracefully
    # if len(inference_result) == 4:
    #     first, second, third, fourth = inference_result
    #     if isinstance(first, str):
    #         # (detected_disease, detections, report, image)
    #         detected_disease, detections, report, image = first, second, third, fourth
    #     elif isinstance(first, np.ndarray):
    #         # (image, detections, report, detected_disease?) -> prefer report for disease
    #         image, detections, report, maybe_disease = first, second, third, fourth
    #         detected_disease = (
    #             (report or {}).get("primary_diagnosis")
    #             or (maybe_disease if isinstance(maybe_disease, str) else "Healthy")
    #         )
    #     else:
    #         raise ValueError("Unsupported return signature from run_yolo_inference (len=4)")
    if len(inference_result) == 3:
        first, second, third = inference_result
        if isinstance(first, np.ndarray):
            # Current signature: (image, detections, report)
            image, detections, report = first, second, third
            detected_disease = (report or {}).get("primary_diagnosis", "Healthy")
        elif isinstance(first, str):
            # Legacy signature: (detected_disease, detections, image)
            detected_disease, detections, image = first, second, third
            report = None
        else:
            raise ValueError("Unsupported return signature from run_yolo_inference (len=3)")
    else:
        raise ValueError(f"run_yolo_inference returned unexpected tuple length {len(inference_result)}")

    # 3️⃣ Ensure image is a numpy array and draw bounding boxes
    if image is None or not hasattr(image, "shape"):
        # Fallback: decode again from the original bytes
        np_arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
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
        output_image_path=image_url,
        report=report
    )