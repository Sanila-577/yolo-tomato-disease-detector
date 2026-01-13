# 🌱 Neuro Leaf: Tomato Leaf Disease Assistant

A production-ready AI system combining computer vision and conversational AI for tomato leaf disease diagnosis and treatment guidance. Built with FastAPI backend, LangGraph agentic workflow, and Streamlit frontend.

---

## 📦 What's Inside

### 🔧 Backend (FastAPI)

- **API Service** (`api/main.py`):
  - `POST /detect` – YOLO-based disease detection with annotated images and structured reports
  - `POST /chat` – LangGraph-powered chat with session-based memory
  - `GET /health` – Health check endpoint
  - Static file serving for annotated images at `/static`

### 🤖 AI Components

- **LangGraph Agents** (`agents/`):
  - **Router Agent** – Intelligently routes queries to chat, RAG, or web search
  - **Chat Agent** – Handles casual conversation and greetings
  - **Retriever Agent** – RAG over FAISS vector store with PDF knowledge base
  - **Web Agent** – Tavily-powered web search for out-of-domain queries
  - **Grader Agent** – Evaluates answer relevance and triggers fallback if needed

### 🎨 Frontend (Streamlit)

- **Main App** (`frontend/app.py`):
  - Image upload and disease detection interface
  - Real-time chat UI with disease-specific context
  - Session state management with persistence
  - Automatic memory reset on new disease detection

### 🔬 Vision System (YOLO)

- **Inference Pipeline** (`vision/`):
  - **Ultralytics YOLOv11 Large (YOLO11l)** object detection for 7 disease classes
  - Non-maximum suppression (NMS) for overlapping detections
  - Structured report generation with severity levels
  - Treatment recommendations based on disease type
  - High-priority disease flagging (e.g., Late Blight)

### 📚 Knowledge Base

- **FAISS Vector Store** (`faiss_db/`):
  - Built from PDF documents in `context/` folder (10 research papers)
  - Embeddings via HuggingFace `all-MiniLM-L6-v2`
  - Covers 6 major tomato diseases with scientific literature
  - Automatically rebuilds if index is missing

### 🔑 Key Features

- Session-based chat memory that persists across page refreshes
- Disease-specific conversation context injection
- Multi-agent routing for optimal answer quality
- Fallback mechanism from RAG to web search
- Treatment advisor with disease-specific guidance
- Support for 7 disease classes + healthy state
- OpenAI GPT-4o-mini via OpenRouter for LLM inference

---

## 🗂️ Project Structure

```
agents/                              # LangGraph agent implementations
  ├── router_agent.py                # Query routing logic (chat/RAG/web)
  ├── chat_agent.py                  # Conversational responses
  ├── retriever_agent.py             # FAISS-based RAG retrieval
  ├── web_agent.py                   # Tavily web search integration
  ├── grader_answer_agent.py         # Answer relevance evaluation
  ├── state.py                       # AgentState TypedDict definition
  └── __init__.py

api/                                 # FastAPI backend
  ├── main.py                        # FastAPI app with static file mounting
  ├── routes/
  │   ├── chat.py                    # Chat endpoint with session memory
  │   ├── detect.py                  # YOLO detection endpoint
  │   └── health.py                  # Health check endpoint
  ├── schemas/
  │   ├── chat_schema.py             # Pydantic schemas for chat (ChatRequest/Response)
  │   └── vision_schema.py           # Pydantic schemas for vision (VisionResponse)
  ├── static/outputs/                # Generated annotated images from detection
  └── __init__.py

core/                                # Core LangGraph & LLM setup
  ├── build_graph.py                 # LangGraph workflow construction & compilation
  ├── run_graph.py                   # Graph execution logic with state management
  ├── faiss_setup.py                 # FAISS index building/loading from PDFs
  ├── llm.py                         # ChatOpenAI via OpenRouter (GPT-4o-mini)
  └── __init__.py

frontend/                            # Streamlit UI
  ├── app.py                         # Main application entry point
  ├── config.py                      # Configuration constants (API URLs, etc.)
  ├── state.py                       # Session state initialization & persistence
  ├── components/
  │   ├── chat_ui.py                 # Chat interface components & message rendering
  │   └── detection_view.py          # Detection result display & image preview
  ├── services/
  │   ├── chat_service.py            # API client for /chat endpoint
  │   └── detection_service.py       # API client for /detect endpoint
  └── __init__.py

vision/                              # YOLO inference pipeline
  ├── inference.py                   # Detection logic with NMS & structured reporting
  ├── model.py                       # YOLO model loading from weights
  ├── utils.py                       # Drawing & visualization utilities (bounding boxes)
  └── __init__.py

tools/                               # LangChain tool wrappers
  ├── retriever_tool.py              # FAISS retrieval tool for RAG agents
  ├── tavily_search_tool.py          # Tavily web search tool wrapper
  └── __init__.py

context/                             # Knowledge base PDFs (10 documents)
  ├── late_blight1.pdf               # Late blight research papers
  ├── late_blight2.pdf
  ├── early_blight1.pdf              # Early blight documentation
  ├── early_blight2.pdf
  ├── bacterial_spot1.pdf            # Bacterial spot studies
  ├── bacterial_spot2.pdf
  ├── leaf_mold1.pdf                 # Leaf mold information
  ├── target_spot1.pdf               # Target spot research
  ├── 9068_SE_S9_Target-Spot-of-Tomato.pdf
  └── s41685-022-00264-5.pdf         # Scientific research paper

models/                              # Pre-trained model weights
  └── tomato_leaf_disease_detector_v1.pt  # YOLOv11 Large model (7 disease classes)

faiss_db/                            # Vector store persistence
  └── index.faiss                    # Auto-generated from context/ PDFs

data/                                # Training datasets
  └── dataset/                       # Roboflow YOLO format dataset
      ├── data.yaml                  # Dataset configuration & class names
      ├── README.dataset.txt         # Dataset documentation
      ├── README.roboflow.txt        # Roboflow export info
      ├── train/                     # Training images & labels
      │   ├── images/
      │   └── labels/
      ├── valid/                     # Validation split
      │   ├── images/
      │   └── labels/
      └── test/                      # Test split
          ├── images/
          └── labels/

docs/                                # Documentation files
  └── Folder structure.docx          # Project structure documentation

.env                                 # Environment variables (not in git)
.gitattributes                       # Git attributes for LFS
readme.md                            # This file
requirements.txt                     # Python dependencies
```

