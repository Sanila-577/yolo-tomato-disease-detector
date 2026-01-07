import streamlit as st
import uuid
from typing import Optional, Dict, Any


def _get_or_set_query_session_id() -> str:
    """Get a stable session id that survives browser refresh via query params."""
    params = st.query_params
    existing = params.get("sid")
    if existing:
        return existing[0] if isinstance(existing, list) else existing

    sid = uuid.uuid4().hex
    st.query_params["sid"] = sid
    return sid


@st.cache_resource
def get_persistent_store() -> Dict[str, Dict[str, Any]]:
    """Process-wide cache keyed by sid; keeps data across refresh while app runs."""
    return {}


def load_persisted_state(session_id: str) -> Optional[Dict[str, Any]]:
    store = get_persistent_store()
    return store.get(session_id)


def save_persisted_state(session_id: str, detection_result: Any, chat_history: Any) -> None:
    store = get_persistent_store()
    store[session_id] = {
        "detection_result": detection_result,
        "chat_history": chat_history,
    }


def init_state():
    """Initialize shared Streamlit session state with sensible defaults."""
    if "session_id" not in st.session_state:
        # Stable session identifier for backend chat memory and local cache
        st.session_state.session_id = _get_or_set_query_session_id()

    if "detected_disease" not in st.session_state:
        st.session_state.detected_disease = None

    if "detection_result" not in st.session_state:
        # Holds the full detection payload returned by the API
        st.session_state.detection_result = None

    if "chat_history" not in st.session_state:
        # Local chat transcript used to redraw the UI without extra API calls
        st.session_state.chat_history = []