import streamlit as st
from deepface import DeepFace
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Student Mood Detector", layout="centered")

st.title("🎭 AI-Powered Mood Detector for Students")
st.markdown("Upload a selfie to detect your current mood (emotion analysis).")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Analyzing Mood..."):
        try:
            # Convert to OpenCV format
            img_array = np.array(image.convert('RGB'))
            result = DeepFace.analyze(img_array, actions=['emotion'], enforce_detection=False)

            # Show results
            st.subheader("Detected Emotion:")
            st.success(result[0]['dominant_emotion'])

            st.markdown("### Emotion Probabilities:")
            st.json(result[0]['emotion'])

        except Exception as e:
            st.error("Could not detect face or emotion. Try another image.")
            st.error(str(e))
