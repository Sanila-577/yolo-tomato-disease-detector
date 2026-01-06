import streamlit as st
from frontend.services.detection_service import detect_disease

def show_detection(image_file):
    st.subheader("🔍 Detection Result")

    result = detect_disease(image_file)
    st.write(result)

    # Correct keys
    st.image(result["output_image_path"], caption="Detected Diseases")
    st.success(f"Detected: {result['detected_disease']}")
    

    return result["detected_disease"]
