import json
from datetime import datetime
import os

def load_feedback(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_feedback(path, weather, outfit, rating):
    feedback = load_feedback(path)
    feedback.append({
        "date": str(datetime.now()),
        "weather": weather,
        "outfit": outfit,
        "rating": rating
    })
    with open(path, "w") as f:
        json.dump(feedback, f, indent=2)
