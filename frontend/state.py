import streamlit as st

def init_state():
    if "detected_disease" not in st.session_state:
        st.session_state.detected_disease = None