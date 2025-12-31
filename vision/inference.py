import cv2
from typing import Tuple, List
from vision.model import yolo_model
from vision.utils import draw_boxes, save_output_image

def run_yolo_inference(image_path: str):
    image = cv2.imread(image_path)
    results = yolo_model(image)

    detections = []
    disease_labels = set()

    for box in results.boxes:
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

        disease_labels.add(label)

    # Pick most frequent disease
    detected_disease = (
        max(disease_labels, key=lambda x: sum(d["label"] == x for d in detections))
        if disease_labels else "Healthy"

    )

    image_with_boxes = draw_boxes(image, detections)
    output_path = save_output_image(image_with_boxes, "detected.jpg")
    return detected_disease, detections, output_path
