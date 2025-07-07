# Step 1: Load model
from src.utils import get_transforms, get_our_trained_model, get_generators

generators = get_generators()
_, transform, _ = get_transforms()
device = "cuda:0"
model = get_our_trained_model(ncls=1, device=device)
model.to(device)

# Step 2: Define data path
data_path = "./dataset.csv"  # image, label -> path, int

# Step 2: Create pipeline
from PIL import Image
from torch import tensor
import torch


def pipeline(data):
    images = [Image.open(path).convert("RGB") for path in data["image"]]  # Open
    images = [transform(img) for img in images]  # Transform
    images = torch.stack(images).to(
        device
    )  # To GPU # shape = batch_size, 3, width, hight
    with torch.no_grad():
        outputs = model(images)[0].squeeze()  # shape = batch_size
    return outputs.cpu().tolist()


# Step 3: Run evaluation
from transparency import evaluation

metrics = evaluation.run(
    data=data_path, pipeline=pipeline, task="Image Classification", batch_size=32
)
print(metrics)
