import streamlit as st

def show_detection(image_file):
    st.subheader("Detection Result")
    result = detect_disease(image_file)

    st.image(result["annotated_image"],
             caption="Detected disease" )
    st.success(f"Detected: {','.join(result['detected_diseases'])}")

    return result["detected_disease"][0]

