import torch
import torch.nn as nn
from abc import ABC, abstractmethod
import torchvision.models as models
import torchvision.transforms as T

# If not installed, install CLIP from GitHub:
#   pip install git+https://github.com/openai/CLIP.git
import clip

class BinaryClassifier(nn.Module, ABC):
    """
    Abstract superclass for binary classifiers.
    Enforces the presence of a preprocessor:
      self.preprocessor
    """
    def __init__(self):
        super().__init__()
        self.preprocessor = None

    @abstractmethod
    def forward(self, images):
        """
        Subclasses must implement their own forward() method.
        """
        pass

class CLIPBinaryClassifier(BinaryClassifier):
    """
    A self-contained classifier using CLIP's encode_image()
    plus a linear head for two-class classification.

    By default, loads the ViT-B/32 variant of CLIP and
    attempts to read weights from 'models/clip_vit_classifier.pth'.
    """
    def __init__(
        self,
        device=torch.device("cuda" if torch.cuda.is_available() else "cpu"),
        model_path="models/clip_classifier_10epochs.pth",
        clip_variant="ViT-B/32",
        embed_dim=512,
        num_classes=2
    ):
        super().__init__()
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        # 1) Load a CLIP model + recommended preprocessor
        clip_model, clip_preprocess = clip.load(clip_variant, device=device)
        clip_model.eval()
        for param in clip_model.parameters():
            param.requires_grad = False

        # 2) Store them as attributes
        self.clip_model = clip_model
        self.classifier = nn.Linear(embed_dim, num_classes)
        self.preprocessor = clip_preprocess

        # 3) Load the classifier weights if available
        try:
            state_dict = torch.load(model_path, map_location=device)
            self.load_state_dict(state_dict)
        except FileNotFoundError:
            print(f"Warning: No classifier weights found at {model_path}.")

        self.to(device)

    def forward(self, images):
        # 1) Preprocess
        # images = self.preprocessor(images)
        # 2) Encode with CLIP (frozen)
        with torch.no_grad():
            embeddings = self.clip_model.encode_image(images)
        # 3) Convert to float32 and run the linear head
        embeddings = embeddings.float()
        return self.classifier(embeddings)

class ResNetBinaryClassifier(BinaryClassifier):
    """
    A binary classifier using ResNet-18 with 2 outputs.
    Attempts to load weights from 'models/resnet18_cnn.pth'.
    """
    def __init__(self, device=None, model_path="models/resnet18_cnn.pth"):
        super().__init__()
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        # 1) Basic transforms
        self.preprocessor = T.Compose([
            T.Resize(256),
            T.CenterCrop(224),
            T.ToTensor()
        ])

        # 2) Build a ResNet-18 for 2 classes
        resnet = models.resnet18(pretrained=False)
        num_ftrs = resnet.fc.in_features
        resnet.fc = nn.Linear(num_ftrs, 2)
        resnet.eval()
        self.resnet = resnet

        # 3) Load weights if available
        try:
            loaded_state = torch.load(model_path, map_location=device)
            self.resnet.load_state_dict(loaded_state)
        except FileNotFoundError:
            print(f"Warning: No ResNet weights found at {model_path}.")

        self.to(device)

    def forward(self, images):
        # 1) Preprocess
        #images = self.preprocessor(images)
        # 2) Forward pass
        return self.resnet(images)