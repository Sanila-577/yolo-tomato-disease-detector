import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/chat"

def chat_backend(message, disease, session_id="default"):
    # Track if this is the first message in this session
    session_key = f"api_session_{session_id}"
    is_first = session_key not in st.session_state
    if is_first:
        st.session_state[session_key] = True
    
    payload = {
        "message": message,
        "detected_disease": disease,
        "session_id": session_id,
        "is_first_message": is_first
    }
    res = requests.post(API_URL, json=payload)
    response_data = res.json()
    return response_data["answer"], response_data.get("detected_disease")