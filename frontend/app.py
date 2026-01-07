import streamlit as st
from frontend.state import (
    init_state,
    load_persisted_state,
    save_persisted_state,
)
from frontend.components.chat_ui import chat_ui
from frontend.components.detection_view import show_detection

# ----------------------------
# App Config
# ----------------------------
st.set_page_config(
    page_title="Neuro Leaf",
    layout="wide"
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

if uploaded_image:
    detection_result = show_detection(image_file=uploaded_image)

    if detection_result:
        detected_disease = (
            detection_result.get("detected_disease")
            or (detection_result.get("report", {}) or {}).get("primary_diagnosis")
        )

        # Save detection + reset chat
        st.session_state["detected_disease"] = detected_disease
        st.session_state["detection_result"] = detection_result

        save_persisted_state(
            st.session_state.session_id,
            st.session_state["detection_result"],
            st.session_state["chat_history"],
        )

        chat_ui(detected_disease)

elif st.session_state.get("detection_result"):
    # Rehydrate UI if refresh happens
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