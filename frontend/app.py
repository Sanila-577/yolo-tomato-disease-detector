import streamlit as st
from frontend.state import init_state

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
    detection = show_detection()

    if detection:
        st.session_state["detected_disease"] = detection
        st.divider()
        chat_ui(detection)