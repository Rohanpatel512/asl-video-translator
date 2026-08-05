import torch 
from torchvision import datasets, transforms

def train_model(model, train_dataloader, loss_function, optimizer, device):
    """
    Args 
        model - Pre-trained model (CNN) to train on.
        train_dataloader - The training dataloader
        loss_function - Loss function used during training.
        optimizer - Optimizer used during training.
        device - Device trained on (CPU or GPU).
    
    Returns
        train_loss - The loss value during training (float)
        train_accuracy - The accuracy during training (float)
    """

    model.train()

    correct_predictions = 0
    train_loss = 0
    total = 0

    for x, y in train_dataloader:
        x = x.to(device) 
        y = y.to(device)

        optimizer.zero_grad()

        output = model(x) 

        loss = loss_function(output, y)

        loss.backward()
        optimizer.step()

        train_loss += loss.item()

        predictions = torch.argmax(output, dim=1)

        correct_predictions += (predictions == y).sum().item()
        total += y.size(0)


    train_loss = train_loss / len(train_dataloader)
    train_accuracy = correct_predictions / total 

    return train_loss, train_accuracy 

    

def validate_model(model, valid_dataloader, loss_function, device):
    """

    Args
        model - Pre-trained model (CNN) to train on.
        valid_dataloader - The validation dataloader 
        loss_function - Loss function used during training.
        device - Device validation done on (CPU or GPU)

    Returns
        val_loss - The loss value during validation (float)
        val_accuracy - The accuracy during validation (float)
    """
    model.eval()

    total = 0
    val_loss = 0
    val_correct = 0

    with torch.inference_mode():
        for x, y in valid_dataloader:
            x = x.to(device) 
            y = y.to(device) 

            output = model(x)

            loss = loss_function(output, y)
            val_loss += loss.item()

            predictions = torch.argmax(output, dim=1)

            val_correct += (predictions == y).sum().item()
            total += y.size(0)
    
    val_loss = val_loss / len(valid_dataloader)
    val_accuracy = val_correct / total 

    return val_loss, val_accuracy 


def train(model, learning_rate, train_dataloader, valid_dataloader, epochs, loss_function, optimizer, device):
    """
    Trains the model given the learning, epochs, loss function, and optimizer
    
    Args
        model - Pre-trained model (CNN) to train on.
        learning_rate - The learning rate applied to the model.
        train_dataloader - The training dataloader
        valid_dataloader - The validation dataloader 
        epochs - Number of epochs to train.
        loss_function - Loss function used during training.
        optimizer - Optimizer used during training.
        device - Device validation done on (CPU or GPU)

    Returns
        results (Python dictionary) - The results of training and validating 
    """

    results = {
        "train_accuracy": [],
        "train_loss": [],
        "val_accuracy": [],
        "val_loss": []
    }

    for epoch in range(0, epochs):
        train_loss, train_accuracy = train_model(model, train_dataloader, loss_function, optimizer, device)
        val_loss, val_accuracy = validate_model(model, valid_dataloader, loss_function, device)

        results["train_accuracy"].append(train_accuracy)
        results["train_loss"].append(train_loss) 
        results["val_accuracy"].append(val_accuracy)
        results["val_loss"].append(val_loss)

        print(f"Epoch {epoch + 1}\n Train Acc: {train_accuracy:.2f}, Train Loss: {train_loss:.2f} | Validation Acc: {val_accuracy:.2f}, Validation Loss: {val_loss:.2f}")
    
    return results 