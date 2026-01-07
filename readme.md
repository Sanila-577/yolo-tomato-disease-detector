# 🌱 Neuro Leaf: Tomato Leaf Disease Assistant

FastAPI + LangGraph backend with a Streamlit frontend for tomato leaf disease detection and guidance. Runs YOLO-based vision to detect diseases, feeds the latest report into a LangGraph chat pipeline, and serves responses through a chat UI.

---

## 📦 What’s Inside

- FastAPI service (`api/main.py`) with routes:
  - `/detect` – runs YOLO inference, returns annotated image + report
  - `/chat` – LangGraph chat endpoint with per-session memory
  - `/health` – basic health check
- Streamlit UI (`frontend/app.py`) for upload, detection preview, and chat
- LangGraph agents (`agents/`) for routing, RAG, web fallback, and grading
- Vision pipeline (`vision/`) and YOLO weights in `models/tomato_leaf_disease_detector_v1.pt`
- FAISS vector store in `faiss_db/` for RAG
- Shared state helpers in `frontend/state.py` for session IDs and caching

---

## 🗂️ Project Structure (high level)

```
agents/                    # LangGraph agents
  ├── router_agent.py      # Routes queries (chat/RAG/web)
  ├── chat_agent.py        # Conversational agent
  ├── retriever_agent.py   # RAG retriever over FAISS
  ├── web_agent.py         # Web search fallback (Tavily)
  ├── grader_answer_agent.py # Grades answer relevance
  ├── state.py             # Agent state management
  └── __init__.py
api/                       # FastAPI backend
  ├── main.py              # FastAPI app
  ├── routes/
  │   ├── chat.py          # /chat endpoint
  │   ├── detect.py        # /detect endpoint
  │   └── health.py        # /health endpoint
  ├── schemas/
  │   ├── chat_schema.py
  │   └── vision_schema.py
  ├── static/outputs/      # Annotated images from detection
  └── __init__.py
core/                      # Core logic & LangGraph
  ├── build_graph.py       # Construct LangGraph workflow
  ├── run_graph.py         # Execute graph
  ├── faiss_setup.py       # FAISS index initialization
  ├── llm.py               # LLM configuration
  └── __init__.py
frontend/                  # Streamlit UI
  ├── app.py               # Main app entry
  ├── config.py            # Configuration
  ├── state.py             # Session state management
  ├── components/
  │   ├── chat_ui.py       # Chat interface
  │   └── detection_view.py # Detection preview
  ├── services/
  │   ├── chat_service.py  # Chat API calls
  │   └── detection_service.py # Detection API calls
  └── __init__.py
vision/                    # YOLO inference
  ├── inference.py         # Run inference
  ├── model.py             # Model loading
  ├── utils.py             # Vision utilities
  └── __init__.py
tools/                     # Tool integrations
  ├── retriever_tool.py    # FAISS retrieval
  ├── tavily_search_tool.py # Web search
  └── __init__.py
models/                    # Pre-trained weights
  └── tomato_leaf_disease_detector_v1.pt
faiss_db/                  # Vector store index
  └── index.faiss
data/                      # Training data
  └── dataset/             # Roboflow dataset (YOLO format)
      ├── train/
      ├── valid/
      └── test/
static/outputs/            # Generated annotated images
docs/                      # Documentation
readme.md, requirements.txt
```

---

## 🧰 Prerequisites

- Python 3.10+ recommended
- Virtual environment (venv/conda)
- GPU optional; YOLO will run on CPU if CUDA is unavailable

Environment variables (create `.env` in project root):

```
OPENROUTER_API_KEY=your_key          # for LLM in core/llm.py
TAVILY_API_KEY=your_key              # for web fallback
```

---

## 🚀 Setup

```bash
python -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

If you need the FAISS index fresh, delete `faiss_db/` and it will rebuild on first RAG call.

---

## ▶️ Run the stack

In one terminal (backend):

```bash
cd /Users/sanilawijesekara/Documents/RAG-chatbot
fastapi dev ./api/main.py           # or: uvicorn api.main:app --reload
```

In another terminal (frontend):

```bash
cd /Users/sanilawijesekara/Documents/RAG-chatbot
streamlit run ./frontend/app.py
```

Open Streamlit at http://localhost:8501 and upload a tomato leaf image.

---

## 🧠 How it works

1) Upload leaf image → `/detect` returns annotated image + structured report
2) The latest report is stored per session and sent with the first chat turn
3) LangGraph routes: chat for small talk, RAG over FAISS for plant knowledge, web for out-of-domain
4) Chat memory resets when a new disease is detected; the UI still shows your previous messages for convenience

---

## 🔎 Troubleshooting

- If detection fails: ensure the model file exists at `models/tomato_leaf_disease_detector_v1.pt` and the image is a valid JPG/PNG.
- If chat fails: confirm `fastapi dev ./api/main.py` is running and API_URL in frontend services points to the backend (defaults to 127.0.0.1:8000).
- For theme issues: UI styling is driven by `frontend/styles/theme.css`; adjust there if needed.

---

## 📄 License

MIT (update if your project uses a different license).
