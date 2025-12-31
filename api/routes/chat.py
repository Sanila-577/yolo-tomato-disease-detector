from fastapi import APIRouter
from api.schemas.chat_schema import ChatRequest, ChatResponse
from core.run_graph import run_graph

router = APIRouter(prefix="/chat", tags=["chat"])

CHAT_MEMORY = {}

@router.post("", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    session_id = "default"  # later replace with user/session ID

    messages = CHAT_MEMORY.get(session_id, [])

    # Inject disease context ONLY once
    if req.is_first_message and req.detected_disease:
        system_prompt = (
            f"The plant disease detected is {req.detected_disease}. "
            f"Provide accurate, agriculture-safe guidance. "
         
        )
        answer, messages = run_graph(system_prompt, messages)

    # Normal user message
    answer, messages = run_graph(req.message, messages)

    CHAT_MEMORY[session_id] = messages

    return ChatResponse(answer=answer)