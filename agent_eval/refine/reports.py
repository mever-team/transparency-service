import json


def save_json(results, path):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            results,
            f,
            indent=2,
            ensure_ascii=False
        )


def print_metrics(title, metrics):

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


def print_summary(metrics):

    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)

    # -------------------------
    # Overall
    # -------------------------

    print_metrics(
        "Overall",
        metrics
    )

    # -------------------------
    # By requirement type
    # -------------------------

    for item_type in (
        "mention",
        "explain",
        "constraint"
    ):

        if item_type in metrics["by_type"]:

            print_metrics(
                item_type.capitalize(),
                metrics["by_type"][item_type]
            )

    print("\n" + "=" * 60)