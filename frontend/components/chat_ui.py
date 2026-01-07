import streamlit as st
from frontend.services.chat_service import chat_backend
from frontend.state import save_persisted_state


def chat_ui(disease):
    st.subheader("Ask about the disease")

    history_key = "chat_history"
    if history_key not in st.session_state:
        st.session_state[history_key] = []

    # Display chat history
    for role, msg in st.session_state[history_key]:
        st.chat_message(role).write(msg)

    user_input = st.chat_input("Ask anything...")
    if user_input:
        st.chat_message("user").write(user_input)

        session_id = st.session_state.get("session_id", "default")
        response, stored_disease = chat_backend(user_input, disease, session_id=session_id)

        st.chat_message("assistant").write(response)

        # Update local chat history for UI display only
        st.session_state[history_key].append(("user", user_input))
        st.session_state[history_key].append(("assistant", response))

        save_persisted_state(
            session_id,
            st.session_state.get("detection_result"),
            st.session_state[history_key],
        )


