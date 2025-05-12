import cv2
from deepface import DeepFace

# Optional: Map emotions to emojis
emoji_dict = {
    "happy": "😊", "sad": "😢", "angry": "😠", "surprise": "😲",
    "fear": "😨", "disgust": "🤢", "neutral": "😐"
}

# Open the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Webcam not accessible.")
    exit()
else:
    print("✅ Webcam is working. Starting emotion detection...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to read from webcam.")
        break

    try:
        # Analyze emotions (allow multiple faces)
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        # Make sure results is a list
        if not isinstance(results, list):
            results = [results]

        for face in results:
            x, y, w, h = face['region']['x'], face['region']['y'], face['region']['w'], face['region']['h']
            emotion = face['dominant_emotion']
            emoji = emoji_dict.get(emotion.lower(), '')

            # Draw rectangle & text
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            cv2.putText(frame, f"{emoji} {emotion}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    except Exception as e:
        cv2.putText(frame, "No face detected", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Show result
    cv2.imshow("Real-Time Emotion Detection", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
