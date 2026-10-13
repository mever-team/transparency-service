import csv
import json
from pathlib import Path


def percentage(value):
    return f"{value * 100:.2f}%"


def print_summary(aggregate):

    print()
    print("=" * 75)
    print("MODEL CARD JSON CLASSIFICATION EVALUATION")
    print("=" * 75)

    print(
        f"Files evaluated:              "
        f"{aggregate['files']}"
    )

    print(
        f"Ground-truth paragraphs:      "
        f"{aggregate['total_gt']}"
    )

    print(
        f"Matched paragraphs:           "
        f"{aggregate['matched']}"
    )

    print(
        f"Missing paragraphs:           "
        f"{aggregate['missing']}"
    )

    print(
        f"Predicted paragraphs:         "
        f"{aggregate['predicted_total']}"
    )

    print(
        f"Extra paragraphs:             "
        f"{aggregate['extra']}"
    )

    print()

    print(
        f"Paragraph recall:             "
        f"{percentage(aggregate['paragraph_recall'])}"
    )

    print(
        f"Classification accuracy:      "
        f"{percentage(aggregate['classification_accuracy'])}"
    )

    print(
        f"Correct classification rate:  "
        f"{percentage(aggregate['correct_classification_rate'])}"
    )

    print(
        f"Extra paragraph rate:         "
        f"{percentage(aggregate['extra_rate'])}"
    )

    print()
    print("-" * 75)
    print("FIELD-LEVEL METRICS")
    print("-" * 75)

    print(
        f"{'Field':40}"
        f"{'Precision':>11}"
        f"{'Recall':>11}"
        f"{'F1':>11}"
    )

    for field, values in aggregate[
        "field_metrics"
    ].items():

        print(
            f"{field:40}"
            f"{percentage(values['precision']):>11}"
            f"{percentage(values['recall']):>11}"
            f"{percentage(values['f1']):>11}"
        )

    print()
    print("-" * 75)
    print("MISCLASSIFICATIONS")
    print("-" * 75)

    for key, count in aggregate[
        "confusion_matrix"
    ].items():

        gt, pred = key.split(
            " -> ",
            1,
        )

        if gt != pred:
            print(
                f"{gt:40} -> "
                f"{pred:40} "
                f"{count:>5}"
            )


def save_json(data, path: Path):

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2,
        )


def save_mismatches(
    file_results,
    path: Path,
):
    """
    Save misclassified, missing and extra paragraphs
    for manual inspection.
    """

    rows = []

    for file_result in file_results:

        filename = file_result["filename"]
        result = file_result["result"]

        for match in result["matches"]:

            if match["status"] != "misclassified":
                continue

            rows.append({
                "file": filename,
                "status": "misclassified",

                "gt_field": match["gt_field"],
                "pred_field": match["pred_field"],

                "similarity": match["similarity"],

                "gt_text": match["gt_text"],
                "pred_text": match["pred_text"],
            })

        for paragraph in result["missing"]:

            rows.append({
                "file": filename,
                "status": "missing",

                "gt_field": paragraph["field"],
                "pred_field": "",

                "similarity": "",

                "gt_text": paragraph["text"],
                "pred_text": "",
            })

        for paragraph in result["extra"]:

            rows.append({
                "file": filename,
                "status": "extra",

                "gt_field": "",
                "pred_field": paragraph["field"],

                "similarity": "",

                "gt_text": "",
                "pred_text": paragraph["text"],
            })

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "file",
                "status",
                "gt_field",
                "pred_field",
                "similarity",
                "gt_text",
                "pred_text",
            ],
        )

        writer.writeheader()
        writer.writerows(rows)


def save_confusion_matrix(
    aggregate,
    path: Path,
):

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fields = sorted(
        aggregate["field_metrics"]
    )

    matrix = {}

    for key, count in aggregate[
        "confusion_matrix"
    ].items():

        gt, pred = key.split(
            " -> ",
            1,
        )

        matrix.setdefault(gt, {})
        matrix[gt][pred] = count

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            ["GT \\ Prediction"] + fields
        )

        for gt in fields:

            writer.writerow([
                gt,
                *[
                    matrix.get(
                        gt,
                        {},
                    ).get(pred, 0)
                    for pred in fields
                ],
            ])