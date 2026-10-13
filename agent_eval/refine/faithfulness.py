import json
import requests

from config import JUDGE_MODEL, OLLAMA_URL, RESULTS_PATH


FAITHFULNESS_RESULTS_PATH = "faithfulness_results.json"


FAITHFULNESS_PROMPT = """
You are evaluating the factual faithfulness of an AI-generated explanation.

The SOURCE is the only evidence available for evaluating factual claims
about the specific model.

Your task is to:

1. Extract the atomic factual claims made in the GENERATED EXPLANATION.
2. Compare each claim against the SOURCE.
3. Classify every claim as SUPPORTED, PARTIAL, UNSUPPORTED, or CONTRADICTION.

SOURCE:
{source}

GENERATED EXPLANATION:
{prediction}

IMPORTANT RULES:

1. Extract atomic factual claims.

If one sentence contains multiple factual claims, split them into
separate claims.

For example:

"The model uses X and X improves performance."

should produce two claims:

- "The model uses X."
- "X improves performance."

2. SUPPORTED

Use SUPPORTED when the claim is directly stated or logically entailed
by the SOURCE.

Simple paraphrasing is SUPPORTED.

Example:

SOURCE:
"The model uses a 196B-parameter language backbone."

CLAIM:
"The model has a language backbone with 196 billion parameters."

VERDICT:
SUPPORTED

3. PARTIAL

Use PARTIAL when the claim is based on information in the SOURCE but
adds a specific detail that is not supported by the SOURCE.

Example:

SOURCE:
"The model uses stochastic latent synthesis."

CLAIM:
"The model uses stochastic latent synthesis to introduce random
variations."

VERDICT:
PARTIAL

The source supports the use of stochastic latent synthesis, but does
not establish the additional explanation about how it works.

4. UNSUPPORTED

Use UNSUPPORTED when the claim introduces a model-specific factual
statement that is not stated or logically entailed by the SOURCE.

Examples include unsupported claims about:

- performance
- accuracy
- quality
- benefits
- advantages
- training methods
- training data
- capabilities
- limitations
- mechanisms
- reasons for using a component
- effects of a component
- comparisons with other models

Example:

SOURCE:
"The model uses residual coupling flow."

CLAIM:
"Residual coupling flow improves the model's performance."

VERDICT:
UNSUPPORTED

The SOURCE says that the model uses the component but does not state
that it improves performance.

5. CONTRADICTION

Use CONTRADICTION when the claim conflicts with information in the
SOURCE.

Example:

SOURCE:
"The model combines a 196B-parameter language backbone with a
1.8B-parameter vision encoder."

CLAIM:
"The vision encoder is larger than the language backbone."

VERDICT:
CONTRADICTION

6. GENERAL TECHNICAL DEFINITIONS

Do NOT mark a claim UNSUPPORTED merely because it provides a general
definition or clarification of a technical term.

For example:

SOURCE:
"The model uses ASR."

CLAIM:
"ASR stands for Automatic Speech Recognition."

This is a general definition and should not automatically be considered
an unsupported model-specific claim.

Similarly:

SOURCE:
"The model has 198 billion parameters."

CLAIM:
"Parameters are numerical values used by a neural network."

This is a general technical explanation and should not automatically
be considered unsupported.

However, if the explanation makes a claim specifically about the
model, evaluate that claim against the SOURCE.

Example:

CLAIM:
"The model's parameters were trained using supervised learning."

This is a model-specific claim and must be supported by the SOURCE.

7. DO NOT USE EXTERNAL KNOWLEDGE

Do not use your own knowledge about the model, architecture, technology,
or terminology to establish that a model-specific claim is true.

The SOURCE is the evidence for model-specific factual claims.

8. DO NOT PENALIZE EXPLANATORY WORDING

Do not penalize wording that merely makes the SOURCE easier to understand.

For example:

SOURCE:
"196B-parameter language backbone"

CLAIM:
"The model contains a large language component with 196 billion
parameters."

This should be SUPPORTED.

9. BENEFITS AND PERFORMANCE

Be particularly strict with claims about benefits, quality, or
performance.

If the SOURCE says that a component is used, this does NOT imply that
the component improves performance, quality, efficiency, accuracy,
naturalness, or any other property.

10. CLAIMS ABOUT OTHER MODELS

Claims comparing the model with other models should only be SUPPORTED
if the comparison is present or logically entailed by the SOURCE.

11. OMMISSIONS

Do not penalize the GENERATED EXPLANATION for failing to mention
information from the SOURCE.

This evaluation only measures whether claims that ARE made are
supported.

12. VERDICT PRIORITY

If a claim clearly contradicts the SOURCE, use CONTRADICTION.

If it is not contradicted but contains an unsupported additional
model-specific detail, use PARTIAL when the core claim is supported
and UNSUPPORTED when the claim as a whole introduces unsupported
information.

Return ONLY valid JSON.

Use exactly this format:

{{
    "claims": [
        {{
            "claim": "atomic factual claim",
            "verdict": "SUPPORTED",
            "evidence": "relevant information from the SOURCE",
            "reason": "brief explanation of the verdict"
        }}
    ]
}}

Allowed verdicts:

SUPPORTED
PARTIAL
UNSUPPORTED
CONTRADICTION
"""


