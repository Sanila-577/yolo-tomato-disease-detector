from fastapi import APIRouter
from api.schemas.chat_schema import ChatRequest, ChatResponse
from core.run_graph import run_graph

router = APIRouter(prefix="/chat", tags=["chat"])

CHAT_MEMORY = {}

@router.post("", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    # 🔴 HARD-CODED TEST QUESTION
    test_question = "What is the treatment for tomato early blight?"

    session_id = "default"  # later replace with real session/user ID
    messages = CHAT_MEMORY.get(session_id, [])


    system_context = None
    user_question = req.message

    # First interaction after disease detection
    if req.is_first_message and req.detected_disease:
        system_context = (
            f"The plant disease detected is {req.detected_disease}. "
            f"You are an agricultural assistant. "
            f"Give accurate, safe, and practical advice."
        )

        # If frontend sends empty message, auto-generate first question
        if not user_question.strip():
            user_question = f"What is the treatment for {req.detected_disease}?"

    answer, messages = run_graph(
        user_input=user_question,
        messages=messages,
        system_context=system_context
    )

    CHAT_MEMORY[session_id] = messages
    return ChatResponse(answer=answer)