from fastapi import APIRouter
from api.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    answer = get_rag_response(
        question=req.message,
        disease=req.detected_disease
    )
    return ChatResponse(answer=answer)
    