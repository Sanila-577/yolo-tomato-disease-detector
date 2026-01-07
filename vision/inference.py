import cv2
import numpy as np
from typing import List, Dict, Tuple
from vision.model import yolo_model

# --- CONFIGURATION ---
# We treat Late Blight as "High Priority" due to its rapid spread
HIGH_PRIORITY_DISEASES = {"Late Blight"}

# Treatment Dictionary for your specific 7 classes
TREATMENT_ADVISOR = {
    "Late_blight": "EMERGENCY: Highly contagious. Remove and destroy infected plants. Do not compost. Apply fungicides to healthy neighbors.",
    "Early_Blight": "Remove lower infected leaves. Improve airflow. Use copper-based fungicides if spreading.",
    "Bacterial_Spot": "Avoid overhead watering. Apply copper-based bactericides. Sanitize tools between plants.",
    "Leaf_Mold": "Reduce humidity and increase ventilation. Prune for better airflow.",
    "Target_Spot": "Remove debris from soil. Apply appropriate fungicide. Avoid working with plants when wet.",
    "Black_Spot": "Prune infected areas. Improve drainage and sunlight exposure.",
    "Healthy": "Plant looks great! Keep monitoring and maintain regular watering/fertilizing."
}

def iou(boxA, boxB):
    xA = max(boxA["x1"], boxB["x1"])
    yA = max(boxA["y1"], boxB["y1"])
    xB = min(boxA["x2"], boxB["x2"])
    yB = min(boxA["y2"], boxB["y2"])
    interW, interH = max(0, xB - xA), max(0, yB - yA)
    interArea = interW * interH
    boxAArea = (boxA["x2"] - boxA["x1"]) * (boxA["y2"] - boxA["y1"]) 
    boxBArea = (boxB["x2"] - boxB["x1"]) * (boxB["y2"] - boxB["y1"]) 
    denom = boxAArea + boxBArea - interArea
    return interArea / denom if denom > 0 else 0.0

def run_yolo_inference(image_bytes: bytes):
    # 1. Decode Image
    np_arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Failed to decode image")
    h, w = image.shape[:2]

    # 2. YOLO Inference
    results = yolo_model(image)
    print(results)
    result = results[0]
    
    raw_detections: List[Dict] = []
    if result.boxes is not None:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            label = yolo_model.names[cls_id]
            conf = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            # Dynamic Thresholding: Late Blight is shown even at 45% confidence
            threshold = 0.45 if label in HIGH_PRIORITY_DISEASES else 0.60
            
            if conf >= threshold:
                raw_detections.append({
                    "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                    "confidence": conf, "label": label,
                    "notes": [], "is_priority": label in HIGH_PRIORITY_DISEASES
                })

    # 3. Conflict Resolution (Overlap Handling)
    # Sort by confidence so we process strongest matches first
    raw_detections.sort(key=lambda x: x["confidence"], reverse=True)
    kept: List[Dict] = []
    
    for i, current in enumerate(raw_detections):
        keep_current = True
        for j, other in enumerate(kept):
            if iou(current, other) > 0.5:
                # If they overlap, add the "loser" to the "winner's" notes
                if current["label"] != other["label"]:
                    other["notes"].append(f"Symptoms also resemble {current['label']}")
                keep_current = False
                break
        if keep_current:
            kept.append(current)

    # 4. Analyze Results for Report
    if not kept:
        primary_diag = "Healthy"
        severity = "None"
        count = 0
    else:
        # Filter out 'Healthy' boxes for diagnosis if diseases are present
        diseases_found = [d for d in kept if d["label"] != "Healthy"]
        if not diseases_found:
            primary_diag = "Healthy"
        else:
            primary_diag = max(diseases_found, key=lambda x: x["confidence"])["label"]
        
        count = len(diseases_found)
        print("Number of diseases: ", count)
        
        total_disease_area = sum((d["x2"]-d["x1"])*(d["y2"]-d["y1"]) for d in diseases_found)
        coverage = total_disease_area / (w * h)

        # Severity Logic
        if primary_diag in HIGH_PRIORITY_DISEASES or coverage > 0.25:
            severity = "High"
        elif coverage > 0.05 or count >= 2:
            severity = "Medium"
        else:
            severity = "Low"

    # 5. Build Final Report
    co_infections = list(set([d["label"] for d in kept if d["label"] != primary_diag and d["label"] != "Healthy"]))
    print(primary_diag)
    
    # --- Aggregate confidence per disease ---
    disease_conf_map = {}
    for d in kept:
        disease_conf_map.setdefault(d["label"], []).append(d["confidence"])

    disease_confidence_summary = {
        label: {
            "max_confidence": round(max(confs) * 100, 1),
            "mean_confidence": round(sum(confs) / len(confs) * 100, 1),
            "detections": len(confs),
            "is_priority": any(d["is_priority"] for d in kept if d["label"] == label)
        }
        for label, confs in disease_conf_map.items()
    }

    report = {
        "primary_diagnosis": primary_diag,
        "primary_confidence": round(
            max(disease_conf_map.get(primary_diag, [0])) * 100, 1
        ) if disease_conf_map else None,

        "severity_level": severity,
        "co_infections": co_infections,

        "disease_confidence_summary": disease_confidence_summary,

        "treatment_steps": TREATMENT_ADVISOR.get(primary_diag, "Monitor plant health."),
        "alert_type": "EMERGENCY" if primary_diag == "Late_blight" else "STANDARD"
    }
    print("kept: ",kept)
    print("report: ",report)

    return image, kept, report