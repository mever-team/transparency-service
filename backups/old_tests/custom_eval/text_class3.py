# Step 1: Load dataset
from datasets import load_dataset

dataset = load_dataset("lytang/LLM-AggreFact")
data_test = dataset["test"]
splits = [
    "AggreFact-CNN",  # 558
    "FactCheck-GPT",  # 1566
    "Lfqa",  # 1911
    "ClaimVerify",  # 1088
    "Wice",  # 358
    "RAGTruth",  # 16371
    "AggreFact-XSum",  # 558
    "ExpertQA",  # 3702
    "TofuEval-MediaS",  # 726
    "Reveal",  # 1710
    "TofuEval-MeetB",  # 772
]

# Step 2: Load model
from transformers import pipeline

classifier = pipeline("text-classification", model="VinMir/GordonAI-fact_checking")


# Step 3: Define pipeline
def pl(data):
    claims = [sample for sample in data["claim"]]
    docs = [sample for sample in data["doc"]]
    input = [claim + doc for claim, doc in zip(claims, docs)]

    response = classifier(input)

    scores = []
    for dict in response:
        scores.append(
            dict["score"] if dict["label"] == "TrueNews" else 1 - dict["score"]
        )

    return scores


from aicard import evaluation

split_dataset = [data_test.filter(lambda x: x["dataset"] == split) for split in splits]
for split, split_name in zip(split_dataset, splits):
    metrics = evaluation.run(
        data=split, pipeline=pl, task="Text Classification", batch_size=4
    )
    print({"model": "GordonAI", "dataset": split_name} | metrics)
