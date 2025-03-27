import json

from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input

import shap

import transparency_service

# load pre-trained model and data
model = ResNet50(weights="imagenet")
X, y = shap.datasets.imagenet50()

# getting ImageNet 1000 class names
url = "https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json"
with open(shap.datasets.cache(url)) as file:
    class_names = [v[1] for v in json.load(file).values()]
# print("Number of ImageNet classes:", len(class_names))
# print("Class names:", class_names)

def f(x):
    tmp = x.copy()
    preprocess_input(tmp)
    return model(tmp)


transparency_service.explainers.shap.image.classification.explainer(f, X[1:3], output_names = class_names)