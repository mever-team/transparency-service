import json

from aicard.service.assistants.prompter import Prompter
from aicard.agents import Ollama
from aicard.service.logger import Logger

from config import MODEL_NAME


logger = Logger()

prompter = Prompter(
    Ollama(
        MODEL_NAME,
        name="🌬️ Mistral",
        timeout_secs=45
    )
)


def load_dataset(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def infer_sample(text):
    output = ""

    for chunk in prompter.refine_field(text, logger):
        chunk = json.loads(chunk)
        output += chunk["message"]["content"]

    return output


def run_inference(dataset):
    results = []

    for i, sample in enumerate(dataset):
        print(f"Inference {i + 1}/{len(dataset)}")

        prediction = infer_sample(sample["input"])

        results.append({
            "id": sample["id"],
            "input": sample["input"],
            "prediction": prediction,
            "checklist": sample["ground_truth"],
            "source": sample["source"]
        })

    return results