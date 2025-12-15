# 🌱 Plant RAG Chatbot (LangGraph + FAISS + Streamlit)

An intelligent Retrieval-Augmented Generation (RAG) chatbot for answering plant-related questions using PDF knowledge, web search fallback, and multi-agent reasoning built with LangGraph, LangChain, FAISS, and Streamlit.

---

## 🚀 Features
- 🧠 Multi-Agent Architecture (LangGraph)
- Router Agent (Chat / RAG / Web)
- RAG Agent (FAISS Vector Search)
- Web Agent (Tavily Search)
- Grader Agent (Context relevance checking)
- 📚 RAG over PDFs from `context/`
- FAISS for semantic similarity search
- HuggingFace embeddings (`all-MiniLM-L6-v2`)
- 🌐 Web Search Fallback (Tavily)
- 💬 Conversational memory with LangChain messages
- 🖥️ Streamlit UI
🌱 Plant RAG Chatbot (LangGraph + FAISS + Streamlit)
---

## 📁 Project Structure

```
RAG-chatbot/
├─ context/                     # PDF documents for RAG
├─ faiss_db/                    # Persistent FAISS index storage
│  └─ index.faiss               # Auto-generated on first run
├─ agents/                      # Agent logic
│  ├─ router_agent.py
│  ├─ chat_agent.py
│  ├─ retriever_agent.py
│  ├─ web_agent.py
│  └─ grader_answer_agent.py
├─ tools/                       # Tool definitions
│  ├─ retriever_tool.py
│  └─ tavily_search_tool.py
├─ core/                        # Graph construction and execution
│  ├─ build_graph.py
│  ├─ faiss_setup.py
│  ├─ llm.py
│  └─ run_agent.py
├─ streamlit_app.py             # Streamlit frontend
├─ requirements.txt
├─ .env                         # Create this
└─ readme.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone or open the project
If cloning from Git:

```bash
git clone <your-repo-url>
cd RAG-chatbot
```

### 2️⃣ Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows (PowerShell)
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Environment Variables
Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Notes:
- LLM configured via OpenRouter in `core/llm.py` using model `openai/gpt-4o-mini`.
- Tavily is used for web search fallback; an API key is required.

---

## 📚 PDF Knowledge Base
- Place your plant-related PDFs inside `context/`.
- On first run, FAISS embeddings are created automatically from PDFs using `all-MiniLM-L6-v2`.
- Subsequent runs load the vector store from `faiss_db/` (no re-embedding).

---

## ▶️ Running the Application

### 🖥️ Streamlit UI (Recommended)
```bash
streamlit run streamlit_app.py
```
Open: http://localhost:8501

### 💻 Terminal Version (Optional)
```bash
python -m core.run_agent
```

---

## 🧠 How It Works

### 1️⃣ Router Agent
Classifies the query into:
- `chat` → casual conversation
- `rag` → plant knowledge from PDFs
- `web` → general knowledge via Tavily

### 2️⃣ RAG Agent
- Uses FAISS to retrieve relevant document chunks
- Calls the retriever tool
- Stores retrieved content for grading

### 3️⃣ Grader + Answer
- Evaluates whether retrieved context fully answers the question
- If insufficient, triggers web fallback
- If sufficient, generates final answer

### 4️⃣ Web Agent (Fallback)
- Uses Tavily search for live web information
- Returns answers when local knowledge is insufficient

---

## 🧪 Tech Stack
- LangGraph – Multi-agent workflow orchestration
- LangChain – Tool calling & message handling
- FAISS – Vector similarity search
- HuggingFace Embeddings (`all-MiniLM-L6-v2`)
- OpenRouter (model: `openai/gpt-4o-mini`)
- Tavily API – Web search
- Streamlit – Frontend UI

---

## ✅ Example Queries
- What are common tomato plant diseases?
- How to treat leaf curl in tomatoes?
- What is nitrogen deficiency in plants?
- Hello!
- Latest research on plant fungal infections

---

## 🔒 Notes
- FAISS index persists between runs (stored in `faiss_db/`)
- Chat memory resets on Streamlit refresh
- Designed for modular expansion (tools, agents, memory)

## 🛠️ Troubleshooting
- If FAISS build fails, ensure PDFs exist in `context/` and retry.
- If OpenRouter requests fail, check `OPENROUTER_API_KEY` and network access.
- For Tavily errors, verify `TAVILY_API_KEY` and reduce `max_results` in `tools/tavily_search_tool.py` if rate limited.

---

## 🧑‍💻 Author
Built with ❤️ using LangGraph + RAG. Feel free to fork, extend, and deploy 🚀

---

## Extras
If you want, I can also:
- Add architecture diagrams
- Write deployment instructions (Docker / AWS)
- Add example screenshots
- Convert this into a research-grade README

An intelligent Retrieval-Augmented Generation (RAG) chatbot for answering plant-related questions using PDF knowledge, web search fallback, and multi-agent reasoning built with LangGraph, LangChain, FAISS, and Streamlit.

⸻

🚀 Features
	•	🧠 Multi-Agent Architecture (LangGraph)
	•	Router Agent (Chat / RAG / Web)
	•	RAG Agent (FAISS Vector Search)
	•	Web Agent (Tavily Search)
	•	Grader Agent (Context relevance checking)
	•	📚 RAG over PDFs
	•	Loads plant-related PDFs from context/
	•	Uses FAISS for semantic similarity search
	•	HuggingFace embeddings (all-MiniLM-L6-v2)
	•	🌐 Web Search Fallback
	•	Automatically falls back to Tavily web search when local context is insufficient
	•	💬 Conversational Memory
	•	Maintains multi-turn conversation using LangChain message objects
	•	🖥️ Streamlit UI
	•	Interactive chat interface
	•	Session-based memory
	•	Clean user/bot message separation

⸻

📁 Project Structure

rag_chatbot/
│
├─ context/                     # PDF documents for RAG
│   ├─ tomato_diseases.pdf
│   └─ plant_guide.pdf
│
├─ faiss_db/                    # Persistent FAISS index storage
│   └─ (FAISS files auto-generated)
│
├─ agents/                      # Agent logic
│   ├─ router_agent.py
│   ├─ chat_agent.py
│   ├─ retriever_agent.py
│   ├─ web_agent.py
│   └─ grader_agent.py
│
├─ tools/                       # Tool definitions
│   ├─ retriever_tool.py
│   └─ tavily_search_tool.py
│
├─ core/                        # Graph construction and execution
│   ├─ build_graph.py
│   └─ run_agent.py
│
├─ streamlit_app.py             # Streamlit frontend
├─ requirements.txt
├─ .env
└─ README.md


⸻

⚙️ Setup Instructions

1️⃣ Clone the repository

git clone https://github.com/your-username/rag-chatbot.git
cd rag-chatbot


⸻

2️⃣ Create and activate a virtual environment

python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows


⸻

3️⃣ Install dependencies

pip install -r requirements.txt


⸻

4️⃣ Environment Variables

Create a .env file in the root directory:

OPENROUTER_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key


⸻

📚 PDF Knowledge Base
	•	Place your plant-related PDFs inside the context/ folder.
	•	On first run, FAISS embeddings are created automatically.
	•	On subsequent runs, the vector store is loaded from faiss_db/ (no re-embedding).

⸻

▶️ Running the Application

🖥️ Streamlit UI (Recommended)

streamlit run streamlit_app.py

Then open:

http://localhost:8501


⸻

💻 Terminal Version (Optional)

python core/run_agent.py


⸻

🧠 How It Works

1️⃣ Router Agent

Determines whether the query is:
	•	chat → casual conversation
	•	rag → plant knowledge from PDFs
	•	web → general knowledge via Tavily

⸻

2️⃣ RAG Agent
	•	Uses FAISS to retrieve relevant document chunks
	•	Calls retriever tool dynamically
	•	Stores retrieved content for grading

⸻

3️⃣ Grader Agent
	•	Evaluates whether retrieved context fully answers the question
	•	If insufficient, triggers web fallback
	•	If sufficient, generates final answer

⸻

4️⃣ Web Agent (Fallback)
	•	Uses Tavily search for live web information
	•	Returns answers when local knowledge is insufficient

⸻

🧪 Tech Stack
	•	LangGraph – Multi-agent workflow orchestration
	•	LangChain – Tool calling & message handling
	•	FAISS – Vector similarity search
	•	HuggingFace Embeddings
	•	OpenRouter (GPT-4o-mini)
	•	Tavily API – Web search
	•	Streamlit – Frontend UI

⸻

✅ Example Queries
	•	What are common tomato plant diseases?
	•	How to treat leaf curl in tomatoes?
	•	What is nitrogen deficiency in plants?
	•	Hello!
	•	Latest research on plant fungal infections

⸻

🔒 Notes
	•	FAISS index persists between runs
	•	Chat memory resets on Streamlit refresh
	•	Designed for modular expansion (tools, agents, memory)

⸻

📌 Future Enhancements
	•	🔁 Streaming responses
	•	🧠 Conversation summarization memory
	•	🗂️ Multi-collection FAISS support
	•	☁️ Cloud deployment
	•	📊 Source citation UI

⸻

🧑‍💻 Author

Built with ❤️ using LangGraph + RAG
Feel free to fork, extend, and deploy 🚀

⸻

If you want, I can also:
	•	Add architecture diagrams
	•	Write deployment instructions (Docker / AWS)
	•	Add example screenshots
	•	Convert this into a research-grade README

Just tell me 👍