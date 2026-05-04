import os
import pandas as pd
import json
import shutil

df = pd.read_excel("data/responses.xlsx")
os.makedirs("dataset", exist_ok=True)

def compute_traits(row):
    """Compute Big Five personality traits from survey responses"""
    
    def safe_get(col_name):
        """Handle column name variations and missing values"""
        # Try exact match and common variations
        for key in row.index:
            if col_name.strip().lower() == key.strip().lower():
                val = row[key]
                # Ensure value is numeric and in valid range
                try:
                    val = float(val)
                    return max(1, min(5, val))  # Clamp to 1-5
                except:
                    return 3  # Default middle value
        print(f"⚠️ Warning: Column '{col_name}' not found")
        return 3
    
    openness = (
        safe_get("I enjoy trying new and different experiences") +
        safe_get("I am imaginative and creative") +
        safe_get("I like exploring new ideas and concepts") +
        safe_get("I enjoy art, music, or literature") +
        safe_get("I am open to change")
    ) / 5

    conscientiousness = (
        safe_get("I am well-organized in my daily life") +
        safe_get("I complete tasks on time") +
        safe_get("I pay attention to small details") +
        safe_get("I am responsible and dependable")
    ) / 4

    extraversion = (
        safe_get("I am talkative and expressive") +
        safe_get("I enjoy being around people") +
        safe_get("I feel energized in social situations") +
        safe_get("I make friends easily") +
        safe_get("I like being the center of attention")
    ) / 5

    agreeableness = (
        safe_get("I am kind and considerate toward others") +
        safe_get("I trust people easily") +
        safe_get("I like helping others") +
        safe_get("I avoid conflicts when possible") +
        safe_get("I cooperate well in a team")
    ) / 5

    neuroticism = (
        safe_get("I feel stressed or anxious easily") +
        safe_get("I worry about things often") +
        safe_get("I get upset quickly") +
        safe_get("I experience mood swings") +
        safe_get("I feel nervous in unfamiliar situations")
    ) / 5

    return {
        "openness": float(openness),
        "conscientiousness": float(conscientiousness),
        "extraversion": float(extraversion),
        "agreeableness": float(agreeableness),
        "neuroticism": float(neuroticism)
    }

for _, row in df.iterrows():
    sample_id = str(int(row["ID"]))
    folder = f"dataset/{sample_id}"
    os.makedirs(folder, exist_ok=True)

    src_video = f"videos/video_{sample_id}.mp4"
    dst_video = f"{folder}/video.mp4"

    if not os.path.exists(src_video):
        print(f"⚠️ Missing video {sample_id}")
        continue

    shutil.copy(src_video, dst_video)
    labels = compute_traits(row)

    with open(f"{folder}/labels.json", "w") as f:
        json.dump(labels, f, indent=4)

print("✅ Dataset ready")