from config import DATASET_PATH, RESULTS_PATH

from inference import load_dataset, run_inference
from evaluator import evaluate_sample
from metrics import calculate_sample_metrics, calculate_overall_metrics
from reports import save_json, print_summary


def main():

    # -------------------------
    # 1. Load dataset
    # -------------------------

    dataset = load_dataset(DATASET_PATH)

    # -------------------------
    # 2. Run Mistral
    # -------------------------

    predictions = run_inference(dataset)

    # -------------------------
    # 3. Evaluate checklist
    # -------------------------

    results = []

    for i, sample in enumerate(predictions):

        print(
            f"\rEvaluating sample "
            f"{i + 1}/{len(predictions)}", end="", flush=True
        )

        checklist_results = evaluate_sample(sample)

        sample_metrics = calculate_sample_metrics(
            checklist_results
        )

        results.append({
            **sample,
            "checklist_results": checklist_results,
            "metrics": sample_metrics
        })

    # -------------------------
    # 4. Overall metrics
    # -------------------------

    overall_metrics = calculate_overall_metrics(results)

    # -------------------------
    # 5. Save results
    # -------------------------

    output = {
        "metrics": overall_metrics,
        "samples": results
    }

    save_json(output, RESULTS_PATH)

    # -------------------------
    # 6. Print summary
    # -------------------------

    print_summary(overall_metrics)


if __name__ == "__main__":
    main()