from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"]) # container to register endpoints
# /health is the primary endpoint. That's why it is in prefix

@router.get("") # "" means there are no secondary endpoints like /health/status/...
async def health():
    return {
        "status":"ok"
    }