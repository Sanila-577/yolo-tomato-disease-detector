import cv2
from vision.model import yolo_model
from vision.utils import draw_boxes, save_output_image
import numpy as np

def run_yolo_inference(image_bytes: bytes):
    np_arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Failed to decode image bytes")

    results = yolo_model(image)
    result = results[0]

    detections = []
    disease_labels = []

    if result.boxes is not None:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            label = yolo_model.names[cls_id]
            confidence = float(box.conf[0])

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            detections.append({
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "confidence": confidence,
                "label": label
            })

            disease_labels.append(label)

    detected_disease = (
        max(set(disease_labels), key=disease_labels.count)
        if disease_labels else "Healthy"
    )

    return detected_disease, detections, image