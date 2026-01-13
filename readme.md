# 🎨 Neuro Leaf Frontend - Streamlit UI Documentation

## Overview

The frontend is a modern, interactive Streamlit application that provides users with an intuitive interface for tomato leaf disease detection and AI-powered guidance. It features real-time image upload, disease detection visualization, and multi-turn conversational chat with session persistence.

---

## 📁 Frontend Directory Structure

```
/
├── app.py                  # Main Streamlit application entry point
├── state.py                # Session state management & persistence
├── components/
│   ├── chat_ui.py          # Chat interface component
│   └── detection_view.py   # Detection results visualization
├── services/
│   ├── chat_service.py     # Chat API client
│   └── detection_service.py # Detection API client
└── __init__.py
```

---

## 🚀 Running the Frontend

### Prerequisites

- Python 3.10+
- Virtual environment activated
- Backend FastAPI server running (deployed in hugging face spaces at [https://sanila-wijesekara-neuro-leaf-backend.hf.space](https://sanila-wijesekara-neuro-leaf-backend.hf.space) )
- All dependencies installed from `requirements.txt`

### Start Frontend

```bash
streamlit run app.py
```

**Frontend URL**: [https://neuroleaf.streamlit.app/](https://neuroleaf.streamlit.app/)

## 📊 File Documentation

### `app.py` - Main Application

**Purpose**: Entry point for the Streamlit application

**Key Features**:

- Page configuration (title, layout)
- Session state initialization
- File uploader for leaf images
- Integration of detection and chat components
- Persistent state management across page refreshes

**Workflow**:

1. Initialize Streamlit page with "Neuro Leaf" title
2. Load persisted state (if available) from cache
3. Display file uploader for JPG/PNG/JPEG images
4. On file upload: call `show_detection()` to display results
5. If disease detected: pass to `chat_ui()` component
6. On page refresh: restore previous detection and chat history

**Key Functions**:

```python
def init_state()                      # Initialize session variables
def load_persisted_state(session_id)  # Load cached data
def save_persisted_state(...)         # Save data to cache
```

**Session Variables Used**:

- `session_id`: Unique ID for user session (UUID)
- `detected_disease`: Disease name from detection
- `detection_result`: Full detection API response
- `chat_history`: List of chat messages

---

### `components/chat_ui.py` - Chat Interface

**Purpose**: Display and manage chat interaction with disease context

**Key Features**:

- Chat message display (user/assistant)
- Chat input box for user messages
- Real-time message rendering
- Session memory integration
- First message tracking for context injection

**Main Function**: `chat_ui(disease: str)`

### `components/detection_view.py` - Detection Visualization

**Purpose**: Display disease detection results with structured information

**Key Features**:

- Annotated image display with bounding boxes
- Primary diagnosis with severity level
- Emergency alert handling (Late Blight)
- Disease confidence breakdown
- Co-infection detection
- Treatment recommendations
- Result caching for refresh handling

**Main Function**: `show_detection(image_file=None, cached_result=None)`

**Renders** (in order):

1. **Annotated Image**: Displays image with bounding boxes
2. **Primary Diagnosis**: Disease name with severity level
3. **Alert Level**: Shows 🚨 EMERGENCY icon for high-priority diseases
4. **Confidence Score**: Primary detection confidence percentage
5. **Disease Summary**: Table of all detected diseases with:
   - Priority icon (⚠️ for high-priority, 🦠 for others)
   - Max confidence percentage
   - Mean confidence percentage
   - Number of detections
6. **Co-infections**: List of multiple diseases detected simultaneously
7. **Treatment Advice**: Expandable section with recommended actions

**Example Detection Result Structure**:

```python
{
    "output_image_path": "http://localhost:8000/static/outputs/...",
    "detected_disease": "Late Blight",
    "report": {
        "primary_diagnosis": "Late Blight",
        "severity_level": "High",
        "alert_type": "EMERGENCY",
        "primary_confidence": 95,
        "disease_confidence_summary": {
            "Late_blight": {
                "max_confidence": 95,
                "mean_confidence": 92,
                "detections": 3,
                "is_priority": True
            },
            "Early_Blight": {
                "max_confidence": 45,
                "mean_confidence": 40,
                "detections": 2,
                "is_priority": False
            }
        },
        "co_infections": ["Late Blight", "Early Blight"],
        "treatment_steps": "EMERGENCY: Remove and destroy infected plants..."
    }
}
```

---

### `services/chat_service.py` - Chat API Client

**Purpose**: Handle HTTP communication with backend `/chat` endpoint

**Configuration**:

- Backend URL: Retrieved from Streamlit secrets or defaults to `http://localhost:8000` (for local development)
- Production URL: `https://sanila-wijesekara-neuro-leaf-backend.hf.space`
- Allows flexible deployment (dev/prod)

**Main Function**: `chat_backend(message, disease, session_id="default", report=None)`

**Payload Structure**:

```python
{
    "message": "How do I treat late blight?",
    "detected_disease": "Late Blight",
    "report": {...full report dict...},
    "session_id": "abc123def456",
    "is_first_message": True  # First message triggers context injection
}
```

**Error Handling**:

- HTTPError: Logs server-side error details
- JSONDecodeError: Reports invalid API response
- Includes error messages for debugging

---

### `services/detection_service.py` - Detection API Client

**Purpose**: Handle HTTP communication with backend `/detect` endpoint

**Configuration**:

- Backend URL: Retrieved from Streamlit secrets or defaults to `http://localhost:8000` (for local development)
- Production URL: `https://sanila-wijesekara-neuro-leaf-backend.hf.space`

**Main Function**: `detect_disease(image_file)`

**Returns Response Structure**:

```python
{
    "output_image_path": "http://localhost:8000/static/outputs/...",
    "detected_disease": "Late Blight",
    "report": {...}
}
```

## 🔧 Configuration

### Streamlit Secrets (`secrets.toml`)

Create `.streamlit/secrets.toml` in project root:

```toml
# Production (Deployed on Streamlit Cloud)
BACKEND_URL = "https://sanila-wijesekara-neuro-leaf-backend.hf.space"

# Development (Local)
# BACKEND_URL = "http://localhost:8000"
```

---

## 🔄 Data Flow

### Detection Flow

```
User uploads image (JPG/PNG)
    ↓
Streamlit UploadedFile object
    ↓
app.py: show_detection(image_file)
    ↓
detection_view.py: detect_disease(image_file)
    ↓
detection_service.py: POST /detect (multipart form)
    ↓
FastAPI Backend: YOLO inference + report generation
    ↓
API Response: {output_image_path, detected_disease, report}
    ↓
detection_view.py: _render_detection(result)
    ↓
Streamlit UI displays:
  - Annotated image
  - Disease diagnosis
  - Severity & confidence
  - Treatment advice
    ↓
Detection result saved to session state
```

### Chat Flow

```
User types message in chat_ui
    ↓
chat_ui.py: chat_backend(message, disease, session_id)
    ↓
chat_service.py: POST /chat (JSON)
    ↓
Payload includes:
  - User message
  - Detected disease context
  - Full detection report (first message only)
  - Session ID
  - is_first_message flag
    ↓
FastAPI Backend: LangGraph agent routing
  - Router: Classifies intent (chat/rag/web)
  - Routes to appropriate agent
  - Grader evaluates RAG sufficiency
  - Fallback to web if needed
    ↓
API Response: {answer, detected_disease}
    ↓
chat_ui.py displays response
    ↓
Both messages added to chat_history
    ↓
State saved to persistent store
```

---

## 📱 UI Components & Layout

### Page Layout

- **Mode**: Wide (allows side-by-side layouts)
- **Title**: "Neuro Leaf"
- **Logo/Branding**: Leaf emoji 🌱

### Main Sections

1. **Upload Section**

   - File uploader (JPG/PNG/JPEG)
   - Drag-and-drop support
   - Inline instructions
2. **Detection Results Section**

   - Annotated image with bounding boxes
   - Disease diagnosis card
   - Severity indicator
   - Confidence scores
   - Co-infections list
   - Treatment expander
3. **Chat Section**

   - Chat history display
   - User/Assistant message differentiation
   - Chat input box
   - Real-time message streaming

---

## 📦 Dependencies

**Streamlit Framework**:

- `streamlit`: UI framework

**API Communication**:

- `requests`: HTTP client for backend APIs

**State Management**:

- Built-in Streamlit session state (`st.session_state`)
- Custom caching with `@st.cache_resource`

See `requirements.txt` for full dependency list.

---

## 🚀 Deployment

### Development

```bash
streamlit run app.py
```

### Production

**Frontend**: Deployed on [Streamlit Cloud](https://streamlit.io/cloud)

**Backend**: Deployed on [Hugging Face Spaces](https://huggingface.co/spaces)

- Backend URL: `https://sanila-wijesekara-neuro-leaf-backend.hf.space`

### Docker Deployment

See `Dockerfile` for containerized deployment

### Secrets Management

- `.streamlit/secrets.toml`: Local secrets (git-ignored)
- Production: Use Streamlit Cloud secrets dashboard
- Backend URL: Configure in Streamlit Cloud secrets as `BACKEND_URL = "https://sanila-wijesekara-neuro-leaf-backend.hf.space"`

### Backend URL Configuration

- Development: `http://localhost:8000`
- Production: `https://sanila-wijesekara-neuro-leaf-backend.hf.space` (configured in Streamlit Cloud)

---

---

## 📚 References

- Streamlit Docs: https://docs.streamlit.io/
- Session State: https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
- File Uploader: https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader
