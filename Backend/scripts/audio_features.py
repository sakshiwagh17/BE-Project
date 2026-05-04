import librosa
import numpy as np

def extract_audio_features(audio_path):
    try:
        y, sr = librosa.load(audio_path, sr=None)

        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc = np.mean(mfcc, axis=1)

        pitches, _ = librosa.piptrack(y=y, sr=sr)
        pitch_values = pitches[pitches > 0]
        pitch = np.mean(pitch_values) if len(pitch_values) > 0 else 0

        energy = np.mean(librosa.feature.rms(y=y))
        zcr = np.mean(librosa.feature.zero_crossing_rate(y))

        return np.hstack([mfcc, pitch, energy, zcr])

    except Exception as e:
        print("❌ Audio error:", e)
        return np.zeros(16)