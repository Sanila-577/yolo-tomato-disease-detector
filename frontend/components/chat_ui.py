import streamlit as st
from frontend.services.chat_service import chat_backend

def chat_ui(disease):
    st.subheader("Ask about the disease")

    # Initialize session-specific chat history
    session_key = f"chat_history_{disease}"
    if session_key not in st.session_state:
        st.session_state[session_key] = []

    # Display chat history
    for role, msg in st.session_state[session_key]:
        st.chat_message(role).write(msg)

    user_input = st.chat_input("Ask anything...")
    if user_input:
        # Display user message
        st.chat_message("user").write(user_input)
        
        # Get response from backend (which maintains server-side history)
        response, stored_disease = chat_backend(user_input, disease)
        
        # Display assistant message
        st.chat_message("assistant").write(response)
        
        # Update local chat history for UI display only
        st.session_state[session_key].append(("user", user_input))
        st.session_state[session_key].append(("assistant", response))


