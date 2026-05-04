import cv2
import os

def extract_frames(video_path, output_folder, frame_skip=3):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"❌ Cannot open video: {video_path}")
        return

    os.makedirs(output_folder, exist_ok=True)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    count, saved = 0, 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count % frame_skip == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face = frame[y:y+h, x:x+w]
                cv2.imwrite(f"{output_folder}/frame_{saved}.jpg", face)
                saved += 1

        count += 1

    cap.release()
    print(f"✅ {saved} face frames extracted")

# Run
dataset_path = "dataset"
for sample in os.listdir(dataset_path):
    video_path = f"{dataset_path}/{sample}/video.mp4"
    frames_folder = f"{dataset_path}/{sample}/frames"

    if os.path.exists(video_path):
        extract_frames(video_path, frames_folder)