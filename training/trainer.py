"""
trainer.py

Trains the model.
"""

import torch
import torchvision

from dataset import ImageSet

def train(batch_size, lr, patience, device):
    train_set = ImageSet()
    dev_set = ImageSet(dup_factor=1)
    train_loader = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True)
    dev_loader = torch.utils.data.DataLoader(dev_set, batch_size=batch_size, shuffle=True)

    num_classes = len(dev_set) // dev_set.duplication_factor
    model = torchvision.models.resnet34(pretrained=True).to(device)
    model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(params=model.parameters(), lr=lr)

    no_improvement = 0
    best_dev_loss = 1000000000

    max_epochs = 100
    epochs = 0

    while no_improvement < patience and epochs < max_epochs:
        train_loss = 0
        dev_loss = 0
        train_batches = 0
        dev_batches = 0
        model.train()
        for imgs, labels in train_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            pred = model(imgs)
            loss = loss_fn(pred, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
            train_batches += 1
        model.eval()
        for imgs, labels in dev_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            pred = model(imgs)
            loss = loss_fn(pred, labels)
            dev_loss += loss.item()
            dev_batches += 1
        train_loss = train_loss / train_batches
        dev_loss = dev_loss / dev_batches

        if dev_loss < best_dev_loss:
            best_dev_loss = dev_loss
            no_improvement = 0
            torch.save(model.state_dict(), "model_weights")
            print("New best dev loss!")
        else:
            no_improvement += 1
        epochs += 1
        print(f"Epoch: {epochs}; Training Loss: {train_loss}; Dev Loss: {dev_loss}; Best Dev Loss: {best_dev_loss}")


def main():
    cuda_avail = torch.cuda.is_available()
    device = None
    if cuda_avail:
        device = "cuda"
    else:
        device = "cpu"
        print("Training on CPU :(")
    train(batch_size=16, lr=1e-3, patience=5, device=device)


if __name__=="__main__":
    main()
