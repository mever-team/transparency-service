from config import (
    GT_DIR,
    PRED_DIR,
    REPORT_DIR,
    MATCH_THRESHOLD,
    EXCLUDED_FIELDS,
    MIN_PREDICTION_LENGTH,
    REPORT_FILE,
    HTML_REPORT
)
from html_out import generate_html

from loader import (
    load_json,
    find_file_pairs,
)

from extractor import (
    extract_paragraphs,
)

from matcher import (
    match_predictions,
)

from metrics import (
    calculate_metrics,
    aggregate_metrics,
)

from log import print_metrics


def main():

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    pairs = find_file_pairs(
        GT_DIR,
        PRED_DIR,
    )

    results = []
    detailed_results = []
    with REPORT_FILE.open("w", encoding="utf-8") as report:
        for pair in pairs:

            # print()
            # print("=" * 70)
            # print(pair["name"])
            # print("=" * 70)

            if pair["pred_path"] is None:

                print("Prediction file missing.")

                continue

            gt_card = load_json(
                pair["gt_path"]
            )

            pred_card = load_json(
                pair["pred_path"]
            )

            gt_paragraphs = extract_paragraphs(
                gt_card,
                EXCLUDED_FIELDS,
            )

            pred_paragraphs = extract_paragraphs(
                pred_card,
                EXCLUDED_FIELDS,
            )
            
            pred_paragraphs = [
                p for p in pred_paragraphs
                if len(p["text"]) >= MIN_PREDICTION_LENGTH
            ]

            result = match_predictions(
                gt_paragraphs,
                pred_paragraphs,
                MATCH_THRESHOLD
            )
            # print("\n--- UNMATCHED PREDICTED SENTENCES ---")

            # for extra in result["extra"]:
            #     print(
            #         f"[{extra['pred_field']}]\n"
            #         f"{extra['pred_text']}\n"
            #         f"Best similarity: {extra['similarity']}\n"
            #     )
            metrics = calculate_metrics(
                result
            )

            results.append(metrics)
            detailed_results.append({ "name": pair["name"], "result": result,})
            print_metrics(pair['name'], metrics, result, file=report)

        if not results:
            print("No files were evaluated.")
            return

        aggregate = aggregate_metrics(results)

        print_metrics("ACCUMULATED RESULTS", aggregate, file=report)

        generate_html(detailed_results, HTML_REPORT, aggregate["confusion_matrix"])


if __name__ == "__main__":
    main()