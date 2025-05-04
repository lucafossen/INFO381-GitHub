import torch
import torch.nn as nn
# 5) Create a simple classifier head for the CLIP embeddings.
#    CLIP's ViT-B/32 has a default embedding dimension of 512.

class CLIPClassifier(nn.Module):
    def __init__(self, clip_model, embed_dim=512, num_classes=2):
        super().__init__()
        self.clip_model = clip_model
        self.classifier = nn.Linear(embed_dim, num_classes)

    def forward(self, images):
        with torch.no_grad():
            image_embeddings = self.clip_model.encode_image(images)
        image_embeddings = image_embeddings.float()  # cast to float32
        return self.classifier(image_embeddings)