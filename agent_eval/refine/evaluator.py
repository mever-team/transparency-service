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
The required information is conveyed by the output, either explicitly or
through an equivalent description or explanation. The exact terminology
does not need to appear if the meaning is clearly present.

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
- Check whether the required concept or fact is present in the output.
- Different wording is acceptable if the meaning is preserved.
- The required information does NOT need to explicitly name the concept
  if the output clearly conveys the required information through its
  description or explanation.
- Do not require additional explanation.
- If the required information is present, even without explicitly naming
  the concept, information_present is YES.
- If the concept or its required information is absent, information_present
  must be NO and satisfaction must be NO.
- If the required information is present, satisfaction is normally YES.

For "explain" requirements:
- Check whether the required concept is explained, not merely whether its
  exact name appears.
- The concept does NOT need to be explicitly named if the output clearly
  conveys the required explanation or definition.
- For example, if the requirement is:
  "Explains that phonemes are the basic sound units used to represent
  spoken language."
  an output such as:
  "They are the basic sound units used to represent spoken language."
  contains the required explanation even though the word "phonemes" does
  not appear explicitly.
- If the required information or explanation can be clearly understood
  from the output without the technical term being explicitly stated,
  information_present is YES.
- The concept must still be explained clearly enough for a non-expert.
- Merely mentioning the technical term is not sufficient.
- If the concept or explanation is partially conveyed, information_present
  can be YES while satisfaction is PARTIAL.
- If the required information is completely absent, information_present
  must be NO and satisfaction must be NO.
- If the explanation fully addresses the requirement, satisfaction is YES.
  
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