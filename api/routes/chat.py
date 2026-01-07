from fastapi import APIRouter
from api.schemas.chat_schema import ChatRequest, ChatResponse
from core.run_graph import run_graph
from langchain_core.messages import SystemMessage
import json

router = APIRouter(prefix="/chat", tags=["chat"])

# Session storage: {session_id: {"messages": [], "detected_disease": str, "report": dict}}
CHAT_MEMORY = {}

@router.post("", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    print("In the chat endpoint")
    print("Chat memory: ", CHAT_MEMORY)
    session_id = req.session_id
    
    # Get or initialize session data
    if session_id not in CHAT_MEMORY:
        CHAT_MEMORY[session_id] = {
            "messages": [],
            "detected_disease": None,
            "report": None,
        }
    
    session_data = CHAT_MEMORY[session_id]
    print(session_data)
    messages = session_data["messages"]
    print("messages: ",messages)
    
    # If disease changes, reset conversation so memory only reflects the latest detection
    if req.detected_disease and req.detected_disease != session_data.get("detected_disease"):
        print("disease changed")
        session_data["messages"] = []
        session_data["detected_disease"] = req.detected_disease
        session_data["report"] = req.report
    elif req.detected_disease:
        print("disease not changed")
        session_data["detected_disease"] = req.detected_disease
        if req.report:
            session_data["report"] = req.report
    
    system_context = None
    user_question = req.message
    print("Request first message da? ",req.is_first_message)
    print("user question? ",user_question)
    print("disease?",req.detected_disease)


    # First interaction after disease detection
    if req.is_first_message and req.detected_disease:
        detected_disease = req.detected_disease
        report_blob = session_data.get("report") or {}
        system_context = (
            f"The plant disease detected is {detected_disease}. "
            f"You are an agricultural assistant. Give accurate, safe, and practical advice. "
            f"Use this detection report to ground your answer: {json.dumps(report_blob)}"
        )
        print("System context: ",system_context)

        # If frontend sends empty message, auto-generate first question
        if not user_question.strip():
            user_question = f"What is the treatment for {detected_disease}?"

    answer, messages = run_graph(
        user_input=user_question,
        messages=messages,
        system_context=system_context
    )

    # Update session with new messages
    CHAT_MEMORY[session_id]["messages"] = messages
    
    return ChatResponse(
        answer=answer,
        detected_disease=session_data["detected_disease"],
        session_id=session_id
    )