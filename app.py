import streamlit as st
import os
from PIL import Image
from state import (
    init_state,
    load_persisted_state,
    save_persisted_state,
)
from components.chat_ui import chat_ui
from components.detection_view import show_detection

# ----------------------------
# App Config
# ----------------------------
st.set_page_config(
    page_title="Neuro Leaf - Tomato Disease Detection",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------
# Initialize State
# ----------------------------
init_state()

persisted = load_persisted_state(st.session_state.session_id)
if persisted and not st.session_state.get("detection_result"):
    st.session_state["detection_result"] = persisted.get("detection_result")
    st.session_state["chat_history"] = persisted.get("chat_history", [])
    if st.session_state.get("detection_result"):
        st.session_state["detected_disease"] = (
            st.session_state["detection_result"].get("detected_disease")
            or (st.session_state["detection_result"].get("report", {}) or {}).get("primary_diagnosis")
        )


# ----------------------------
# Sidebar - Sample Images
# ----------------------------
st.sidebar.title("Sample Images")
st.sidebar.caption("Select a sample tomato leaf")

SAMPLE_DIR = "samples"

sample_image = None
if os.path.exists(SAMPLE_DIR):
    sample_files = [
        f for f in os.listdir(SAMPLE_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if sample_files:
        selected_sample = st.sidebar.radio(
            "Choose a sample",
            sample_files
        )

        sample_path = os.path.join(SAMPLE_DIR, selected_sample)
        sample_image = Image.open(sample_path)

        st.sidebar.image(
            sample_image,
            caption=selected_sample,
            use_container_width=True
        )

# ----------------------------
# App Title
# ----------------------------
st.title("Tomato leaf disease detection")

# ----------------------------
# File Upload / Detection
# ----------------------------
uploaded_image = st.file_uploader(
    "Upload a tomato leaf image",
    type=["jpg", "png", "jpeg"]
)

input_image = None
image_source = None

if uploaded_image:
    input_image = uploaded_image
    image_source = "Uploaded Image"
elif sample_image:
    input_image = sample_image
    image_source = "Sample Image"

if input_image:
    st.subheader(image_source)
    detection_result = show_detection(image_file=input_image)

    if detection_result:
        detected_disease = (
            detection_result.get("detected_disease")
            or (detection_result.get("report", {}) or {}).get("primary_diagnosis")
        )

        st.session_state["detected_disease"] = detected_disease
        st.session_state["detection_result"] = detection_result

        save_persisted_state(
            st.session_state.session_id,
            st.session_state["detection_result"],
            st.session_state["chat_history"],
        )

        if detected_disease:
            chat_ui(detected_disease)

elif st.session_state.get("detection_result"):
    detection_result = st.session_state["detection_result"]
    detected_disease = (
        detection_result.get("detected_disease")
        or (detection_result.get("report", {}) or {}).get("primary_diagnosis")
    )

    show_detection(cached_result=detection_result)

    if detected_disease:
        st.session_state["detected_disease"] = detected_disease
        save_persisted_state(
            st.session_state.session_id,
            st.session_state["detection_result"],
            st.session_state["chat_history"],
        )

        chat_ui(detected_disease)