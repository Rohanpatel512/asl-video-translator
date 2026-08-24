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

    train_transform = transforms.Compose([
        transforms.Resize(size=(224, 224)),

        transforms.RandomApply([
            transforms.RandomRotation(10)
        ], p=0.5),

        transforms.RandomApply([
            transforms.RandomResizedCrop(
                224,
                scale=(0.85, 1.0)
            )
        ], p=0.5),

        transforms.RandomApply([
            transforms.ColorJitter(
                brightness=0.2,
                contrast=0.2,
                saturation=0.2
            )
        ], p=0.5),

        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    eval_transform = transforms.Compose([
        transforms.Resize(size=(224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    train_data = datasets.ImageFolder(root=train_path, transform=train_transform)
    val_data = datasets.ImageFolder(root=val_path, transform=eval_transform) 
    test_data = datasets.ImageFolder(root=test_path, transform=eval_transform)

    train_files = set(x[0] for x in train_data.samples)
    val_files = set(x[0] for x in val_data.samples)
    test_files = set(x[0] for x in test_data.samples)
    
    train_val_overlap = train_files & val_files
    train_test_overlap = train_files & test_files 
    test_val_overlap = test_files & val_files 

    if train_val_overlap or train_test_overlap or test_val_overlap:
        raise ValueError(
            f"Found overlapping image files."
            "Check your dataset split and ensure the two folders are separate."
        )

    train_dataloader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
    val_dataloader = DataLoader(val_data, batch_size=batch_size, shuffle=False)
    test_dataloader = DataLoader(test_data, batch_size=batch_size, shuffle=False)

    return train_dataloader, val_dataloader, test_dataloader, train_data, val_data, test_data

