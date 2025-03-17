from flask import Flask, render_template, Response
import cv2
import pandas as pd
import numpy as np

app = Flask(__name__)

# Read color data from CSV
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

# Initialize variables for smoothing
smooth_R, smooth_G, smooth_B = 0, 0, 0
alpha = 0.2  

def get_color_name(R, G, B):
    minimum = 10000
    cname = "Unknown"
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

cap = cv2.VideoCapture(0)

def generate_frames():
    global smooth_R, smooth_G, smooth_B
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape
            cx, cy = width // 2, height // 2
            pixel_center = frame[cy, cx]
            B, G, R = pixel_center

            # Apply smoothing
            smooth_R = alpha * R + (1 - alpha) * smooth_R
            smooth_G = alpha * G + (1 - alpha) * smooth_G
            smooth_B = alpha * B + (1 - alpha) * smooth_B

            color_name = get_color_name(int(smooth_R), int(smooth_G), int(smooth_B))
            cv2.rectangle(frame, (10, 10), (200, 50), (0, 0, 0), -1)
            cv2.circle(frame, (220, 30), 20, (int(smooth_B), int(smooth_G), int(smooth_R)), -1)
            cv2.putText(frame, color_name, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.circle(frame, (cx, cy), 3, (255, 255, 255), -1)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