---

## 🧰 Prerequisites

- **Python 3.10+** (recommended)
- **Virtual environment** (venv/conda)
- **GPU optional** – YOLO will run on CPU if CUDA is unavailable
- **API Keys** – Required for full functionality

### 🔐 Environment Variables

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_key    # Required for LLM (GPT-4o-mini via OpenRouter)
TAVILY_API_KEY=your_tavily_key            # Required for web search fallback
```

### 📋 Dependencies

All dependencies are listed in `requirements.txt`:

- **LangChain Ecosystem**: langchain, langchain-core, langchain-openai, langgraph, langchain-community
- **FastAPI Stack**: fastapi, uvicorn, pydantic, python-multipart
- **Machine Learning**: ultralytics (YOLO), sentence-transformers, faiss-cpu
- **Frontend**: streamlit
- **Utilities**: tavily-python, pypdf, opencv-python, pillow, numpy, requests

---

## 🚀 Setup & Installation

### 1. Clone and Navigate

```bash
cd /Users/sanilawijesekara/Documents/RAG-chatbot
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate           # macOS/Linux
# .venv\Scripts\activate            # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create `.env` file with your API keys (see Prerequisites section above).

### 5. Initialize FAISS Index (Optional)

The FAISS index will auto-build on first use. To rebuild manually:

```bash
rm -rf faiss_db/
# Index will rebuild automatically when first RAG query is made
```

---

## ▶️ Running the Application

### Backend (FastAPI)

Open a terminal and run:

```bash
cd /Users/sanilawijesekara/Documents/RAG-chatbot
source .venv/bin/activate
fastapi dev ./api/main.py
# Alternative: uvicorn api.main:app --reload
```

Backend will be available at: **http://127.0.0.1:8000**

- API docs (Swagger): http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

### Frontend (Streamlit)

Open a **second terminal** and run:

```bash
cd /Users/sanilawijesekara/Documents/RAG-chatbot
source .venv/bin/activate
streamlit run ./frontend/app.py
```

Frontend will be available at: **http://localhost:8501**

### 🎯 Usage Flow

1. **Upload Image**: Navigate to http://localhost:8501 and upload a tomato leaf image (JPG/PNG)
2. **View Detection**: See the annotated image with bounding boxes and disease report
3. **Chat**: Ask questions about the detected disease, treatment, prevention, etc.
4. **Session Persistence**: Your chat history persists across page refreshes
5. **New Detection**: Upload a new image to reset the chat context automatically

---

## 🧠 How It Works

### 1. Disease Detection Flow

```
User uploads image → FastAPI /detect endpoint 
→ YOLOv11 Large inference (vision/inference.py)
→ Non-maximum suppression (NMS)
→ Structured report generation
→ Annotated image saved to api/static/outputs/
→ Response with image URL + JSON report
```

### 2. Chat Flow (Agentic Architecture)

The chat system uses a **multi-agent LangGraph workflow** for intelligent query processing and response generation:

#### Architecture Diagram

![alt text](agent_architecture/architecture.png)

#### Workflow Steps

