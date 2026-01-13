# 🌱 Neuro Leaf: Tomato Leaf Disease Assistant

A production-ready AI system combining computer vision and conversational AI for tomato leaf disease diagnosis and treatment guidance. Built with FastAPI backend, LangGraph agentic workflow, and Streamlit frontend.

Check this out: https://neuroleaf.streamlit.app/

Kaggle model training notebook: 

https://www.kaggle.com/code/sanilawijesekara/tomato-leaf-disease-detection-yolov11-eda

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

Backend deployed in hugging face spaces at https://sanila-wijesekara-neuro-leaf-backend.hf.space

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

## 📚 References & Citations

### Research Papers (in context/)

The knowledge base contains 10 research papers covering major tomato leaf diseases:

#### Late Blight (2 papers)

1. **Late Blight of Tomato** - Kelly Ivors

   - File: `late_blight1.pdf`
   - Focus: Pathogen biology and management strategies for *Phytophthora infestans*
   - Key topics: Host crops, disease transmission, cultural and fungicide control
2. **Late Blight Fact Sheet** - WVU Extension Service

   - File: `late_blight2.pdf`
   - Focus: Practical control methods and disease basics
   - Key topics: Disease spread from infected plants, prevention strategies

#### Early Blight (2 papers)

3. **Early Blight Control Guide** - Sharon M. Douglas, CAES

   - File: `early_blight1.pdf`
   - Focus: Symptom identification and management approaches
   - Key topics: Concentric lesions on leaves and fruit, disease progression
4. **Tomato Early Blight** - Gearhart & Sunshine (CMG GardenNotes #718)

   - File: `early_blight2.pdf`
   - Focus: Comprehensive management guide for home and commercial growers
   - Key topics: Caused by *Alternaria solani* and *Alternaria tomatophila*; management practices including spacing, mulching, rotation, and fungicide options

#### Bacterial Spot (2 papers)

5. **Bacterial Spot of Tomato and Pepper** - Xiaoan Sun, Misty C. Nielsen, John W. Miller

   - File: `bacterial_spot1.pdf`
   - Source: Florida Department of Agriculture & Consumer Services, Plant Pathology Circular No. 129 (Revised, April/May 2002)
   - Focus: Disease caused by *Xanthomonas* spp. and its management
   - Key topics: Serious disease on tomato and pepper worldwide, destructive to seedlings
6. **Bacterial Spot of Tomato** - Dr. Yonghao Li, CAES

   - File: `bacterial_spot2.pdf`
   - Source: Connecticut Agricultural Experiment Station
   - Focus: Visual identification and management strategies
   - Key topics: Brown spots with yellow halos on leaves, symptoms on stems and petioles

#### Leaf Mold (1 paper)

7. **Leaf Mold in High Tunnel Tomatoes** - ClintonED
   - File: `leaf_mold1.pdf`
   - Focus: Disease management in controlled greenhouse environments
   - Key topics: Caused by *Fulvia fulva* (formerly *Cladosporium fulvum*); favored by high humidity; rapid plant-to-plant spread; severe defoliation and yield reduction

#### Target Spot (3 papers)

8. **Target Spot of Tomato** - Seminis (Agronomic Spotlight)

   - File: `9068_SE_S9_Target-Spot-of-Tomato.pdf`
   - Focus: Disease overview and management in tropical/subtropical regions
   - Key topics: Caused by *Corynespora cassiicola*; important disease in warm climates; symptoms may resemble bacterial spot and early blight
9. **Tomato Target Spot** - FAO Fact Sheet #163

   - File: `target_spot1.pdf`
   - Focus: Global distribution and control strategies
   - Key topics: Widespread in tropical regions; rapid leaf damage in wet weather; wind-driven rain spore dispersal; cultural control measures
10. **Climate Change Impacts on Paddy Yields in Sri Lanka** - Chamila Kumari Chandrasiri et al.

    - File: `s41685-022-00264-5.pdf`
    - Source: Asia-Pacific Journal of Regional Science (2023) 7:455–489
    - Focus: Environmental factors affecting crop yields
    - Key topics: Regional climate variations and agricultural productivity; relevant context for disease management under changing environmental conditions

#### Knowledge Base Statistics

- **Total documents**: 10 PDFs
- **Embedding model**: HuggingFace `all-MiniLM-L6-v2` (384 dimensions)
- **Vector store**: FAISS with k=4 default retrieval
- **Coverage**: 7 disease classes (Late Blight, Early Blight, Bacterial Spot, Leaf Mold, Target Spot, Black Spot, Healthy)
- **Focus**: Primarily academic and extension service publications from US institutions and industry sources

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

MIT License - See LICENSE file for details

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
- Email: [sanilamethwan@gmail.com]
- Documentation: See `docs/` folder

---

**Built with ❤️ for sustainable agriculture and AI-powered plant health monitoring**
