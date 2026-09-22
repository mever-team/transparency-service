from collections import Counter, defaultdict


def safe_div(a, b):
    return a / b if b else 0.0


def calculate_metrics(result):
    matches = result["matches"]
    missing = result["missing"]
    extra = result["extra"]

    predicted_total = len(matches) + len(extra)

    correct = sum(
        m["status"] == "correct"
        for m in matches
    )

    misclassified = sum(
        m["status"] == "misclassified"
        for m in matches
    )

    matched_gt = len({
        m["gt_id"]
        for m in matches
    })

    total_gt = matched_gt + len(missing)

    # --------------------------------------------------
    # Sentence-level metrics
    # --------------------------------------------------

    sentence_match_rate = safe_div(
        len(matches),
        predicted_total,
    )

    classification_accuracy = safe_div(
        correct,
        len(matches),
    )

    correct_prediction_rate = safe_div(
        correct,
        predicted_total,
    )

    extra_rate = safe_div(
        len(extra),
        predicted_total,
    )

    # GT coverage.
    gt_recall = safe_div(
        matched_gt,
        total_gt,
    )

    # --------------------------------------------------
    # Field-level metrics
    # --------------------------------------------------

    fields = set()

    for m in matches:
        fields.add(m["gt_field"])
        fields.add(m["pred_field"])

    for p in missing:
        fields.add(p["field"])

    for p in extra:
        fields.add(p["pred_field"])

    field_metrics = {}

    for field in sorted(fields):

        tp = sum(
            1
            for m in matches
            if (
                m["pred_field"] == field
                and m["gt_field"] == field
            )
        )

        fp = sum(
            1
            for m in matches
            if (
                m["pred_field"] == field
                and m["gt_field"] != field
            )
        )

        fn = sum(
            1
            for m in matches
            if (
                m["gt_field"] == field
                and m["pred_field"] != field
            )
        )

        fn += sum(
            p["field"] == field
            for p in missing
        )

        fp += sum(
            p["pred_field"] == field
            for p in extra
        )

        precision = safe_div(
            tp,
            tp + fp,
        )

        recall = safe_div(
            tp,
            tp + fn,
        )

        f1 = safe_div(
            2 * precision * recall,
            precision + recall,
        )

        field_metrics[field] = {
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }

    # --------------------------------------------------
    # Confusion matrix
    # --------------------------------------------------

    confusion = Counter(
        (
            m["gt_field"],
            m["pred_field"],
        )
        for m in matches
    )

    confusion_matrix = {
        f"{gt} -> {pred}": count
        for (gt, pred), count
        in sorted(confusion.items())
    }

    return {
        "total_gt": total_gt,
        "matched_gt": matched_gt,
        "missing_gt": len(missing),

        "predicted_total": predicted_total,
        "matched_predictions": len(matches),
        "correct": correct,
        "misclassified": misclassified,
        "extra": len(extra),

        "sentence_match_rate": sentence_match_rate,
        "classification_accuracy": classification_accuracy,
        "correct_prediction_rate": correct_prediction_rate,
        "extra_rate": extra_rate,
        "gt_recall": gt_recall,

        "field_metrics": field_metrics,
        "confusion_matrix": confusion_matrix,
    }


def aggregate_metrics(results):

    total_gt = sum(r["total_gt"] for r in results)
    matched_gt = sum(r["matched_gt"] for r in results)
    missing_gt = sum(r["missing_gt"] for r in results)

    predicted_total = sum(
        r["predicted_total"]
        for r in results
    )

    matched_predictions = sum(
        r["matched_predictions"]
        for r in results
    )

    correct = sum(
        r["correct"]
        for r in results
    )

    misclassified = sum(
        r["misclassified"]
        for r in results
    )

    extra = sum(
        r["extra"]
        for r in results
    )

    confusion = Counter()

    for result in results:
        for key, count in result["confusion_matrix"].items():
            confusion[key] += count

    # --------------------------------------------------
    # Aggregate field metrics
    # --------------------------------------------------

    field_counts = defaultdict(
        lambda: {
            "tp": 0,
            "fp": 0,
            "fn": 0,
        }
    )

    for result in results:

        for field, values in result["field_metrics"].items():

            field_counts[field]["tp"] += values["tp"]
            field_counts[field]["fp"] += values["fp"]
            field_counts[field]["fn"] += values["fn"]

    field_metrics = {}

    for field, values in sorted(field_counts.items()):

        tp = values["tp"]
        fp = values["fp"]
        fn = values["fn"]

        precision = safe_div(
            tp,
            tp + fp,
        )

        recall = safe_div(
            tp,
            tp + fn,
        )

        f1 = safe_div(
            2 * precision * recall,
            precision + recall,
        )

        field_metrics[field] = {
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }

    return {
        "files": len(results),

        "total_gt": total_gt,
        "matched_gt": matched_gt,
        "missing_gt": missing_gt,

        "predicted_total": predicted_total,
        "matched_predictions": matched_predictions,
        "correct": correct,
        "misclassified": misclassified,
        "extra": extra,

        "sentence_match_rate": safe_div(
            matched_predictions,
            predicted_total,
        ),

        "classification_accuracy": safe_div(
            correct,
            matched_predictions,
        ),

        "correct_prediction_rate": safe_div(
            correct,
            predicted_total,
        ),

        "gt_recall": safe_div(
            matched_gt,
            total_gt,
        ),

        "extra_rate": safe_div(
            extra,
            predicted_total,
        ),

        "field_metrics": field_metrics,

        "confusion_matrix": dict(
            sorted(confusion.items())
        ),
    }