from fastapi import FastAPI
from api.routes.health import router as health_router
from api.routes.chat import router as chat_router
from api.routes.detect import router as detect_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Tomato plant disease detection",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "service": "Tomato Leaf Disease Detection API",
        "status": "running",
        "version": "1.0.0"
        }

app.include_router(health_router) # Register the router
app.include_router(detect_router)
app.include_router(chat_router)

#app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows Streamlit Cloud to connect
    allow_methods=["*"],
    allow_headers=["*"],
)