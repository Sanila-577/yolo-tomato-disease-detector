from fastapi import FastAPI
from api.routes.health import router as health_router
from api.routes.chat import router as chat_router
from api.routes.detect import router as detect_router

app = FastAPI(
    title="Tomato plant disease detection",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"messege": "Hello World"}

app.include_router(health_router) # Register the router
app.include_router(detect_router)
app.include_router(chat_router)

