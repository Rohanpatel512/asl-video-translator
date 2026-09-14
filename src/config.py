from pathlib import Path
import os
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

HF_TOKEN = os.getenv("HF_TOKEN")

HAND_MODEL_REPO = os.getenv("HAND_MODEL_REPO", "Bingsu/adetailer")
HAND_MODEL_FILENAME = os.getenv("HAND_MODEL_FILENAME", "hand_yolov8n.pt")

HAND_DETECTION_CONFIDENCE = float(os.getenv("HAND_DETECTION_CONFIDENCE", 0.30))

PRIVATE_MODEL_REPO = os.getenv("PRIVATE_MODEL_REPO", "RohanP29/asl-model")

CLASSIFIER_MODEL_FILENAME = os.getenv("CLASSIFIER_MODEL_FILENAME", "model_v3.pth")

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://127.0.0.1:5500"
    ).split(",")
    if origin.strip()
]