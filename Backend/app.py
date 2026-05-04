from flask import Flask, request, jsonify
import os
import cv2
import torch
import pickle
import numpy as np
from PIL import Image
from torchvision.models import resnet18, ResNet18_Weights
import torchvision.transforms as transforms
from flask_cors import CORS
import shutil
import subprocess
import librosa

app = Flask(__name__)
CORS(app)

# =========================
# LOAD MODEL + SCALER
# =========================
model = pickle.load(open("./models/personality_model.pkl", "rb"))
scaler = np.load("./features/scaler.npy", allow_pickle=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =========================
# LOAD RESNET
# =========================
resnet = resnet18(weights=ResNet18_Weights.DEFAULT)
resnet = torch.nn.Sequential(*list(resnet.children())[:-1])
resnet = resnet.to(device)
resnet.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                         std=[0.229, 0.224, 0.225])
])

# =========================
# FRAME EXTRACTION
# =========================
def extract_frames(video_path, temp_folder="temp_frames", frame_skip=3):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise Exception("❌ Cannot open video")

    os.makedirs(temp_folder, exist_ok=True)

    count, saved = 0, 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count % frame_skip == 0:
            cv2.imwrite(f"{temp_folder}/frame_{saved:04d}.jpg", frame)
            saved += 1

        count += 1

    cap.release()

    if saved == 0:
        raise Exception("❌ No frames extracted")

    print(f"✅ Extracted {saved} frames")
    return temp_folder


# =========================
# IMAGE FEATURE (ResNet)
# =========================
def get_image_feature(image_path):
    try:
        img = Image.open(image_path).convert("RGB")
        img = transform(img).unsqueeze(0).to(device)

        with torch.no_grad():
            feature = resnet(img)

        return feature.squeeze().cpu().numpy()
    except:
        return np.zeros(512)


# =========================
# VIDEO FEATURE (MEAN + STD)
# =========================
def process_video(frames_folder):
    features = []

    for f in os.listdir(frames_folder):
        path = os.path.join(frames_folder, f)
        feat = get_image_feature(path)

        if not np.allclose(feat, 0):
            features.append(feat)

    if len(features) == 0:
        raise Exception("❌ No valid frames")

    features = np.array(features)

    mean_feat = np.mean(features, axis=0)
    std_feat = np.std(features, axis=0)

    return np.concatenate([mean_feat, std_feat])


# =========================
# AUDIO EXTRACTION (FFmpeg)
# =========================
def extract_audio(video_path, audio_path="temp_audio.wav"):
    command = [
        "ffmpeg",
        "-i", video_path,
        "-ar", "16000",
        "-ac", "1",
        "-y",
        audio_path
    ]

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not os.path.exists(audio_path):
        raise Exception("❌ Audio extraction failed")

    return audio_path


# =========================
# AUDIO FEATURES (librosa)
# =========================
def get_audio_feature(audio_path):
    try:
        y, sr = librosa.load(audio_path, sr=16000)

        mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1)
        energy = np.mean(librosa.feature.rms(y=y))
        zcr = np.mean(librosa.feature.zero_crossing_rate(y))
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        return np.concatenate([mfcc, [energy, zcr, tempo]])
    except:
        return np.zeros(16)


# =========================
# API ROUTE
# =========================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "video" not in request.files:
            return jsonify({"error": "No video provided"}), 400

        file = request.files["video"]
        video_path = "temp_video.mp4"
        file.save(video_path)

        # 🎬 VIDEO PROCESSING
        frames_folder = extract_frames(video_path)
        video_feature = process_video(frames_folder)

        # 🔊 AUDIO PROCESSING
        audio_path = extract_audio(video_path)
        audio_feature = get_audio_feature(audio_path)

        # 🔥 FEATURE FUSION
        final_feature = np.concatenate([video_feature, audio_feature])
        final_feature = scaler.transform([final_feature])[0]

        # 🤖 MODEL PREDICTION
        prediction = model.predict([final_feature])[0]
        prediction = np.clip(prediction, 0, 1)

        # 🎯 OCEAN OUTPUT
        traits = [
            "Openness",
            "Conscientiousness",
            "Extraversion",
            "Agreeableness",
            "Neuroticism"
        ]

        result = {trait: float(prediction[i]) for i, trait in enumerate(traits)}

        # 🧹 CLEANUP
        shutil.rmtree(frames_folder, ignore_errors=True)
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True)