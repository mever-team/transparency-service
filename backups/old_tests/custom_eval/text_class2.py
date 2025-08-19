# Step 1: Load Data Set
from datasets import load_dataset

dataset = load_dataset("google-research-datasets/go_emotions", split="test")

# Step 2: Load metadata
from huggingface_hub import dataset_info

info = dataset_info("google-research-datasets/go_emotions")
class_names = info.card_data["dataset_info"][1]["features"][1]["sequence"][
    "class_label"
]["names"]

# Step 3: Load model
from transformers import pipeline

classifier = pipeline(
    task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None
)


# Step 4: Create pipeline
def pipeline(data):
    sentences = [text for text in data["text"]]
    model_outputs = classifier(sentences)
    out = []
    for sample in model_outputs:
        flat = {d["label"]: d["score"] for d in sample}
        out.append([flat[name] for name in class_names.values()])
    return out


# Step 5: Run evaluation
from aicard import evaluation

metrics = evaluation.run(
    data=dataset, pipeline=pipeline, task="Text Classification", batch_size=32
)
print(metrics)
