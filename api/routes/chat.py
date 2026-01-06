from fastapi import APIRouter
from api.schemas.chat_schema import ChatRequest, ChatResponse
from core.run_graph import run_graph
from langchain_core.messages import SystemMessage

router = APIRouter(prefix="/chat", tags=["chat"])

# Session storage: {session_id: {"messages": [], "detected_disease": str}}
CHAT_MEMORY = {}

@router.post("", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    session_id = req.session_id
    
    # Get or initialize session data
    if session_id not in CHAT_MEMORY:
        CHAT_MEMORY[session_id] = {
            "messages": [],
            "detected_disease": None
        }
    
    session_data = CHAT_MEMORY[session_id]
    messages = session_data["messages"]
    
    # Update detected disease if provided
    if req.detected_disease:
        session_data["detected_disease"] = req.detected_disease
    
    system_context = None
    user_question = req.message

    # First interaction after disease detection
    if req.is_first_message and req.detected_disease:
        detected_disease = req.detected_disease
        system_context = (
            f"The plant disease detected is {detected_disease}. "
            f"The name of the disease is {detected_disease}. "
            f"You are an agricultural assistant. "
            f"Give accurate, safe, and practical advice. "
            f"You have access to the disease name and should reference it in your answers."
        )

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