1. **Router Agent** (Decision Node)

   - Classifies incoming user query into three categories: `CHAT`, `RAG`, or `WEB`
   - Routes chat/greeting queries directly to Chat Agent
   - Directs disease/treatment questions to Retriever Agent (RAG)
   - Routes general/out-of-domain questions to Web Search Agent
   - Decision logic: Intent classification + keyword matching
2. **Chat Agent** (Conversational Path)

   - Handles casual greetings and small talk
   - Provides contextual responses without external knowledge
   - Returns responses immediately for chat-only queries
   - Maintains conversational tone and user engagement
3. **Retriever Agent** (RAG Path)

   - Retrieves relevant knowledge from **FAISS vector store** via Retriever Tool
   - Searches across 10 PDF documents covering 6 major tomato diseases
   - Performs semantic similarity search (k=4 documents by default)
   - Passes retrieved context to Grader Agent for quality evaluation
4. **Grader Agent** (Answer Quality Check)

   - Evaluates whether retrieved context adequately answers the user's question
   - Binary decision: `YES` (sufficient context) or `NO` (insufficient context)
   - If `YES`: Proceeds to Answer Generator with RAG context
   - If `NO`: Falls back to Web Search Agent for supplementary information
5. **Web Search Agent** (Fallback Path)

   - Executes Tavily web search for queries not covered by knowledge base
   - Retrieves up-to-date information from the internet
   - Used when RAG retrieval is insufficient
   - Combines web results with original query for answer generation
6. **Answer Generator** (Response Node)

   - Synthesizes final response using:
     - Original user query
     - Retrieved RAG context (if available)
     - Web search results (if used)
     - Disease-specific conversation context (if applicable)
   - Generates clear, concise, and actionable responses
   - Returns response to user via FastAPI chat endpoint

#### Key Features

- **Conditional Routing**: Dynamic workflow based on query classification
- **Fallback Mechanism**: RAG → Web Search → Answer Generation chain
- **Context Injection**: Detected disease information automatically included in conversation
- **State Management**: Maintains conversation state across agent nodes
- **Efficiency**: Chat-only queries skip RAG/Web to minimize latency

### 4. Memory Management

- Each session has a unique `session_id` (UUID)
- Chat history stored in-memory dict: `CHAT_MEMORY[session_id]`
- Memory resets when a **new disease is detected** (different from previous)
- UI maintains visual history for user convenience (persisted via Streamlit state)

### 5. Knowledge Base

The FAISS vector store is built from 10 PDF documents covering:

- Late Blight (2 papers)
- Early Blight (2 papers)
- Bacterial Spot (2 papers)
- Leaf Mold (1 paper)
- Target Spot (2 papers)
- General tomato disease research (1 paper)

Embeddings: **HuggingFace all-MiniLM-L6-v2** (384 dimensions)
Retriever: **FAISS** with similarity search (k=4 default)

### 6. Disease Classes Supported

1. **Late Blight** (High Priority - rapid spread)
2. **Early Blight**
3. **Bacterial Spot**
4. **Leaf Mold**
5. **Target Spot**
6. **Black Spot**
7. **Healthy**

Each disease has tailored treatment recommendations in `vision/inference.py`.

---

## 🔎 Troubleshooting

### Detection Issues

**Problem**: Detection endpoint returns error or no detections**Solutions**:

- Verify model file exists at `models/tomato_leaf_disease_detector_v1.pt`
- Ensure uploaded image is valid JPG/PNG format
- Check image dimensions (YOLOv11 handles various sizes, but very small images may fail)
- Review logs in FastAPI terminal for YOLO errors

**Problem**: Annotated image not displaying**Solutions**:

- Verify `api/static/outputs/` directory exists and is writable
- Check FastAPI static file mounting in `api/main.py`
- Ensure frontend `API_URL` in `frontend/services/` points to correct backend

### Chat Issues

**Problem**: Chat endpoint returns 500 error**Solutions**:

