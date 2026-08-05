import os 
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

def create_dataloaders(train_path, val_path, test_path, batch_size=32):
    """
    Create train, test, and validation dataloaders for training pipeline.
    Args
        train_path (str) - Path to training set 
        val_path (str) - Path to validation set 
        test_path (str) - Path to test set 
    
    Returns
        train_dataloader (DataLoader) - Iteratable training dataset
        val_dataloader (DataLoader) - Iteratable validation dataset
        test_dataloader (DataLoader) - Iteratable test dataset

        train_data (Image Folder) - Train image dataset 
        val_data (Image Folder) - Test image dataset 
        test_data (Image Folder) - Validation image dataset
    """

    data_transform = transforms.Compose([
        transforms.Resize(size=(224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    train_data = datasets.ImageFolder(root=train_path, transform=data_transform)
    val_data = datasets.ImageFolder(root=val_path, transform=data_transform) 
    test_data = datasets.ImageFolder(root=test_path, transform=data_transform)

    train_files = set(x[0] for x in train_data.samples)
    val_files = set(x[0] for x in val_data.samples)
    overlap_files = train_files & val_files

    print(f"Same file paths in both val and train: {len(overlap_files)}")
    if overlap_files:
        raise ValueError(
            f"Found {len(overlap_files)} overlapping image files between train and val. "
            "Check your dataset split and ensure the two folders are separate."
        )

    train_dataloader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
    val_dataloader = DataLoader(val_data, batch_size=batch_size, shuffle=False)
    test_dataloader = DataLoader(test_data, batch_size=batch_size, shuffle=False)

    return train_dataloader, val_dataloader, test_dataloader, train_data, val_data, test_data

