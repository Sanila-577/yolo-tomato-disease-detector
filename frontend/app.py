import streamlit as st
from frontend.state import init_state
from frontend.components.chat_ui import chat_ui
from frontend.components.detection_view import show_detection

st.set_page_config(
    page_title="Tomato Plant Disease Detection",
    layout="wide"
)

init_state()

st.title("Tomato leaf disease detetection")

uploaded_image = st.file_uploader(
    "Upload a tomato leaf image",
    type = ["jpg","png","jpeg"]
)

if uploaded_image:
    detection = show_detection(uploaded_image)

    if detection:
        st.session_state["detected_disease"] = detection
        st.divider()
        chat_ui(detection)