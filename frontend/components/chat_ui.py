import streamlit as st

def chat_ui(disease):
    st.subheader("Ask about the disease")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for role, msg in st.session_state.chat_history:
        st.chat_message(role).write(msg)

    user_input = st.chat_input("Ask anything...")
    if user_input:

        st.chat_message("user").write(user_input)
        response = chat_backend(user_input, disease)
        st.chat_message("assistant").write(response)
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("assistant", response))


