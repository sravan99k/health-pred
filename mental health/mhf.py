import streamlit as st
import cv2
import os
import uuid
from deepface import DeepFace

# --- Setup ---
st.set_page_config(page_title="AI Mental Health Assessment", layout="centered")
st.title("🧠 AI-Powered Mood & Mental Health Risk Predictor")

questions = [
    "How often do you feel sad or down?",
    "Do you have trouble sleeping or sleep too much?",
    "How often do you feel anxious or worried?",
    "Do you enjoy activities that you used to enjoy?",
    "Do you find it hard to concentrate or focus?",
    "Do you feel isolated or alone frequently?",
    "Do you feel overwhelmed with schoolwork or relationships?",
    "Have you ever had thoughts of hurting yourself?",
]

options = ["Never", "Rarely", "Sometimes", "Often", "Always"]

# Store captured data
if "captured_data" not in st.session_state:
    st.session_state.captured_data = []

# Folder to save snapshots
if not os.path.exists("snapshots"):
    os.makedirs("snapshots")

# --- Function to capture face + answer ---
def capture_face_expression(q_num, answer):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if ret:
        filename = f"snapshots/q{q_num}_{uuid.uuid4().hex[:8]}.jpg"
        cv2.imwrite(filename, frame)

        try:
            analysis = DeepFace.analyze(img_path=filename, actions=['emotion'], enforce_detection=False)
            emotion = analysis[0]['dominant_emotion']
        except:
            emotion = "undetected"

        st.session_state.captured_data.append({
            "question": questions[q_num],
            "answer": answer,
            "emotion": emotion,
            "image_path": filename
        })
        return emotion
    return "no_frame"

# --- Question Loop ---
st.header("📋 Mental Health Questions")
for i, q in enumerate(questions):
    st.write(f"**Q{i+1}. {q}**")
    selected = st.radio(f"Select your answer for Q{i+1}:", options, key=f"q{i+1}_answer")

    if st.button(f"📸 Capture Response for Q{i+1}"):
        if selected:
            emotion = capture_face_expression(i, selected)
            st.success(f"✅ Captured Q{i+1}: {selected} | Emotion: {emotion}")
        else:
            st.warning("Please select an answer before capturing.")

# --- Submit Section ---
st.markdown("---")
if st.button("🧮 Submit Assessment"):
    if len(st.session_state.captured_data) == 0:
        st.error("❌ No answers captured. Please answer the questions and capture responses before submitting.")
    else:
        # Scoring logic
        emotion_risk = {"happy": 0, "neutral": 1, "sad": 2, "angry": 3, "fear": 3, "disgust": 2, "surprise": 1, "undetected": 1}
        answer_risk = {"Never": 0, "Rarely": 1, "Sometimes": 2, "Often": 3, "Always": 4, "Yes": 2, "No": 0}

        total_score = 0
        for entry in st.session_state.captured_data:
            total_score += answer_risk.get(entry['answer'], 0)
            total_score += emotion_risk.get(entry['emotion'], 1)

        risk_percent = min(100, int((total_score / (len(st.session_state.captured_data) * 7)) * 100))

        # --- Display Results ---
        st.header("📊 Your Results")
        st.write(f"🧠 **Mental Health Risk Score**: `{risk_percent}%`")
        st.progress(risk_percent)

        st.subheader("📌 Summary of Responses:")
        for entry in st.session_state.captured_data:
            st.markdown(f"**Q:** {entry['question']}")
            st.write(f"📝 Answer: `{entry['answer']}`")
            st.write(f"😊 Emotion: `{entry['emotion']}`")
            st.image(entry['image_path'], width=200)
            st.markdown("---")
