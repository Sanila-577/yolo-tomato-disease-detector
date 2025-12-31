from pathlib import Path
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "models" / "tomato_leaf_disease_detector_v1.pt"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"YOLO model not found at {MODEL_PATH}")

yolo_model = YOLO(str(MODEL_PATH))

# This file keeps preventing reloading model on every request