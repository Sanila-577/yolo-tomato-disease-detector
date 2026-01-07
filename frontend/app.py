import streamlit as st
from frontend.state import (
    init_state,
    load_persisted_state,
    save_persisted_state,
)
from frontend.components.chat_ui import chat_ui
from frontend.components.detection_view import show_detection

st.set_page_config(
    page_title="Tomato Plant Disease Detection",
    layout="wide"
)

init_state()

# Restore cached state (survives browser refresh while server runs)
persisted = load_persisted_state(st.session_state.session_id)
if persisted and not st.session_state.get("detection_result"):
    st.session_state["detection_result"] = persisted.get("detection_result")
    st.session_state["chat_history"] = persisted.get("chat_history", [])
    if st.session_state.get("detection_result"):
        st.session_state["detected_disease"] = (
            st.session_state["detection_result"].get("detected_disease")
            or (st.session_state["detection_result"].get("report", {}) or {}).get("primary_diagnosis")
        )

# Theme toggle state initialization
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"

# Apply theme via custom CSS
if st.session_state.theme_mode == "dark":
    st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stMultiSelect > div > div {
        background-color: #262730;
        color: #FAFAFA;
        border-color: #464B5E;
    }
    .stButton > button {
        background-color: #262730;
        color: #FAFAFA;
        border: 1px solid #464B5E;
    }
    .stButton > button:hover {
        background-color: #363B4E;
        border-color: #57A6FF;
    }
    section[data-testid="stSidebar"] {
        background-color: #262730;
    }
    .theme-toggle-btn {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 999999;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
        color: #111827;
    }
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stMultiSelect > div > div {
        background-color: #FFFFFF;
        color: #111827;
        border-color: #D1D5DB;
    }
    .stButton > button {
        background-color: #FFFFFF;
        color: #111827;
        border: 1px solid #D1D5DB;
    }
    .stButton > button:hover {
        background-color: #F5F7FA;
        border-color: #0A84FF;
    }
    section[data-testid="stSidebar"] {
        background-color: #F5F7FA;
    }
    .theme-toggle-btn {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 999999;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

# Create columns for button alignment
col1, col2 = st.columns([8, 1])
with col2:
    icon = "🌙" if st.session_state.theme_mode == "light" else "☀️"
    if st.button(icon, key="theme_toggle", help="Toggle theme"):
        new_mode = "dark" if st.session_state.theme_mode == "light" else "light"
        st.session_state.theme_mode = new_mode
        st.rerun()

st.title("Tomato leaf disease detetection")

uploaded_image = st.file_uploader(
    "Upload a tomato leaf image",
    type = ["jpg","png","jpeg"]
)

if uploaded_image:
    detection_result = show_detection(image_file=uploaded_image)

    if detection_result:
        detected_disease = (
            detection_result.get("detected_disease")
            or (detection_result.get("report", {}) or {}).get("primary_diagnosis")
        )

        # Persist latest detection + reset chat to avoid mixing past diseases
        st.session_state["detected_disease"] = detected_disease
        st.session_state["detection_result"] = detection_result

        save_persisted_state(
            st.session_state.session_id,
            st.session_state["detection_result"],
            st.session_state["chat_history"],
        )

        chat_ui(detected_disease)
elif st.session_state.get("detection_result"):
    # Rehydrate UI from cached detection so refresh doesn't blank the page
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