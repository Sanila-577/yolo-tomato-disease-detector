from pathlib import Path
from ultralytics import YOLO

MODEL_PATH = Path("models/tomato_leaf_disease_detector_v1.pt")

# Load the model once at startup
yolo_model = YOLO(str(MODEL_PATH))

# This file keeps preventing reloading model on every request