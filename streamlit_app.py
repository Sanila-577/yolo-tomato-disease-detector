import streamlit as st
from core.run_graph import app
from langchain_core.messages import HumanMessage, AIMessage

# —————— THEME HANDLING ——————

# Initialize theme in session state
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Toggle button
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Switch Theme"):
        # Toggle between light and dark
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

# CSS to force light/dark theme based on session state
if st.session_state.theme == "dark":
    st.markdown(
        """
        <style>
            .stApp {background-color: #0E1117; color: #FFFFFF;}
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
            .stApp {background-color: #FFFFFF; color: #000000;}
        </style>
        """,
        unsafe_allow_html=True,
    )

# —————— APP TITLE ——————

st.title("🌱 Plant RAG Chatbot")

# —————— SESSION STATE SETUP ——————

if "messages" not in st.session_state:
    st.session_state.messages = []

# —————— CHAT INTERFACE ——————

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about plants:"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # —————— LLM STATE ——————

    state = {
        "question": prompt,
        "messages": [
            HumanMessage(content=prompt)
            if isinstance(prompt, str)
            else HumanMessage(content=str(prompt))
        ],
        "route": None,
        "retrieved_docs": [],
        "web_retrievals": [],
        "enough_info": None,
        "final_answer": None,
    }

    # Call your RAG agent
    result = app.invoke(state)

    # Get the answer
    final_answer = result.get("final_answer", "Sorry, something went wrong 😕")

    # Store and display assistant response
    st.session_state.messages.append({"role": "assistant", "content": final_answer})
    with st.chat_message("assistant"):
        st.markdown(final_answer)