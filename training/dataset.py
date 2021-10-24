"""
dataset.py

Contains a PyTorch dataset used for training.
"""

from _typeshed import Self
import os

import PIL
import torch
import torchvision.transforms as T

class ImageSet(torch.utils.data.Dataset):
    """Loads country images.
    
    Images are randomly scaled/rotated, textured, then put onto a background.
    Each country appears three times in the set, with a random permutation each
    time."""
    
    def __init__(self):
        """Loads the images into the dataset."""
        
        self.duplication_factor = 3

        self.countries = list()

        for entry in os.scandir("./dataset/countries"):
            if entry.path.endswith(".png"):
                file_name = os.path.basename(entry.path)
                self.countries.append((PIL.image.open(), file_name[:file_name.index(".png")]))
        self.transforms = T.Compose(
            T.RandomRotation(180, expand=True, fill=(0,0,0,0)),
            T.Resize((100,100)),
            T.ToTensor(),
        )

    def __getitem__(self, i):
        """Returns the element in the dataset at index i."""

        index = i % len(self.countries)
        img, _ = self.countries[index]
        return self.transform(img), index

    def __len__(self):
        """Returns the length of the dataset."""

        return self.duplication_factor * len(self.countries)
    
