import json


def save_json(results, path):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            results,
            f,
            indent=2,
            ensure_ascii=False
        )


def print_summary(metrics):

    print("\n" + "=" * 50)
    print("EVALUATION SUMMARY")
    print("=" * 50)

    print(
        f"Requirements satisfied: "
        f"{metrics['satisfied_requirements']} / "
        f"{metrics['total_requirements']}"
    )

    print(
        f"Checklist coverage: "
        f"{metrics['coverage'] * 100:.2f}%"
    )

    print("=" * 50)