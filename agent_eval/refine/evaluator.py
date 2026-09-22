import requests
import json

from config import OLLAMA_URL, JUDGE_MODEL


def judge_requirement(
    input_text,
    prediction,
    requirement,
    requirement_type
):
    prompt = f"""
You are evaluating an AI model's explanation
of a technical sentence for non-AI experts.

Original sentence:
{input_text}

Model output:
{prediction}

Requirement type:
{requirement_type}

Requirement:
{requirement}

Evaluate the model output using TWO separate criteria.

1. INFORMATION PRESENT

Determine whether the information required by the requirement
is present in the model output.

Return:

YES:
The required information is present.

NO:
The required information is absent.

2. SATISFACTION

Determine how well the model output satisfies the requirement.

Return:

YES:
The requirement is fully satisfied.

PARTIAL:
Some of the required information or explanation is present,
but the requirement is not fully satisfied.

NO:
The requirement is not satisfied.

Evaluation rules:

For "mention" requirements:
- Check whether the required concept or fact is present.
- Different wording is acceptable if the meaning is preserved.
- Do not require additional explanation.
- If the concept is present, satisfaction is normally YES.
- If the concept is absent, information_present must be NO
  and satisfaction must be NO.

For "explain" requirements:
- The required concept must be present.
- The concept must be explained clearly enough for a non-expert.
- Merely mentioning the technical term is not sufficient.
- If the concept is mentioned but the explanation is insufficient,
  information_present can be YES while satisfaction is PARTIAL.
- If the required concept is completely absent,
  information_present must be NO and satisfaction must be NO.
- If the explanation fully addresses the requirement,
  satisfaction is YES.

For "constraint" requirements:
- Check whether the required constraint is respected by the output.
- If the constraint is respected, satisfaction is YES.
- If it is partially respected, satisfaction is PARTIAL.
- If it is violated, satisfaction is NO.
- Determine information_present based on whether the relevant
  information needed to evaluate the constraint is present.

The model output should be evaluated against the requirement,
not against what you personally think would make a good explanation.

Do not penalize different wording when the meaning is preserved.

Return ONLY valid JSON in exactly this format:

{{
    "information_present": "YES",
    "satisfaction": "YES",
    "reason": "Short explanation of the evaluation."
}}

Allowed values for information_present:
YES
NO

Allowed values for satisfaction:
YES
PARTIAL
NO
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": JUDGE_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0
            }
        },
        timeout=120
    )

    response.raise_for_status()

    result = json.loads(
        response.json()["response"]
    )

    return result


def evaluate_sample(sample):
    checklist_results = []

    for item in sample["checklist"]:

        result = judge_requirement(
            sample["input"],
            sample["prediction"],
            item["requirement"],
            item["type"]
        )

        checklist_results.append({
            "id": item["id"],
            "type": item["type"],
            "requirement": item["requirement"],
            "information_present": (
                result["information_present"] == "YES"
            ),
            "satisfaction": result["satisfaction"],
            "reason": result["reason"]
        })

    return checklist_results