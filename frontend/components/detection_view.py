import base64
from io import BytesIO
from typing import Optional, Dict

import streamlit as st
from frontend.services.detection_service import detect_disease

def _render_detection(result: dict) -> str:
    """Render detection details and return the detected disease name."""
    
    # 1️⃣ Image Handling (Base64)
    image_data = result.get("output_image_path")  # The "data:image/jpeg;base64,..." string
    
    if image_data:
        # Streamlit natively displays Base64 data URLs
        st.image(
            image_data,
            caption="AI Annotated Result",
            width=420,
            use_container_width=False,
        )
        
        # 📥 Download Button Logic
        try:
            # We extract the raw base64 string by removing the metadata prefix
            if "base64," in image_data:
                header, encoded = image_data.split(",", 1)
                binary_data = base64.b64decode(encoded)
                
                st.download_button(
                    label="📥 Download Annotated Image",
                    data=binary_data,
                    file_name="vinedoc_detection.jpg",
                    mime="image/jpeg",
                    use_container_width=False
                )
        except Exception as e:
            st.error(f"Could not generate download link: {e}")

    # --- 2️⃣ Diagnosis & Report Logic ---
    report = result.get("report", {}) or {}

    primary = (
        result.get("detected_disease")
        or report.get("primary_diagnosis")
        or "Unknown"
    )
    severity = report.get("severity_level", "Unknown")
    alert = report.get("alert_type", "STANDARD")
    primary_conf = report.get("primary_confidence")

    # High-level summary
    if alert == "EMERGENCY":
        st.error(f"🚨 **Primary Diagnosis:** {primary}")
    else:
        st.success(f"🌿 **Primary Diagnosis:** {primary}")

    if primary_conf is not None:
        st.markdown(f"**Primary Confidence:** `{primary_conf}%`")

    st.markdown(f"**Severity Level:** `{severity}`")

    # 3️⃣ Aggregated disease confidence
    st.markdown("### 🧬 Detected Diseases")
    disease_summary = report.get("disease_confidence_summary", {}) or {}

    if not disease_summary:
        st.info("No disease symptoms detected. Plant appears healthy.")
    else:
        for label, stats in disease_summary.items():
            icon = "⚠️" if stats.get("is_priority") else "🦠"
            st.markdown(
                f"""
                - {icon} **{label}**
                  - Max confidence: **{stats.get('max_confidence', 'N/A')}%**
                  - Mean confidence: **{stats.get('mean_confidence', 'N/A')}%**
                  - Detections: `{stats.get('detections', 'N/A')}`
                """
            )

    # 4️⃣ Co-infections
    co = report.get("co_infections", []) or []
    if co:
        st.warning("⚠️ **Co-Infections Detected:**")
        for disease in co:
            st.markdown(f"- {disease}")
    else:
        st.markdown("✅ **No co-infections detected**")

    # 5️⃣ Treatment advice
    with st.expander("💊 Recommended Action", expanded=True):
        st.info(report.get("treatment_steps", "No recommendation available."))

    return primary


def show_detection(
    image_file=None,
    cached_result: Optional[Dict] = None,
) -> Optional[Dict]:
    """Run or render detection and return the detection payload."""
    st.subheader("🔍 Detection Result")

    if cached_result is not None:
        # Use the cached payload without re-calling the API
        _render_detection(cached_result)
        return cached_result

    if image_file is None:
        st.warning("Please upload an image to start detection.")
        return None

    try:
        # This calls your frontend/services/detection_service.py
        result = detect_disease(image_file)
    except Exception as e:
        st.error(f"Detection failed: {e}")
        return None

    _render_detection(result)
    return result