- Confirm backend is running: `fastapi dev ./api/main.py`
- Verify `.env` has `OPENROUTER_API_KEY` set correctly
- Check API_URL in `frontend/config.py` (default: http://127.0.0.1:8000)
- Review backend terminal for LangGraph/LLM errors

**Problem**: Chat responses are empty or irrelevant**Solutions**:

- Check FAISS index exists: `faiss_db/index.faiss`
- Rebuild FAISS: `rm -rf faiss_db/` then restart backend
- Verify PDF files exist in `context/` directory
- Check `TAVILY_API_KEY` for web search fallback

**Problem**: Memory not persisting across refreshes**Solutions**:

- Verify `session_id` is being generated and passed correctly
- Check Streamlit session state in `frontend/state.py`
- Clear browser cache/cookies and restart Streamlit

### Model Loading Issues

**Problem**: YOLOv11 model fails to load**Solutions**:

- Reinstall ultralytics: `pip install --upgrade ultralytics`
- Verify model file is not corrupted (YOLOv11 Large is typically 40-50MB)
- Check disk space and read permissions
- Ensure Ultralytics version supports YOLO11: `pip show ultralytics`

**Problem**: FAISS index build fails**Solutions**:

- Verify all PDFs in `context/` are readable
- Check sentence-transformers installation: `pip install --upgrade sentence-transformers`
- Ensure sufficient RAM (at least 2GB free for embeddings)

### Environment Issues

**Problem**: Import errors or module not found**Solutions**:

- Activate virtual environment: `source .venv/bin/activate`
- Reinstall requirements: `pip install -r requirements.txt`
- Clear Python cache: `find . -type d -name __pycache__ -exec rm -rf {} +`

**Problem**: Port already in use (8000 or 8501)**Solutions**:

- Kill existing process: `lsof -ti:8000 | xargs kill -9` (or 8501 for Streamlit)
- Use alternative ports: `uvicorn api.main:app --port 8001` or `streamlit run frontend/app.py --server.port 8502`

### Performance Issues

**Problem**: Slow inference or chat responses**Solutions**:

- YOLOv11: Use GPU if available (check CUDA installation), or use smaller variant (11n/11s)
- FAISS: Reduce retrieval `k` value in `tools/retriever_tool.py`
- LLM: Use faster model (adjust `core/llm.py` to gpt-3.5-turbo)
- Streamlit: Disable automatic reruns in settings

---

## 🏗️ Architecture Decisions

### Why LangGraph?

- **State Management**: Built-in state passing between agents
- **Conditional Routing**: Dynamic workflow based on query classification
- **Fallback Chains**: Automatic RAG → Web fallback on insufficient information
- **Memory Persistence**: Native support for conversation history

### Why FAISS?

- **Fast Retrieval**: Efficient similarity search for RAG
- **Local Storage**: No external vector DB dependencies
- **Easy Setup**: Auto-builds from PDF documents
- **Lightweight**: Works on CPU with minimal resource requirements

### Why OpenRouter?

- **Model Flexibility**: Easy switching between LLM providers
- **Cost Optimization**: Competitive pricing for GPT-4o-mini
- **Reliability**: Fallback providers if primary is unavailable

### Design Patterns

- **Agent-Based Architecture**: Modular agents with single responsibilities
- **Session-Based Memory**: Per-user conversation context isolation
- **Microservice API**: Decoupled backend and frontend for scalability
- **Static File Serving**: Efficient image delivery via FastAPI static mounting

---

## 🚀 Future Enhancements

- [ ] PostgreSQL integration for persistent chat history
- [ ] Redis caching for FAISS query results
- [ ] Multi-language support (Spanish, Hindi, Chinese)
- [ ] Mobile-responsive UI redesign
- [ ] Real-time detection via webcam/camera feed
- [ ] Export chat history as PDF report
- [ ] Disease progression tracking over time
- [ ] Integration with weather APIs for environmental risk factors
- [ ] Batch image processing for large-scale diagnosis
- [ ] Fine-tuned LLM specifically for agriculture domain

---

## 📚 References & Citations

### Research Papers (in context/)

- Target Spot: 9068_SE_S9_Target-Spot-of-Tomato.pdf
- General Research: s41685-022-00264-5.pdf
- Late Blight, Early Blight, Bacterial Spot, Leaf Mold: Various academic PDFs

### Technologies

- **YOLO**: Ultralytics YOLOv11 Large - https://github.com/ultralytics/ultralytics
- **LangChain**: https://python.langchain.com/
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **FastAPI**: https://fastapi.tiangolo.com/
- **Streamlit**: https://streamlit.io/
- **FAISS**: Facebook AI Similarity Search - https://github.com/facebookresearch/faiss

---

## 👥 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add your feature"`
4. Push to branch: `git push origin feature/your-feature`
5. Open a Pull Request

### Development Setup

Follow the setup instructions above, then:

- Install dev dependencies: `pip install pytest black flake8`
- Run tests: `pytest tests/`
- Format code: `black .`
- Lint: `flake8 .`

---

## 📄 License

MIT License - See LICENSE file for details (update if using a different license).

---

## 🙏 Acknowledgments

- **Roboflow** for dataset hosting and annotation tools
- **Ultralytics** for YOLO implementation
- **LangChain Team** for the agent framework
- **OpenAI/OpenRouter** for LLM access
- **Tavily** for web search capabilities

---

## 📞 Contact & Support

For issues, questions, or contributions:

- Create an issue on GitHub
- Email: [your-email@example.com]
- Documentation: See `docs/` folder

---

**Built with ❤️ for sustainable agriculture and AI-powered plant health monitoring**
