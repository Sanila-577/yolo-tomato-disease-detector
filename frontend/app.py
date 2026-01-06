import streamlit as st
from frontend.state import init_state
from frontend.components.chat_ui import chat_ui
from frontend.components.detection_view import show_detection

st.set_page_config(
    page_title="Tomato Plant Disease Detection",
    layout="wide"
)

init_state()

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
    detection = show_detection(uploaded_image)

    if detection:
        st.session_state["detected_disease"] = detection
        st.divider()
        chat_ui(detection)