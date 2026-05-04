import os
import subprocess

def extract_audio(video_path, audio_path):
    command = [
        "C:\\Users\\DELL\\Downloads\\ffmpeg-8.1-full_build\\ffmpeg-8.1-full_build\\bin\\ffmpeg.exe",
        "-i", video_path,
        "-ar", "16000",
        "-ac", "1",
        "-y",
        audio_path
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

dataset_path = "dataset"

for sample in os.listdir(dataset_path):
    video_path = f"{dataset_path}/{sample}/video.mp4"
    audio_path = f"{dataset_path}/{sample}/audio.wav"

    if os.path.exists(video_path):
        extract_audio(video_path, audio_path)

print("✅ Audio extracted")