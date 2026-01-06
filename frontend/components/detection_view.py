import streamlit as st
from frontend.services.detection_service import detect_disease

def show_detection(image_file):
    st.subheader("🔍 Detection Result")

    try:
        result = detect_disease(image_file)
    except Exception as e:
        st.error(f"Detection failed: {e}")
        return None

    # Overlay bounding boxes image
    st.image(result["output_image_path"], caption="Detected Diseases")

    # Summary Bar
    report = result.get("report") or {}
    primary = report.get("primary_diagnosis", result.get("detected_disease"))
    severity = report.get("severity_level", "")
    issues_summary = report.get("issues_detected_summary", "")

    st.info(f"{issues_summary}")

    with st.expander("Disease Report Card", expanded=True):
        st.markdown(f"- Primary Diagnosis: **{primary}**")
        st.markdown(f"- Severity Level: **{severity}**")
        co = report.get("co_infections") or []
        if co:
            st.markdown("- Co-Infections:")
            for item in co:
                st.markdown(f"  - {item}")
        else:
            st.markdown("- Co-Infections: None detected")
        st.markdown(f"- Immediate Action: {report.get('immediate_action', '')}")
        st.markdown(f"- Confidence Level: {report.get('confidence_level', '')}")

    st.success(f"Detected: {primary}")

    return primary
