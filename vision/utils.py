import cv2
from pathlib import Path
from typing import List

def draw_boxes(image, detections: List[dict]):

    for det in detections:
        x1, y1, x2, y2 = map(int, [det["x1"], det["y1"], det["x2"], det["y2"]])
        label = f"{det['label']} ({det['confidence']:.2f})"
        color = (0, 255, 0)
        if det.get("is_quarantine"):
            color = (0, 165, 255)  # orange for warnings
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        
        cv2.putText(
            image,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2

        )

        # Additional note line if available
        notes = det.get("notes") or []
        if det.get("verification_needed"):
            notes = ["Warning: Verification Needed"] + notes
        if notes:
            note_text = ", ".join(notes)
            cv2.putText(
                image,
                note_text,
                (x1, max(0, y1 - 25)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                1
            )

    return image

def save_output_image(image, filename: str):
    if image is None:
        raise ValueError("Cannot save empty image")

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / filename
    success = cv2.imwrite(str(output_path), image)

    if not success:
        raise RuntimeError("cv2.imwrite failed")

    return str(output_path)


