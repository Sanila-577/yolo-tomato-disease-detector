import requests
import streamlit as st

# API_URL = "http://127.0.0.1:8000/detect"

BACKEND_URL = st.secrets.get("BACKEND_URL","http://localhost:8000")

def detect_disease(image_file):
    # Streamlit's UploadedFile needs to be converted into a proper multipart tuple
    try:
        file_bytes = image_file.getvalue() if hasattr(image_file, "getvalue") else image_file.read()
        filename = getattr(image_file, "name", "upload.jpg")
        content_type = getattr(image_file, "type", None) or "image/jpeg"

        files = {"file": (filename, file_bytes, content_type)}
        res = requests.post(f"{BACKEND_URL}/detect", files=files, timeout=300)
        res.raise_for_status()
        return res.json()
    except requests.HTTPError as e:
        # Surface server-side error details if available
        detail = None
        try:
            detail = res.text
        except Exception:
            pass
        raise RuntimeError(f"Detection API error: {e}. Response: {detail}")
    except ValueError as e:
        # JSON decode errors
        raise RuntimeError(f"Invalid JSON from Detection API: {e}")