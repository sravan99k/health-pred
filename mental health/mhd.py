import streamlit as st
from deepface import DeepFace
import os

st.set_page_config(page_title="Mood & Risk Predictor", layout="centered")
st.title("🧠 AI-Powered Mood & Risk Predictor for Students")
st.write("Answer a few questions and upload your photo to assess your mental well-being.")

# -----------------------------
# 1. Survey Questions
# -----------------------------
st.header("📋 Mental Health Survey")

survey = {}

questions = {
    "anxious": "How often do you feel anxious?",
    "stressed": "How often do you feel stressed?",
    "supported_by_friends": "Do you feel supported by your friends?",
    "talk_to_parents": "Can you talk to your parents when needed?",
    "talk_to_teachers": "Can you talk to your teachers when needed?",
    "overwhelmed": "Do you feel overwhelmed by studies or exams?",
    "time_for_self": "Do you feel you have enough time for yourself?",
    "sleep_hours": "On average, how many hours do you sleep?",
    "rested": "Do you feel rested when you wake up?",
    "exercise": "How often do you exercise or play sports?",
    "eat_healthy": "Do you eat healthy meals regularly?",
    "seek_help": "Would you feel comfortable seeking help?"
}

options = ["Always", "Often", "Sometimes", "Rarely", "Never"]

for key, question in questions.items():
    if key == "sleep_hours":
        survey[key] = st.slider(question, 0, 10, 7)
    else:
        survey[key] = st.selectbox(question, options, key=key)

# -----------------------------
# 2. Upload Image for Emotion Detection
# -----------------------------
st.header("📷 Upload Your Face Photo (Optional)")
uploaded_file = st.file_uploader("Upload an image file (JPG or PNG)", type=["jpg", "jpeg", "png"])

emotion = None
if uploaded_file:
    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.read())
    try:
        analysis = DeepFace.analyze(img_path="temp.jpg", actions=['emotion'], enforce_detection=False)
        emotion = analysis[0]['dominant_emotion']
        st.success(f"Detected Emotion: **{emotion.capitalize()}**")
    except Exception as e:
        st.error("Could not detect emotion. Please try a clearer face photo.")

# -----------------------------
# 3. Calculate Mental Health Risk
# -----------------------------
st.header("🧠 Mood & Risk Score")
risk = 0

# Score survey responses
score_map = {"Always": 10, "Often": 8, "Sometimes": 5, "Rarely": 2, "Never": 0}
for key, value in survey.items():
    if key == "sleep_hours":
        if value < 6:
            risk += 10
        elif value < 8:
            risk += 5
    else:
        risk += score_map.get(value, 0)

# Score based on emotion
if emotion in ["sad", "angry", "fear", "disgust"]:
    risk += 15
elif emotion == "neutral":
    risk += 5

# Show result
st.subheader(f"🔢 Your Mental Health Risk Score: **{risk}/140**")

if risk >= 90:
    st.error("⚠️ High Risk: Please consider talking to a counselor or adult you trust.")
elif 60 <= risk < 90:
    st.warning("🟠 Moderate Risk: Take care, and consider stress-relief practices.")
else:
    st.success("🟢 Low Risk: You're doing well. Keep maintaining a healthy routine!")

# Cleanup temp file
if os.path.exists("temp.jpg"):
    os.remove("temp.jpg")
