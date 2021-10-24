"""
dataset.py

Contains a PyTorch dataset used for training.
"""

import os
import random

import PIL
import torch
import torchvision.transforms as T

class ImageSet(torch.utils.data.Dataset):
    """Loads country images.
    
    Images are randomly scaled/rotated, textured, then put onto a background.
    Each country appears three times in the set, with a random permutation each
    time."""
    
    def __init__(self, dup_factor = 3):
        """Loads the images into the dataset."""
        
        self.duplication_factor = dup_factor

        self.countries = list()
        self.backgrounds = list()
        self.backgrounds.append(PIL.Image.new("RGBA", (100, 100), (255, 255, 255)))

        for entry in os.scandir("./dataset/countries"):
            if entry.path.endswith(".png"):
                file_name = os.path.basename(entry.path)
                self.countries.append((PIL.Image.open(entry.path), file_name[:file_name.index(".png")]))
        self.transforms = T.Compose((
            T.RandomRotation(180, expand=True, fill=(0,0,0,0)),
            T.Resize((100,100)),
        ))
        self.normalize = T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

    def __getitem__(self, i):
        """Returns the element in the dataset at index i."""

        index = i % len(self.countries)
        img, _ = self.countries[index]
        img = self.transforms(img)
        background = self.backgrounds[random.randint(0, len(self.backgrounds) - 1)]
        background.paste(img)
        img = T.ToTensor()(background)[:3]
        self.normalize(img)
        return img, index

    def __len__(self):
        """Returns the length of the dataset."""

        return self.duplication_factor * len(self.countries)
    
