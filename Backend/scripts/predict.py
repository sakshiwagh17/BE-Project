import numpy as np
import pickle

# Load model
model = pickle.load(open("models/personality_model.pkl", "rb"))

# Load scaler (FIXED)
scaler = pickle.load(open("models/scaler.pkl", "rb"))

# Load feature
feature = np.load("test_feature.npy")

# Reshape properly
feature = feature.reshape(1, -1)

# Scale
feature = scaler.transform(feature)

# Predict
pred = model.predict(feature)[0]

traits = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]

print("\n🎯 BIG FIVE PERSONALITY:")
for i, t in enumerate(traits):
    print(f"{t}: {pred[i]:.2f}")