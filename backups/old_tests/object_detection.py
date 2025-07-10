import modelcard
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
import json
from pycocotools.coco import COCO

device = "cuda:0"

processor = DetrImageProcessor.from_pretrained(
    "facebook/detr-resnet-50", revision="no_timm"
)


def preprocessor(image):
    out = processor(images=image, return_tensors="pt")
    return out


class custommodel(torch.nn.Module):
    def __init__(self):
        super(custommodel, self).__init__()
        self.model = DetrForObjectDetection.from_pretrained(
            "facebook/detr-resnet-50", revision="no_timm"
        )

    def forward(self, input_ids):
        return self.model(**input_ids)


def postprocessor(model_output, image_size):
    return processor.post_process_object_detection(
        model_output, target_sizes=torch.tensor([image_size[::-1]]), threshold=0.9
    )[0]


mymodel = custommodel()

annFile = "/home/gnikoul/fiftyone/coco-2017/raw/instances_val2017.json"
coco = COCO(annFile)
imgIds = coco.getImgIds()
imgIds = imgIds[0:9]
data = []
for i in range(len(imgIds)):
    img = coco.loadImgs(imgIds[i])[0]
    annIds = coco.getAnnIds(imgIds=img["id"])
    anns = coco.loadAnns(annIds)  # get annotations for each image
    imgdata = {"url": img["coco_url"], "anns": anns}
    data.append(imgdata)
    print(data)
    input("see")


metrics = modelcard.evaluation.evaluate(
    model=mymodel,
    preprocessor=preprocessor,
    postprocessor=postprocessor,
    path="/home/gnikoul/fiftyone/coco-2017/validation/data",
    target_box_format="xyhw",
    predict_box_format="xyxy",
    target_iou="bbox",
    predict_iou="boxes",
    target_labels="category_id",
    predict_labels="labels",
    scores="scores",
)
