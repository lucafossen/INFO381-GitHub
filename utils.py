import os
import zipfile
import torch
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from torchvision import transforms

def get_dataloaders(zip_path="fake_vs_real.zip", local_exctract_dir="../", batch_size=32, transform=None, split="both"):
    """
    Gets train/test DataLoaders (assuming a folder structure similar to the CIFAKE dataset).
    If running on Google Colab, the zip file is always extracted into a non-synced folder.
    If running locally, the zip file is extracted only if the folder doesn't already exist.

    :param zip_path: Path to the zip file containing your dataset
                    (with 'train' and 'test' folders).
    :param batch_size: Batch size for DataLoaders.
    :param transform: Optional torchvision transform to apply
                    (if None, a basic transform is used).
    :param split: 'train', 'test', or 'both' to return the corresponding DataLoader(s).
    :return: (train_loader, test_loader)
    """
    folder_name = zip_path.split(".")[0]+"/"
    try:
        import google.colab
        IN_COLAB = True
        print("Running in Google Colab")
    except:
        IN_COLAB = False
        print("Not running in Google Colab")

    if IN_COLAB:
        extract_dir = "/content/"+folder_name
        # Create the directory if it doesn't exist
        os.makedirs(extract_dir, exist_ok=True)
        # Always extract in Colab
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
    else:
        extract_dir = local_exctract_dir+folder_name
        # If the folder already exists, skip extraction
        if not os.path.exists(extract_dir):
            print(f"Folder '{extract_dir}' does not exist. Extracting from {zip_path} ...")
            os.makedirs(extract_dir, exist_ok=True)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
        else:
            print(f"Folder '{extract_dir}' exists. Loading...")

    # Default transform if none is provided
    if transform is None:
        transform = transforms.Compose([
            transforms.ToTensor()
        ])

    train_path = os.path.join(extract_dir, "train")
    test_path  = os.path.join(extract_dir, "test")

    train_dataset = ImageFolder(root=train_path, transform=transform)
    test_dataset  = ImageFolder(root=test_path, transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader  = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    if split == "train":
        return train_loader
    elif split == "test":
        return test_loader
    elif split == "both":
        return train_loader, test_loader
    else:
        raise ValueError("Invalid split. Choose 'train', 'test', or 'both'.")