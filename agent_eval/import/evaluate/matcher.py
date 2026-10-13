import re
import unicodedata

from rapidfuzz import fuzz


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().casefold()


def similarity(pred_text: str, gt_text: str) -> float:
    pred = normalize_text(pred_text)
    gt = normalize_text(gt_text)
    
    if len(pred) > len(gt):
        return 0
    
    return fuzz.partial_ratio(pred, gt)



def match_predictions(
    gt_paragraphs,
    pred_paragraphs,
    threshold=85.0,
):
    matches = []
    extra = []
    gt_paragraphs = [p for p in gt_paragraphs if len(p["text"]) >= 5]

    for pred in pred_paragraphs:

        best_score = 0.0
        best_gt = None

        for gt in gt_paragraphs:

            score = similarity(
                pred["text"],
                gt["text"],
            )

            if score > best_score:
                best_score = score
                best_gt = gt

        if best_gt is None or best_score < threshold:

            extra.append({
                "pred_id": pred["id"],
                "pred_field": pred["field"],
                "pred_text": pred["text"],
                "similarity": round(best_score, 2),
                "best_gt_field": best_gt["field"] if best_gt else None,
                "best_gt_text": best_gt["text"] if best_gt else None,
                "status": "unmatched",
            })

            continue

        status = (
            "correct"
            if pred["field"] == best_gt["field"]
            else "misclassified"
        )

        matches.append({
            "pred_id": pred["id"],
            "pred_field": pred["field"],
            "pred_text": pred["text"],

            "gt_id": best_gt["id"],
            "gt_field": best_gt["field"],
            "gt_text": best_gt["text"],

            "similarity": round(best_score, 2),
            "status": status,
        })

    matched_gt_ids = {
        match["gt_id"]
        for match in matches
    }

    missing = [
        gt
        for gt in gt_paragraphs
        if gt["id"] not in matched_gt_ids
    ]

    return {
        "matches": matches,
        "missing": missing,
        "extra": extra,
    }