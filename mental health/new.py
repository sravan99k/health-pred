import streamlit as st
import os
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Buddy Pulse – Student Wellness Check", layout="centered")
st.title("🌈 Buddy Pulse – Student Mental Health Assessment")
st.markdown("Answer these questions honestly. Your answers are private and help us understand your feelings better.")

categories = {
    "Comparison & Pressure": [
        "Have you ever felt like you're not as good as others in your class?",
        "Do you sometimes feel bad when you don’t score well?",
        "Do you think people only value marks and not your other skills?"
    ],
    "Lack of Interest": [
        "Have you been enjoying your hobbies or fun activities lately?",
        "Do you feel excited to try new things these days?"
    ],
    "Social Media": [
        "How often do you compare yourself to others online?",
        "Do you think social media makes you feel better or worse?"
    ],
    "Distractions": [
        "Do you find it hard to concentrate in class or while studying?",
        "What do you do when you get bored during study time?"
    ],
    "Financial Concerns": [
        "Do you ever stop yourself from asking for something because you're worried about money?",
        "Do you feel comfortable sharing your needs with your parents?"
    ],
    "Discrimination": [
        "Do you feel everyone is treated equally in your school?",
        "Have you felt left out or judged for being different?"
    ],
    "Addictions": [
        "Do you feel you spend too much time on your phone or games?",
        "Can you take breaks from screens easily?"
    ],
    "Stress": [
        "Do you feel calm most of the time?",
        "Do you feel pressure to be perfect?"
    ],
    "Time Management": [
        "Do you feel you have enough time for school, play, and rest?",
        "Are you often in a rush to finish things?"
    ],
    "Generation Gap": [
        "Do you feel your parents understand your thoughts and feelings?",
        "Can you talk to your parents about your worries?"
    ],
    "Career Pressure": [
        "Do you feel free to choose your dream job?",
        "Do you feel heard when you talk about what you want to be?"
    ],
    "Guidance": [
        "Do you have someone to guide you when you're confused?",
        "Do you know whom to talk to when you feel low?"
    ],
    "Loneliness": [
        "Do you feel like you have a friend or adult you can trust?",
        "Do you often keep your feelings to yourself?"
    ],
    "Relationships": [
        "Do your friendships make you feel happy and safe?",
        "Do you feel respected by your friends and family?"
    ],
    "Anger": [
        "Do you get angry easily and not know why?",
        "Can you calm down easily when upset?"
    ],
    "Food": [
        "Are you eating healthy meals every day?",
        "Do you feel tired or low energy often?"
    ]
}

responses = {}
st.markdown("---")
st.subheader("🧠 Questions")

for category, questions in categories.items():
    st.markdown(f"### {category}")
    for q in questions:
        response = st.radio(q, ["😊 Yes", "😐 Sometimes", "😟 No"], key=q)
        responses[q] = response

if st.button("🔍 Submit Assessment"):
    risk_score = sum(1 for v in responses.values() if v == "😟 No") + 0.5 * sum(1 for v in responses.values() if v == "😐 Sometimes")
    st.markdown("---")
    st.subheader("📊 Your Mental Wellness Summary")

    if risk_score <= 10:
        st.success("You seem to be doing quite well! Keep it up! 💪")
    elif 10 < risk_score <= 20:
        st.warning("You're doing okay, but there are a few areas to take care of. Try talking to someone you trust. 🌼")
    else:
        st.error("You might be feeling overwhelmed. It’s important to talk to a counselor, teacher, or parent. You are not alone. ❤️")

    st.markdown("---")
    st.markdown("### 💡 What You Can Do")
    st.markdown("- Talk to a friend, teacher, or counselor you trust")
    st.markdown("- Take breaks, rest well, and eat healthy")
    st.markdown("- Try journaling or drawing how you feel")
    st.markdown("- Don’t be afraid to ask for help")

    # Optional: Save to CSV
    log = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "risk_score": risk_score}
    log.update(responses)
    df = pd.DataFrame([log])
    df.to_csv("student_wellness_log.csv", mode='a', header=not pd.read_csv("student_wellness_log.csv").empty if os.path.exists("student_wellness_log.csv") else True, index=False)
    st.success("Your responses have been safely recorded.")
