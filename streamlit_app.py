import streamlit as st
from core.run_agent import app
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(page_title="RAG Chatbot",page_icon = "🌱")
st.title("🌱 Plant RAG Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages=[]

user_input = st.text_input("Ask me anything about plants: ")

if user_input:
    st.session_state.messages.append(HumanMessage(content=user_input))

    state = {
        "question": user_input,
        "messages": st.session_state.messages,
        "route": None,
        "retrieved_docs": [],
        "web_retrievals": [],
        "enough_info": None,
        "final_answer": None
    }

    result = app.invoke(state)

    final_answer = result.get("final_answer","No answer generated")

    st.session_state.messages.append(AIMessage(content=final_answer))

for msg in st.session_state.messages:
    if isinstance(msg, AIMessage):
        st.markdown(f"**🧑 You:** {msg.content}")
