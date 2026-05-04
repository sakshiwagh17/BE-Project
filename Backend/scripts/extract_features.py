import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import os
import numpy as np
import json
from sklearn.preprocessing import StandardScaler
import librosa
from deepface import DeepFace


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ResNet
resnet = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
resnet = torch.nn.Sequential(*list(resnet.children())[:-1])
resnet = resnet.to(device)
resnet.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# -------------------------
# IMAGE FEATURE
# -------------------------
def get_image_feature(path):
    try:
        img = Image.open(path).convert("RGB")
        img = transform(img).unsqueeze(0).to(device)

        with torch.no_grad():
            feat = resnet(img)

        return feat.squeeze().cpu().numpy()
    except:
        return np.zeros(512)

# -------------------------
# EMOTION FEATURE
# -------------------------
def get_emotion(path):
    try:
        result = DeepFace.analyze(
            img_path=path,
            actions=['emotion'],
            enforce_detection=False,
            silent=True
        )

        e = result[0]['emotion']

        return np.array([
            e['angry'], e['disgust'], e['fear'],
            e['happy'], e['sad'], e['surprise'], e['neutral']
        ])
    except:
        return np.zeros(7)

# -------------------------
# AUDIO FEATURE
# -------------------------
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

# -------------------------
# VIDEO PROCESSING
# -------------------------
def process_video(frames_folder):
    img_feats, emo_feats = [], []

    frame_files = sorted([
        f for f in os.listdir(frames_folder)
        if f.endswith(('.jpg', '.png'))
    ])

    if len(frame_files) == 0:
        return np.zeros(1024), np.zeros(7)

    # 🔥 SAMPLE FRAMES (IMPORTANT)
    step = max(1, len(frame_files) // 10)   # only ~10 frames
    sampled_frames = frame_files[::step]

    print(f"Processing {len(sampled_frames)} frames (sampled)")

    for i, f in enumerate(sampled_frames):
        path = os.path.join(frames_folder, f)

        print(f"Frame {i+1}/{len(sampled_frames)}")

        # IMAGE FEATURE
        img_feat = get_image_feature(path)
        img_feats.append(img_feat)

        # 🔥 EMOTION ONLY ON SOME FRAMES
        if i % 2 == 0:   # only half frames
            emo_feat = get_emotion(path)
            emo_feats.append(emo_feat)

    img_feats = np.array(img_feats)
    emo_feats = np.array(emo_feats) if len(emo_feats) > 0 else np.zeros((1,7))

    # IMAGE AGGREGATION
    img_final = np.concatenate([
        np.mean(img_feats, axis=0),
        np.std(img_feats, axis=0)
    ])

    # EMOTION AGGREGATION
    emo_final = np.mean(emo_feats, axis=0)

    return img_final, emo_final

# -------------------------
# CREATE DATASET
# -------------------------
X, y = [], []

dataset_path = "dataset"

for sample in os.listdir(dataset_path):
    frames = f"{dataset_path}/{sample}/frames"
    audio = f"{dataset_path}/{sample}/audio.wav"
    label_path = f"{dataset_path}/{sample}/labels.json"

    if not os.path.exists(frames) or not os.path.exists(label_path):
        continue

    img_feat, emo_feat = process_video(frames)
    aud_feat = get_audio_feature(audio)

    final_feature = np.concatenate([img_feat, emo_feat, aud_feat])

    with open(label_path) as f:
        label = json.load(f)

    X.append(final_feature)
    y.append([
        label["openness"],
        label["conscientiousness"],
        label["extraversion"],
        label["agreeableness"],
        label["neuroticism"]
    ])

X = np.array(X)
y = np.array(y)

scaler = StandardScaler()
X = scaler.fit_transform(X)

os.makedirs("features", exist_ok=True)
np.save("features/X.npy", X)
np.save("features/y.npy", y)
np.save("features/scaler.npy", scaler, allow_pickle=True)

print("✅ Features ready:", X.shape)