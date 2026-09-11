import torchvision
from torchvision import transforms 
import torch 
import torchvision.models as models 
import torch.nn as nn 

def load_model():
    """
    Loads the pre-trained model and its weights for ASL prediction.
    
    Args
        - None
    Returns
        - model: The pre-trained model with loaded weights.
    """

    NUM_CLASSES = 29
    PATH = '/Users/rohan/Desktop/Python-Projects/asl-video-translator/data/weights/model_v3.pth'

    model = torchvision.models.resnet18(weights=None)

    model.fc = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(
            in_features=model.fc.in_features, 
            out_features=NUM_CLASSES
        )
    )

    model.load_state_dict(torch.load(PATH, map_location=torch.device('cpu')))

    return model 