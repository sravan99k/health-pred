from deepface import DeepFace
import cv2

def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)
    emotions = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotions.append(result[0]['dominant_emotion'])
        except:
            continue
    cap.release()

    summary = {e: emotions.count(e) for e in set(emotions)}
    return summary
