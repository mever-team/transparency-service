def calculate_sample_metrics(checklist_results):

    total = len(checklist_results)

    satisfied = sum(
        1 for item in checklist_results
        if item["satisfied"]
    )

    score = satisfied / total if total else 0

    return {
        "total_requirements": total,
        "satisfied_requirements": satisfied,
        "coverage": score
    }


def calculate_overall_metrics(results):

    total_requirements = 0
    satisfied_requirements = 0

    for sample in results:
        total_requirements += len(sample["checklist_results"])

        satisfied_requirements += sum(
            1
            for item in sample["checklist_results"]
            if item["satisfied"]
        )

    coverage = (
        satisfied_requirements / total_requirements
        if total_requirements
        else 0
    )

    return {
        "total_requirements": total_requirements,
        "satisfied_requirements": satisfied_requirements,
        "coverage": coverage
    }


def calculate_requirement_metrics(results):

    stats = {}

    for sample in results:
        for item in sample["checklist_results"]:

            requirement_id = item["id"]

            if requirement_id not in stats:
                stats[requirement_id] = {
                    "total": 0,
                    "satisfied": 0,
                    "requirement": item["requirement"]
                }

            stats[requirement_id]["total"] += 1

            if item["satisfied"]:
                stats[requirement_id]["satisfied"] += 1

    for item in stats.values():
        item["score"] = (
            item["satisfied"] / item["total"]
            if item["total"]
            else 0
        )

    return stats