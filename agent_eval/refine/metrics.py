from collections import defaultdict


def calculate_metrics(checklist_results):

    total = len(checklist_results)

    information_present = sum(
        1
        for item in checklist_results
        if item["information_present"]
    )

    fully_satisfied = sum(
        1
        for item in checklist_results
        if item["satisfaction"] == "YES"
    )

    partially_satisfied = sum(
        1
        for item in checklist_results
        if item["satisfaction"] == "PARTIAL"
    )

    not_satisfied = sum(
        1
        for item in checklist_results
        if item["satisfaction"] == "NO"
    )

    information_presence = (
        information_present / total
        if total
        else 0
    )

    satisfaction_score = (
        (
            fully_satisfied
            + 0.5 * partially_satisfied
        ) / total
        if total
        else 0
    )

    return {
        "total_requirements": total,

        "information_present": information_present,
        "information_presence": information_presence,

        "fully_satisfied": fully_satisfied,
        "partially_satisfied": partially_satisfied,
        "not_satisfied": not_satisfied,
        "satisfaction_score": satisfaction_score
    }


def calculate_sample_metrics(checklist_results):

    # Overall sample metrics
    metrics = calculate_metrics(checklist_results)

    # -------------------------
    # Metrics by requirement type
    # -------------------------

    by_type = defaultdict(list)

    for item in checklist_results:
        by_type[item["type"]].append(item)

    metrics["by_type"] = {
        item_type: calculate_metrics(items)
        for item_type, items in by_type.items()
    }

    return metrics


def calculate_overall_metrics(results):

    all_checklist_results = []

    for sample in results:
        all_checklist_results.extend(
            sample["checklist_results"]
        )

    # Overall metrics
    metrics = calculate_metrics(
        all_checklist_results
    )

    # -------------------------
    # Metrics by requirement type
    # -------------------------

    by_type = defaultdict(list)

    for item in all_checklist_results:
        by_type[item["type"]].append(item)

    metrics["by_type"] = {
        item_type: calculate_metrics(items)
        for item_type, items in by_type.items()
    }

    return metrics


def calculate_requirement_metrics(results):

    stats = {}

    for sample in results:

        for item in sample["checklist_results"]:

            requirement_id = item["id"]

            if requirement_id not in stats:
                stats[requirement_id] = {
                    "total": 0,
                    "information_present": 0,
                    "fully_satisfied": 0,
                    "partially_satisfied": 0,
                    "not_satisfied": 0,
                    "requirement": item["requirement"],
                    "type": item["type"]
                }

            stats[requirement_id]["total"] += 1

            if item["information_present"]:
                stats[requirement_id]["information_present"] += 1

            satisfaction = item["satisfaction"]

            if satisfaction == "YES":
                stats[requirement_id]["fully_satisfied"] += 1

            elif satisfaction == "PARTIAL":
                stats[requirement_id]["partially_satisfied"] += 1

            elif satisfaction == "NO":
                stats[requirement_id]["not_satisfied"] += 1

    for item in stats.values():

        total = item["total"]

        item["information_presence"] = (
            item["information_present"] / total
            if total
            else 0
        )

        item["satisfaction_score"] = (
            (
                item["fully_satisfied"]
                + 0.5 * item["partially_satisfied"]
            ) / total
            if total
            else 0
        )

    return stats