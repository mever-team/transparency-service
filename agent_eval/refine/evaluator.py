import requests
import json

from config import OLLAMA_URL, JUDGE_MODEL


def judge_requirement(input_text, prediction, requirement):

    prompt = f"""
You are evaluating an AI model's explanation of a technical sentence.

Original sentence:
{input_text}

Model output:
{prediction}

Evaluation requirement:
{requirement}

Determine whether the model output satisfies the evaluation requirement.

Rules:
- Answer YES only if the requirement is clearly satisfied.
- Answer NO if the requirement is missing, incorrect, or substantially incomplete.
- Judge the meaning, not exact wording.
- Do not give credit just because related words appear.
- Do not penalize different wording when the meaning is correct.

Return ONLY:
YES
or
NO
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": JUDGE_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0
            }
        },
        timeout=120
    )

    response.raise_for_status()

    result = response.json()["response"].strip().upper()

    if result.startswith("YES"):
        return True

    return False


def evaluate_sample(sample):
    checklist_results = []

    for item in sample["checklist"]:
        satisfied = judge_requirement(
            sample["input"],
            sample["prediction"],
            item["requirement"]
        )

        checklist_results.append({
            "id": item["id"],
            "requirement": item["requirement"],
            "satisfied": satisfied
        })

    return checklist_results