def judge_faithfulness(source, prediction):
    """Use the LLM judge to evaluate claims in a prediction."""

    prompt = FAITHFULNESS_PROMPT.format(
        source=source,
        prediction=prediction
    )

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": JUDGE_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        },
        timeout=300
    )

    response.raise_for_status()

    result = response.json()

    return json.loads(result["response"])


def calculate_faithfulness_metrics(claims):
    """Calculate factual faithfulness metrics."""

    supported = sum(
        1 for claim in claims
        if claim.get("verdict") == "SUPPORTED"
    )

    partial = sum(
        1 for claim in claims
        if claim.get("verdict") == "PARTIAL"
    )

    unsupported = sum(
        1 for claim in claims
        if claim.get("verdict") == "UNSUPPORTED"
    )

    contradiction = sum(
        1 for claim in claims
        if claim.get("verdict") == "CONTRADICTION"
    )

    total = len(claims)

    if total == 0:
        return {
            "total_claims": 0,
            "supported_claims": 0,
            "partial_claims": 0,
            "unsupported_claims": 0,
            "contradiction_claims": 0,
            "factual_faithfulness": 0.0,
            "unsupported_claim_rate": 0.0
        }

    factual_faithfulness = (
        supported + 0.5 * partial
    ) / total

    unsupported_claim_rate = (
        unsupported + contradiction
    ) / total

    return {
        "total_claims": total,
        "supported_claims": supported,
        "partial_claims": partial,
        "unsupported_claims": unsupported,
        "contradiction_claims": contradiction,
        "factual_faithfulness": factual_faithfulness,
        "unsupported_claim_rate": unsupported_claim_rate
    }


def evaluate_sample(sample):
    """Evaluate one sample."""

    source = sample["input"]
    prediction = sample["prediction"]

    result = judge_faithfulness(
        source,
        prediction
    )

    claims = result.get("claims", [])

    metrics = calculate_faithfulness_metrics(claims)

    return {
        "id": sample["id"],
        "source": sample["source"],
        "metrics": metrics,
        "claims": claims
    }


def main():

    print("=" * 60)
    print("FAITHFULNESS EVALUATION")
    print("=" * 60)

    # -------------------------
    # 1. Load existing results
    # -------------------------

    with open(RESULTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    samples = data["samples"]

    # -------------------------
    # 2. Evaluate samples
    # -------------------------

    results = []

    for i, sample in enumerate(samples):

        print(
            f"Evaluating sample "
            f"{i + 1}/{len(samples)}",
        )

        result = evaluate_sample(sample)

        results.append(result)

    print()

    # -------------------------
    # 3. Calculate overall metrics
    # -------------------------

    all_claims = []

    for result in results:
        all_claims.extend(result["claims"])

    overall_metrics = calculate_faithfulness_metrics(
        all_claims
    )

    # -------------------------
    # 4. Save results
    # -------------------------

    output = {
        "metrics": overall_metrics,
        "samples": results
    }

    with open(
        FAITHFULNESS_RESULTS_PATH,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            output,
            f,
            indent=2,
            ensure_ascii=False
        )

    # -------------------------
    # 5. Print summary
    # -------------------------

    print()
    print("=" * 60)
    print("FAITHFULNESS SUMMARY")
    print("=" * 60)

    print(
        f"Total claims: "
        f"{overall_metrics['total_claims']}"
    )

    print(
        f"Supported: "
        f"{overall_metrics['supported_claims']}"
    )

    print(
        f"Partial: "
        f"{overall_metrics['partial_claims']}"
    )

    print(
        f"Unsupported: "
        f"{overall_metrics['unsupported_claims']}"
    )

    print(
        f"Contradictions: "
        f"{overall_metrics['contradiction_claims']}"
    )

    print(
        f"Factual faithfulness: "
        f"{overall_metrics['factual_faithfulness'] * 100:.2f}%"
    )

    print(
        f"Unsupported claim rate: "
        f"{overall_metrics['unsupported_claim_rate'] * 100:.2f}%"
    )

    print("=" * 60)

    print(
        f"Saved results to: "
        f"{FAITHFULNESS_RESULTS_PATH}"
    )


if __name__ == "__main__":
    main()