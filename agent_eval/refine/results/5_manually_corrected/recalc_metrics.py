import json
import sys
from collections import defaultdict

SAT_YES = {"YES"}
SAT_PARTIAL = {"PARTIAL", "PARTIALLY"}
SAT_NO = {"NO"}


def sat_key(item):
    return str(item.get("satisfaction", "")).strip().upper()


def calc_metrics(rows):
    total = len(rows)

    info_present = sum(
        1 for r in rows
        if r.get("information_present") is True
    )

    fully = sum(
        1 for r in rows
        if sat_key(r) in SAT_YES
    )

    partially = sum(
        1 for r in rows
        if sat_key(r) in SAT_PARTIAL
    )

    not_satisfied = sum(
        1 for r in rows
        if sat_key(r) in SAT_NO
    )

    return {
        "total_requirements": total,
        "information_present": info_present,
        "information_presence": (info_present / total) if total else 0.0,
        "fully_satisfied": fully,
        "partially_satisfied": partially,
        "not_satisfied": not_satisfied,
        "satisfaction_score": (
            (fully + 0.5 * partially) / total
        ) if total else 0.0,
    }


def calc_by_type(rows):
    grouped = defaultdict(list)

    for r in rows:
        grouped[r.get("type", "unknown")].append(r)

    return {
        typ: calc_metrics(items)
        for typ, items in grouped.items()
    }


def recalculate(data):
    all_rows = []

    for sample in data.get("samples", []):
        rows = sample.get("checklist_results", [])
        all_rows.extend(rows)

        sample_metrics = calc_metrics(rows)
        sample_metrics["by_type"] = calc_by_type(rows)
        sample["metrics"] = sample_metrics

    global_metrics = calc_metrics(all_rows)
    global_metrics["by_type"] = calc_by_type(all_rows)
    data["metrics"] = global_metrics

    return data


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "evaluation_results.json"
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data = recalculate(data)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Recalculated metrics written to: {output_path}")


if __name__ == "__main__":
    main()