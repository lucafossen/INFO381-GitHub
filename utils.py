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




"""
Cherry-picked real images for explanation and evaluation.

Descriptions for each image:
- "1": man with camera - image has black crop
- "2": car parked in southern Europe
- "3": man smiling to camera
- "4": dog laying on grass
- "5": cat with blue and yellow eyes
- "6": waterfall from Iceland
- "7": desert with blue sky
- "8": model in black and white
- "9": man staring into the camera
- "10": painting of man with big ear
"""

cherry_pick_img_real = {
    1: "/content/fake_vs_real/test/real/207.jpg",
    2: "/content/fake_vs_real/test/real/212.jpg",
    3: "/content/fake_vs_real/test/real/388.jpg",
    4: "/content/fake_vs_real/test/real/467.jpg",
    5: "/content/fake_vs_real/test/real/653.jpg",
    6: "/content/fake_vs_real/test/real/1034.jpg",
    7: "/content/fake_vs_real/test/real/1042.jpg",
    8: "/content/fake_vs_real/test/real/2028.jpg",
    9: "/content/fake_vs_real/test/real/2681.jpg",
    10: "/content/fake_vs_real/test/real/eo40kdp8ot5a1.jpg"
}


"""
Cherry-picked AI-generated (fake) images for explanation and evaluation.

Descriptions for each image:
- "1": Bull Terrier on man
- "2": Statue of man's face
- "3": Girl with skateboard
- "4": Lady with bear on hike
- "5": DALLE watermark, girl with phones and phone head
- "6": Girl with alien
- "7": Will Smith with gun – seems real but has weird buttons/shadows
- "8": Fake wolf
- "9": DALLE watermark, Gender reveal nuclear bomb
- "10": DALLE watermark, Painting of a king with a burger in his hands
"""

cherry_pick_img_ai_generated = {
    1: "/content/fake_vs_real/test/fake/10098.jpg",
    2: "/content/fake_vs_real/test/fake/3158.jpg",
    3: "/content/fake_vs_real/test/fake/11729.jpg",
    4: "/content/fake_vs_real/test/fake/22314.png",
    5: "/content/fake_vs_real/test/fake/12395.jpg",
    6: "/content/fake_vs_real/test/fake/3017.jpg",
    7: "/content/fake_vs_real/test/fake/22417.png",
    8: "/content/fake_vs_real/test/fake/23674.png",
    9: "/content/fake_vs_real/test/fake/25755.png",
    10: "/content/fake_vs_real/test/fake/12073.jpg"
}

