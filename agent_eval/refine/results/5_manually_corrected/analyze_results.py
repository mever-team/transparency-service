import json
from collections import defaultdict
from pathlib import Path


RESULTS_PATH = "evaluation_results.json"
REPORT_PATH = "analysis_report.json"


def calculate_metrics(items):
    """Calculate metrics for a collection of checklist results."""

    total = len(items)

    information_present = sum(
        1
        for item in items
        if item["information_present"]
    )

    fully_satisfied = sum(
        1
        for item in items
        if item["satisfaction"] == "YES"
    )

    partially_satisfied = sum(
        1
        for item in items
        if item["satisfaction"] == "PARTIAL"
    )

    not_satisfied = sum(
        1
        for item in items
        if item["satisfaction"] == "NO"
    )

    information_presence = (
        information_present / total
        if total
        else 0.0
    )

    satisfaction_score = (
        (
            fully_satisfied
            + 0.5 * partially_satisfied
        ) / total
        if total
        else 0.0
    )

    return {
        "total_requirements": total,

        "information_present": information_present,
        "information_presence": information_presence,

        "fully_satisfied": fully_satisfied,
        "partially_satisfied": partially_satisfied,
        "not_satisfied": not_satisfied,

        "satisfaction_score": satisfaction_score,
    }


def calculate_type_metrics(checklist, checklist_results):
    """
    Match checklist types with checklist results using the checklist item ID.
    """

    type_by_id = {
        item["id"]: item["type"]
        for item in checklist
    }

    grouped_items = defaultdict(list)

    for result in checklist_results:

        item_type = type_by_id.get(
            result["id"],
            "unknown"
        )

        grouped_items[item_type].append({
            **result,
            "type": item_type,
        })

    return {
        item_type: calculate_metrics(items)
        for item_type, items in grouped_items.items()
    }


def calculate_overall_metrics(samples):
    """Calculate overall and per-type metrics across all samples."""

    all_items = []
    items_by_type = defaultdict(list)

    for sample in samples:

        type_by_id = {
            item["id"]: item["type"]
            for item in sample["checklist"]
        }

        for result in sample["checklist_results"]:

            item_type = type_by_id.get(
                result["id"],
                "unknown"
            )

            enriched_result = {
                **result,
                "type": item_type,
            }

            all_items.append(enriched_result)
            items_by_type[item_type].append(
                enriched_result
            )

    return {
        "overall": calculate_metrics(all_items),

        "by_type": {
            item_type: calculate_metrics(items)
            for item_type, items in items_by_type.items()
        },
    }


def analyze_samples(samples):
    """Calculate metrics for each individual sample."""

    analyzed_samples = []

    for sample in samples:

        type_metrics = calculate_type_metrics(
            sample["checklist"],
            sample["checklist_results"],
        )

        overall_metrics = calculate_metrics(
            sample["checklist_results"]
        )

        analyzed_samples.append({
            "id": sample["id"],
            "source": sample["source"],
            "metrics": {
                "overall": overall_metrics,
                "by_type": type_metrics,
            },
        })

    return analyzed_samples


def print_metrics(title, metrics):
    """Print metrics in a readable format."""

    print(f"\n{title}")
    print("-" * len(title))

    total = metrics["total_requirements"]

    print(
        f"Total requirements: "
        f"{total}"
    )

    print(
        f"Information present: "
        f"{metrics['information_present']} / {total} "
        f"({metrics['information_presence'] * 100:.2f}%)"
        if total
        else "Information present: 0 / 0 (0.00%)"
    )

    print(
        f"Fully satisfied: "
        f"{metrics['fully_satisfied']} / {total} "
        f"({metrics['fully_satisfied'] / total * 100:.2f}%)"
        if total
        else "Fully satisfied: 0 / 0 (0.00%)"
    )

    print(
        f"Partially satisfied: "
        f"{metrics['partially_satisfied']} / {total} "
        f"({metrics['partially_satisfied'] / total * 100:.2f}%)"
        if total
        else "Partially satisfied: 0 / 0 (0.00%)"
    )

    print(
        f"Not satisfied: "
        f"{metrics['not_satisfied']} / {total} "
        f"({metrics['not_satisfied'] / total * 100:.2f}%)"
        if total
        else "Not satisfied: 0 / 0 (0.00%)"
    )

    print(
        f"Satisfaction score: "
        f"{metrics['satisfaction_score'] * 100:.2f}%"
    )


def print_report(report):
    """Print the complete analysis report."""

    print("\n" + "=" * 60)
    print("EVALUATION ANALYSIS")
    print("=" * 60)

    # -------------------------
    # Overall
    # -------------------------

    print_metrics(
        "Overall",
        report["overall_metrics"]["overall"],
    )

    # -------------------------
    # By type
    # -------------------------

    print("\n" + "=" * 60)
    print("METRICS BY REQUIREMENT TYPE")
    print("=" * 60)

    for item_type in (
        "mention",
        "explain",
        "constraint",
    ):

        if item_type in report["overall_metrics"]["by_type"]:

            print_metrics(
                item_type.capitalize(),
                report["overall_metrics"]["by_type"][item_type],
            )

    # -------------------------
    # Per sample
    # -------------------------

    print("\n" + "=" * 60)
    print("PER-SAMPLE METRICS")
    print("=" * 60)

    for sample in report["samples"]:

        print(f"\nSample {sample['id']}")
        print(f"Source: {sample['source']}")

        print_metrics(
            "Overall",
            sample["metrics"]["overall"],
        )

        for item_type in (
            "mention",
            "explain",
            "constraint",
        ):

            if item_type in sample["metrics"]["by_type"]:

                print_metrics(
                    item_type.capitalize(),
                    sample["metrics"]["by_type"][item_type],
                )


def main():

    results_path = Path(RESULTS_PATH)
    report_path = Path(REPORT_PATH)

    if not results_path.exists():
        raise FileNotFoundError(
            f"Results file not found: {results_path}"
        )

    with results_path.open(
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    samples = data["samples"]

    report = {
        "overall_metrics": calculate_overall_metrics(
            samples
        ),
        "samples": analyze_samples(
            samples
        ),
    }

    with report_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print_report(report)

    print("\n" + "=" * 60)
    print(
        f"Saved analysis report to: "
        f"{report_path}"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()