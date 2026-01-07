import streamlit as st
from frontend.services.detection_service import detect_disease


def show_detection(image_file):
    st.subheader("🔍 Detection Result")

    try:
        result = detect_disease(image_file)
    except Exception as e:
        st.error(f"Detection failed: {e}")
        return None

    # 1️⃣ Annotated image
    st.image(
        result["output_image_path"],
        caption="Detected Leaf Diseases",
        use_container_width=True
    )

    report = result.get("report", {})

    primary = report.get("primary_diagnosis", "Unknown")
    severity = report.get("severity_level", "Unknown")
    alert = report.get("alert_type", "STANDARD")
    primary_conf = report.get("primary_confidence")

    # 2️⃣ High-level summary
    if alert == "EMERGENCY":
        st.error(f"🚨 **Primary Diagnosis:** {primary}")
    else:
        st.success(f"🌿 **Primary Diagnosis:** {primary}")

    if primary_conf is not None:
        st.markdown(f"**Primary Confidence:** `{primary_conf}%`")

    st.markdown(f"**Severity Level:** `{severity}`")

    # 3️⃣ Aggregated disease confidence (FIXED)
    st.markdown("### 🧬 Detected Conditions (Aggregated)")

    disease_summary = report.get("disease_confidence_summary", {})

    if not disease_summary:
        st.info("No disease symptoms detected. Plant appears healthy.")
    else:
        for label, stats in disease_summary.items():
            icon = "⚠️" if stats["is_priority"] else "🦠"

            st.markdown(
                f"""
                - {icon} **{label}**
                  - Max confidence: **{stats['max_confidence']}%**
                  - Mean confidence: **{stats['mean_confidence']}%**
                  - Detections: `{stats['detections']}`
                """
            )

    # 4️⃣ Co-infections
    co = report.get("co_infections", [])
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