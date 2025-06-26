# Step 1: Load model
from transformers import DetrImageProcessor, DetrForObjectDetection

device = "cuda:0"
processor = DetrImageProcessor.from_pretrained(
    "facebook/detr-resnet-50", revision="no_timm"
)
model = DetrForObjectDetection.from_pretrained(
    "facebook/detr-resnet-50", revision="no_timm"
).to(device)

# Step 2: Load data
from pycocotools.coco import COCO
import os

annFile = os.path.expanduser("coco-2017/instances_val2017.json")
coco = COCO(annFile)
imgIds = coco.getImgIds()
img = coco.loadImgs(imgIds)
annIds = [coco.getAnnIds(imgIds=imgId) for imgId in imgIds]
anns = [coco.loadAnns(annId) for annId in annIds]
# len(img) len(anns) 5000
for i in range(len(anns) - 1, -1, -1):  # Remove REL, keep only polygonal segm
    for j in range(len(anns[i])):
        if isinstance(anns[i][j]["segmentation"], dict):
            del anns[i]
            del img[i]
            break
# len(img) len(anns) 4589

# Step 5: Define pipeline
from PIL import Image
import requests
import torch


def pipeline(data):
    urls = [url for url in data["coco_url"]]
    images = [
        Image.open(requests.get(url, stream=True).raw).convert("RGB") for url in urls
    ]
    inputs = processor(images=images, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    target_sizes = torch.tensor([image.size[::-1] for image in images])
    results = processor.post_process_object_detection(
        outputs, target_sizes=target_sizes, threshold=0.9
    )
    return results


# Step 4: Run evaluation
from transparency_service import evaluation

metrics = evaluation.run(
    data=img, pipeline=pipeline, anns=anns, task="Object Detection", batch_size=4
)
print(metrics)
