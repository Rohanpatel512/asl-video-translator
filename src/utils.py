import torchvision
from torchvision import transforms 
import torch 
import torchvision.models as models 
import torch.nn as nn 
from huggingface_hub import hf_hub_download
from src.config import (
    HF_TOKEN,
    HAND_MODEL_REPO,
    HAND_MODEL_FILENAME,
    HAND_DETECTION_CONFIDENCE,
    PRIVATE_MODEL_REPO,
    CLASSIFIER_MODEL_FILENAME,
    CORS_ORIGINS
)

def load_model():
    """
    Loads the pre-trained model and its weights for ASL prediction.
    
    Args
        - None
    Returns
        - model: The pre-trained model with loaded weights.
    """

    NUM_CLASSES = 29

    model = torchvision.models.resnet18(weights=None)

    model.fc = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(
            in_features=model.fc.in_features, 
            out_features=NUM_CLASSES
        )
    )

    local_weight_path = hf_hub_download(
        repo_id=PRIVATE_MODEL_REPO,
        filename=CLASSIFIER_MODEL_FILENAME,
        token=HF_TOKEN
    )

    model.load_state_dict(torch.load(local_weight_path, map_location=torch.device('cpu')))

    return model 