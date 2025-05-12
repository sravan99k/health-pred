import streamlit as st
from emotion_analysis import analyze_video
from risk_calculator import calculate_risk
import tempfile
import os

st.title("🧠 Mental Health Risk Predictor")

# Instructions
st.info("📷 Please allow camera access and record video while answering.")

# Survey Form
with st.form("survey"):
    q1 = st.selectbox("1. How often do you feel stressed?", ["Always", "Often", "Sometimes", "Rarely", "Never"])
    q2 = st.selectbox("2. Do you feel tired even after rest?", ["Always", "Often", "Sometimes", "Rarely", "Never"])
    q3 = st.selectbox("3. How often do you feel sad?", ["Always", "Often", "Sometimes", "Rarely", "Never"])
    video_file = st.file_uploader("📹 Upload Recorded Video (WebM/MP4)", type=["webm", "mp4"])
    submit = st.form_submit_button("Submit")

if submit:
    if not video_file:
        st.warning("Please upload a webcam recording.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp:
            temp.write(video_file.read())
            temp_path = temp.name

        with st.spinner("Analyzing emotions..."):
            emotion_summary = analyze_video(temp_path)

        survey_answers = {"q1": q1, "q2": q2, "q3": q3}
        risk_percent = calculate_risk(emotion_summary, survey_answers)

        st.success(f"✅ Mental Health Risk: {risk_percent}%")
        st.json(emotion_summary)
        os.remove(temp_path)
        # Additional Feature: Age-appropriate Mental Health Tips
        st.header("📘 Mental Health Tips for Students")

        class_tips = {
            "6th": [
                "Take short breaks while studying to refresh your mind.",
                "Talk to your parents or teachers if you feel overwhelmed."
            ],
            "7th": [
                "Practice deep breathing exercises to reduce stress.",
                "Engage in a hobby like drawing or playing a sport."
            ],
            "8th": [
                "Maintain a healthy sleep schedule for better focus.",
                "Share your feelings with a trusted friend or adult."
            ],
            "9th": [
                "Set realistic goals and celebrate small achievements.",
                "Avoid comparing yourself to others; focus on your growth."
            ],
            "10th": [
                "Plan your study schedule to avoid last-minute stress.",
                "Remember to take care of your physical health too."
            ]
        }

        selected_class = st.selectbox("Select Your Class", ["6th", "7th", "8th", "9th", "10th"])
        if selected_class:
            st.subheader(f"Tips for {selected_class} Grade Students:")
            for tip in class_tips[selected_class]:
                st.write(f"- {tip}")