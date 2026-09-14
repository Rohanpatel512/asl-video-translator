from PIL import Image 
import torchvision
from torchvision import transforms 
import torch 
import torchvision.models as models 
import torch.nn as nn 
from src.utils import load_model
import cv2
import mediapipe as mp
from huggingface_hub import hf_hub_download
from ultralytics import YOLO
import numpy as np
import random
from src.config import (
    HAND_MODEL_REPO,
    HAND_MODEL_FILENAME,
    HAND_DETECTION_CONFIDENCE,
    CORS_ORIGINS,
)

# Load the pre-trained model 
model = load_model()

MAP = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 
       'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 
       'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25, 'del': 26, 'nothing': 27, 'space': 28}


# Get the pre-trained model path 
model_pth = hf_hub_download(repo_id=str(HAND_MODEL_REPO), filename=str(HAND_MODEL_FILENAME))

# Load in the pre-trained hand detector model 
hand_detector = YOLO(model_pth)


def process_frame(file):
    """
    Processes frame captured by camera 
    Args
        - file: JPEG captured by camera.
    Returns
        - letter: letter predicted by the model.
    """

    frame = file

    box = detect_hand(frame)

    if box is None:
        return {
            "letter": None,
            "hand_detected": False
        }

    x_min, y_min, x_max, y_max = box 

    padding = 40 

    x_min = max(0, x_min - padding)
    y_min = max(0, y_min - padding)
    x_max = min(frame.width, x_max + padding)
    y_max = min(frame.height, y_max + padding)
    
    # Crop the frame to the bounding box of the hand
    hand = frame.crop((x_min, y_min, x_max, y_max))

    # Chage image size to 224x224 and convert to tensor
    transform = transforms.Compose([
        transforms.Resize(size=(224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    hand = transform(hand).unsqueeze(0) 
    
    model.eval()

    with torch.inference_mode():
        output = model(hand)
        prediction = output.argmax(dim=1).item()

        probabilities = torch.softmax(output, dim=1)

    confidence = probabilities.max().item()

    if confidence >= 0.80:
        letter = list(MAP.keys())[list(MAP.values()).index(prediction)] 
        return {"letter": letter, "hand_detected": True}
    
    return {"letter": None, "hand_detected": True}

   
def detect_hand(image):
    """
    Detects if there is a hand in the image.
    Args:
        - image: PIL Image object.
    
    Returns: 
        - Tuple containing the coordinates of the bounding box if hand is detected, otherwise None.
    """

    results = hand_detector(image, conf=HAND_DETECTION_CONFIDENCE)

    result = results[0]

    if len(result.boxes) == 0:
        return None

    # Get the highest confidence detection
    confidences = result.boxes.conf 

    # Select the box with highest confidence 
    best_idx = confidences.argmax().item()

    # Get the bounding box around users hand 
    box = result.boxes.xyxy[best_idx].cpu().numpy()

    x_min, y_min, x_max, y_max = box 

    return (
        int(x_min),
        int(y_min),
        int(x_max),
        int(y_max)
    )