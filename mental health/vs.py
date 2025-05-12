import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="🌈 Buddy Pulse – Daily Mood Tracker", layout="centered")

st.title("🌈 Buddy Pulse – Daily Mood Tracker")
st.markdown("## How are you feeling today?")

# Mood options
moods = {
    "😊 Happy": "Happy",
    "😌 Calm": "Calm",
    "😐 Okay": "Okay",
    "😣 Stressed": "Stressed",
    "😢 Sad": "Sad"
}
from streamlit_webrtc import webrtc_streamer
import speech_recognition as sr
import av

st.markdown("### 🎙️ Or Speak Your Mood")

# Recognizer and buffer
recognizer = sr.Recognizer()
voice_mood = ""

# Audio processor class
class AudioProcessor:
    def __init__(self):
        self.buffer = []

    def recv(self, frame):
        audio = frame.to_ndarray()
        self.buffer.append(audio)
        return av.AudioFrame.from_ndarray(audio, layout="mono")

# Start mic
class AudioProcessor:
    def __init__(self):
        self.recorded_audio = []

    def recv(self, frame: av.AudioFrame):
        audio = frame.to_ndarray()
        self.recorded_audio.append(audio)
        return frame  # Just return the frame, no conversion needed


if ctx.audio_receiver:
    audio_buffer = []
    while True:
        try:
            audio_frame = ctx.audio_receiver.get_frames(timeout=1)[0]
            audio_buffer.append(audio_frame.to_ndarray())
            if len(audio_buffer) >= 30:
                break
        except:
            break

    # Save to WAV
    import numpy as np
    from scipy.io.wavfile import write

    audio_data = np.concatenate(audio_buffer, axis=0)
    write("temp.wav", 16000, audio_data)

    # Recognize speech
    with sr.AudioFile("temp.wav") as source:
        audio = recognizer.record(source)
        try:
            voice_mood = recognizer.recognize_google(audio)
            st.success(f"🗣️ You said: **{voice_mood}**")
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand. Try again.")

# Match to mood
if voice_mood:
    for emoji, mood in moods.items():
        if mood.lower() in voice_mood.lower():
            selected_mood = mood
            st.success(f"✅ Mood detected as: {selected_mood}")

# Mood selection
selected_mood = st.radio("Choose your mood:", list(moods.values()))

# Optional note
user_note = st.text_input("Want to say something about your day? (optional)")

# CSV file path
csv_file = "mood_data.csv"

# Load or initialize
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=["date", "mood", "note"])

# Mood submission
if st.button("Submit Mood"):
    mood_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mood": selected_mood,
        "note": user_note
    }
    df = pd.concat([df, pd.DataFrame([mood_entry])], ignore_index=True)
    df.to_csv(csv_file, index=False)
    st.success("✅ Your mood has been recorded!")

# Mood history
st.subheader("📋 Recent Mood Log")
if not df.empty:
    st.dataframe(df.tail(10), use_container_width=True)
else:
    st.info("No mood data available yet.")

# Mood trend bar chart
st.subheader("📊 Mood Frequency")
if not df.empty:
    mood_counts = df["mood"].value_counts()
    st.bar_chart(mood_counts)

# Mood over time line chart
st.subheader("📈 Mood Trend Over Time")
if not df.empty:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['date'] = df['date'].dt.date
    trend = df.groupby(['date', 'mood']).size().unstack(fill_value=0)
    st.line_chart(trend)

# Insight block
st.subheader("🧠 AI Insight (Beta)")
if not df.empty:
    most_common = df['mood'].value_counts().idxmax()
    st.info(f"✨ You’ve mostly felt **{most_common}** lately. Keep tracking to learn more about yourself!")
else:
    st.write("Not enough data to provide insights yet.")

# Utilities: download + clear
st.markdown("### ⚙️ Options")
col1, col2 = st.columns(2)

with col1:
    if not df.empty:
        csv_download = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Mood Data", csv_download, file_name="mood_data.csv", mime='text/csv')

with col2:
    if st.button("🗑️ Clear All Data"):
        if os.path.exists(csv_file):
            os.remove(csv_file)
            st.warning("All mood data cleared.")
            st.experimental_rerun()
