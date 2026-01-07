import streamlit as st
from frontend.state import (
    init_state,
    load_persisted_state,
    save_persisted_state,
)
from frontend.components.chat_ui import chat_ui
from frontend.components.detection_view import show_detection

# ----------------------------
# App Config
# ----------------------------
st.set_page_config(
    page_title="Tomato Plant Disease Detection",
    layout="wide"
)

# ----------------------------
# Initialize State
# ----------------------------
init_state()

persisted = load_persisted_state(st.session_state.session_id)
if persisted and not st.session_state.get("detection_result"):
    st.session_state["detection_result"] = persisted.get("detection_result")
    st.session_state["chat_history"] = persisted.get("chat_history", [])
    if st.session_state.get("detection_result"):
        st.session_state["detected_disease"] = (
            st.session_state["detection_result"].get("detected_disease")
            or (st.session_state["detection_result"].get("report", {}) or {}).get("primary_diagnosis")
        )


# # ----------------------------
# # Load CSS + Set Theme on Body
# # ----------------------------
# css_file = Path("frontend/styles/theme.css")
# css_content = css_file.read_text() if css_file.exists() else ""

# st.markdown(
#     f"""
#     <style>
#     {css_content}
#     </style>

#     <script>
#     (function() {{
#         const saved = localStorage.getItem("theme_mode") || "{st.session_state.theme_mode}";
#         document.body.setAttribute("data-theme", saved);
#     }})();
#     </script>
#     """,
#     unsafe_allow_html=True
# )

# # ----------------------------
# # Theme Toggle Button UI
# # ----------------------------
# col1, col2 = st.columns([8, 1])
# with col2:
#     icon = "🌙" if st.session_state.theme_mode == "light" else "☀️"
#     if st.button(icon, key="theme_toggle", help="Toggle theme"):
#         new_mode = "dark" if st.session_state.theme_mode == "light" else "light"
#         st.session_state.theme_mode = new_mode

#         # Sync to browser localStorage + force page rerender
#         st.markdown(
#             f"""
#             <script>
#             localStorage.setItem("theme_mode", "{new_mode}");
#             document.body.setAttribute("data-theme", "{new_mode}");
#             window.location.reload();
#             </script>
#             """,
#             unsafe_allow_html=True
#     )

# ----------------------------
# App Title
# ----------------------------
st.title("Tomato Leaf Disease Detection")

# ----------------------------
# File Upload / Detection
# ----------------------------
uploaded_image = st.file_uploader(
    "Upload a tomato leaf image",
    type=["jpg", "png", "jpeg"]
)

if uploaded_image:
    detection_result = show_detection(image_file=uploaded_image)

    if detection_result:
        detected_disease = (
            detection_result.get("detected_disease")
            or (detection_result.get("report", {}) or {}).get("primary_diagnosis")
        )

        # Save detection + reset chat
        st.session_state["detected_disease"] = detected_disease
        st.session_state["detection_result"] = detection_result

        save_persisted_state(
            st.session_state.session_id,
            st.session_state["detection_result"],
            st.session_state["chat_history"],
        )

        chat_ui(detected_disease)

elif st.session_state.get("detection_result"):
    # Rehydrate UI if refresh happens
    detection_result = st.session_state["detection_result"]
    detected_disease = (
        detection_result.get("detected_disease")
        or (detection_result.get("report", {}) or {}).get("primary_diagnosis")
    )

    show_detection(cached_result=detection_result)

    if detected_disease:
        st.session_state["detected_disease"] = detected_disease
        save_persisted_state(
            st.session_state.session_id,
            st.session_state["detection_result"],
            st.session_state["chat_history"],
        )

        chat_ui(detected_disease)