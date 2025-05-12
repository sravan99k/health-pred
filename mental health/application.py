from flask import Flask, render_template, request
import os
import cv2
from deepface import DeepFace

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        answers = {
            "q1": request.form.get('q1'),
            "q2": request.form.get('q2')
        }

        video = request.files['video']
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
        video.save(video_path)

        # Capture a frame from video for emotion detection
        emotion = detect_emotion(video_path)

        # Save everything
        with open("results.csv", "a") as f:
            f.write(f"{answers['q1']},{answers['q2']},{emotion}\n")

        return "Assessment Complete!"

    return render_template('index.html')

def detect_emotion(video_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()
    if ret:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        return result[0]['dominant_emotion']
    return "No Face Detected"

if __name__ == "__main__":
    app.run(debug=True, port=8000)
