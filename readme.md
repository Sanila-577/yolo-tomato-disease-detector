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
- Backend FastAPI server running (http://localhost:8000)
- All dependencies installed from `requirements.txt`

### Start Frontend

```bash
streamlit run app.py
```

**Frontend URL**: http://localhost:8501

---

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

### `state.py` - Session State Management

**Purpose**: Manage Streamlit session state and cross-refresh persistence

**Key Components**:

#### `_get_or_set_query_session_id()`

- Generates or retrieves stable session ID
- Stored in URL query params (`?sid=...`)
- Survives browser refresh without loss of state
- Returns: UUID hex string

#### `get_persistent_store()`

- Cached resource for in-memory store
- Dictionary keyed by session ID
- Persists data while app is running
- Returns: `Dict[str, Dict[str, Any]]`

#### `load_persisted_state(session_id)`

- Retrieves cached data for session
- Returns: `Optional[Dict]` with keys `detection_result` and `chat_history`
- Used on app initialization to restore previous state

#### `save_persisted_state(session_id, detection_result, chat_history)`

- Saves detection and chat data to cache
- Called after detection or each chat message
- Enables state recovery on page refresh

#### `init_state()`

- Initializes all required session state variables
- Sets defaults for new sessions
- Called at app startup in `app.py`

**State Variables Managed**:

| Variable             | Type        | Purpose                            |
| -------------------- | ----------- | ---------------------------------- |
| `session_id`       | str         | Unique identifier for user session |
| `detected_disease` | str\| None  | Current detected disease           |
| `detection_result` | dict\| None | Full detection API response        |
| `chat_history`     | list        | Chat message history               |

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

**Parameters**:

- `disease`: Detected disease name (passed from detection result)

**Process**:

1. Display subheader "Ask about the disease"
2. Initialize/retrieve chat history from session state
3. Render all previous messages using `st.chat_message()`
4. Provide input box with `st.chat_input()`
5. On user input:
   - Display user message immediately
   - Call `chat_backend()` API with session context
   - Display assistant response
   - Append to local chat history
   - Save state to persistent store

**Key Variables**:

- `history_key`: "chat_history" - session state key
- `session_id`: From session state
- `is_first`: Tracked per session+disease combo
- `detection_result`: Full report sent with first message

---

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

**Parameters**:

- `image_file`: Streamlit UploadedFile object
- `cached_result`: Previous detection result (for refresh)

**Process**:

1. Check if using cached result or new detection
2. If cached: render from cache without API call
3. If new: call `detect_disease()` API
4. Call `_render_detection()` helper
5. Return detection payload

**Helper Function**: `_render_detection(result: dict)`

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

- Backend URL: Retrieved from Streamlit secrets or defaults to `http://localhost:8000`
- Allows flexible deployment (dev/prod)

**Main Function**: `chat_backend(message, disease, session_id="default", report=None)`

**Parameters**:

- `message` (str): User's chat message
- `disease` (str): Detected disease name
- `session_id` (str): Session identifier for memory
- `report` (dict): Full detection report (sent with first message)

**Returns**: `Tuple[str, str]`

- `response`: Assistant's answer
- `stored_disease`: Confirmed disease from backend

**Process**:

1. Check if first message for this session+disease combo
2. Build JSON payload with:
   - User message
   - Detected disease context
   - Full detection report
   - Session ID
   - First message flag
3. POST to `/chat` endpoint
4. Handle HTTP errors and JSON decode errors
5. Return response data

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

- Backend URL: Retrieved from Streamlit secrets or defaults to `http://localhost:8000`
- Timeout: 30 seconds for image processing

**Main Function**: `detect_disease(image_file)`

**Parameters**:

- `image_file`: Streamlit UploadedFile object

**Returns**: `dict`

- Full detection API response

**Process**:

1. Extract image bytes from Streamlit UploadedFile
2. Get filename and content type
3. Build multipart form data
4. POST to `/detect` endpoint with 30-second timeout
5. Parse and return JSON response

**Multipart Form Data**:

```
--boundary
Content-Disposition: form-data; name="file"; filename="leaf.jpg"
Content-Type: image/jpeg

[binary image data]
--boundary--
```

**Returns Response Structure**:

```python
{
    "output_image_path": "http://localhost:8000/static/outputs/...",
    "detected_disease": "Late Blight",
    "report": {...}
}
```

**Error Handling**:

- HTTPError: Attempts to extract server error details
- ValueError: Reports JSON decode errors
- Timeout: Uses 30-second timeout to prevent hanging
- Comprehensive error messages for debugging

---

## 🔧 Configuration

### Streamlit Secrets (`secrets.toml`)

Create `.streamlit/secrets.toml` in project root:

```toml
BACKEND_URL = "http://localhost:8000"  # Development
# BACKEND_URL = "http://production-api.example.com"  # Production
```

### Streamlit Configuration (`config.toml`)

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[client]
showErrorDetails = true
maxUploadSize = 200  # MB

[server]
maxUploadSize = 200
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

## 🎯 Session Management

### Session ID Generation

- UUID generated on first visit
- Stored in URL query params (`?sid=abc123...`)
- Survives browser refresh
- Persists per browser/tab

### State Persistence

- Uses `@st.cache_resource` for in-memory store
- Keyed by session ID
- Stores: detection results + chat history
- Resets when app restarts

### First Message Tracking

- Tracks `api_session_{session_id}_{disease}`
- Triggers context injection to backend
- Resets when disease changes

---

## 🚨 Error Handling

### Detection Errors

```python
try:
    result = detect_disease(image_file)
except Exception as e:
    st.error(f"Detection failed: {e}")
    return None
```

- Shows user-friendly error message
- Returns None (graceful failure)

### Chat Errors

```python
res.raise_for_status()  # HTTPError
res.json()              # JSONDecodeError
```

- HTTP errors: Extract response details
- JSON errors: Report invalid response
- Displayed via Streamlit warning/error widgets

### Image Upload Errors

- Validates file type (JPG/PNG/JPEG)
- Streamlit handles file size limits
- Content-type auto-detection

---

## 🔐 Security Considerations

1. **API URL Configuration**: Use environment secrets, not hardcoded
2. **File Upload**: Streamlit handles file validation (type, size)
3. **Session Isolation**: Each session ID is isolated
4. **CORS**: Backend should validate origin (if needed)
5. **Timeout**: 30-second timeout prevents hanging requests
6. **Error Details**: Production should hide technical error details

---

## 🎨 Styling & Customization

### Color Scheme

- Primary: Blue (`#1f77b4`)
- Background: White
- Secondary: Light Gray (`#f0f2f6`)
- Text: Dark Gray (`#262730`)

### Customization

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#YOUR_COLOR"
backgroundColor = "#YOUR_COLOR"
```

### Markdown Features

- Uses Streamlit markdown for formatted text
- Emoji support: 🌱 🔍 💬 🚨 ⚠️ ✅
- Expandable sections with `st.expander()`
- Error/Warning/Info messages with `st.error()`, `st.warning()`, `st.info()`

---

## 🧪 Testing the Frontend

### Test Detection Upload

```python
# Use a real tomato leaf image
# Should see:
# - Annotated image
# - Disease name
# - Confidence > 0%
# - Treatment advice
```

### Test Chat Interaction

```python
# After detection, ask:
# - "What causes [disease]?"
# - "How do I treat it?"
# - "Prevention tips?"
# - Casual questions
```

### Test Session Persistence

```python
# 1. Upload image + chat
# 2. Refresh page (F5)
# Expected: Previous detection and chat history restored
```

### Test Fallback Behavior

```python
# Ask out-of-domain question in chat
# Expected: Router → web agent → answer from web search
```

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

### Production (Docker)

See `Dockerfile` for containerized deployment

### Secrets Management

- `.streamlit/secrets.toml`: Local secrets (git-ignored)
- Production: Use Streamlit Cloud secrets or environment variables

### Backend URL Configuration

- Development: `http://localhost:8000`
- Production: Use secrets file or environment variable

---

## 🐛 Troubleshooting

### Issue: "Connection refused" (Backend not running)

**Solution**: Start FastAPI backend: `fastapi dev ./api/main.py`

### Issue: Images not displaying

**Solution**: Check backend `/static` mount in `api/main.py`

### Issue: Chat history disappears on refresh

**Solution**: Verify session ID in URL (`?sid=...`)

### Issue: Detection timeout

**Solution**: Check backend, increase timeout in `detection_service.py`

### Issue: API 500 errors

**Solution**: Check backend logs for LLM/FAISS errors

---

## 🔄 Future Enhancements

- [ ] Multi-image comparison
- [ ] Chat export as PDF report
- [ ] Disease progression timeline
- [ ] Real-time webcam detection
- [ ] Multiple disease profiles in single session
- [ ] Dark mode support
- [ ] Mobile-optimized responsive design
- [ ] Voice input for chat
- [ ] Downloadable treatment guides
- [ ] Share chat history/reports feature

---

## 📚 References

- Streamlit Docs: https://docs.streamlit.io/
- Session State: https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
- File Uploader: https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader

---

**Last Updated**: January 9, 2026
**Maintained by**: Neuro Leaf Development Team
