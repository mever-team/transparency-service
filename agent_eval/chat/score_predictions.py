"""
Set-membership scoring of predictions vs ground truth.

For each question:
    right  = sentences in BOTH ground truth and predictions
    missed = sentences in ground truth but NOT predicted
    wrong  = sentences predicted but NOT in ground truth

No precision/recall/F1 — just counts. For every predicted sentence the raw
header tag from the matcher ("<h3 class='success title'>From creator in
overview</h3>") is preserved verbatim so the HTML report can show what
section/field the matcher attributed, without us guessing at it.

Writes:
    scores/N.json         per-model, per-category, per-question results
    scores/summary.json   counts aggregated across all models
"""

import json
import re
import importlib.util
from pathlib import Path

SUCCESS_RE = re.compile(
    r"(<h3 class='success title'>(.*?)</h3>)(.*?)(?=<h3 class=|$)",
    re.DOTALL,
)
ERROR_RE = re.compile(
    r"<h3 class='error'>(.*?)</h3>\s*<span>(.*?)</span>",
    re.DOTALL,
)


def normalize_sentence(text: str) -> str:
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r"<br>\s*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>$", "", text)
    text = re.sub(r"\.{1,3}$", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_prediction_html(html: str):
    """Return (list of prediction dicts, list of error dicts).

    Each prediction:
        raw             - sentence text as returned by the matcher
        normalized      - normalized form used for matching
        header          - human-readable header text (e.g. "From creator in overview")
        header_html     - the whole <h3 class='success title'>...</h3> tag, verbatim
    """
    sentences = []
    seen = set()
    for m in SUCCESS_RE.finditer(html or ""):
        header_html = m.group(1).strip()
        header_text = m.group(2).strip()
        raw_body = re.sub(r"<br>\s*$", "", m.group(3).strip(),
                          flags=re.IGNORECASE).strip()
        if not raw_body:
            continue
        norm = normalize_sentence(raw_body)
        if not norm or norm in seen:
            continue
        seen.add(norm)
        sentences.append({
            "raw": raw_body,
            "normalized": norm,
            "header": header_text,
            "header_html": header_html,
        })

    errors = [
        {"type": m.group(1).strip(), "message": m.group(2).strip()}
        for m in ERROR_RE.finditer(html or "")
    ]
    return sentences, errors


def load_ground_truth(folder: Path):
    spec = importlib.util.spec_from_file_location(
        f"gt_{folder.name}", folder / "ground_truth.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.GROUND_TRUTH


def index_ground_truth(gt_category):
    return {item["question"]: item["ground_truth"] for item in gt_category}


def score_question(gt_list, pred_sentences, pred_errors):
    gt_by_norm = {}
    for g in gt_list:
        norm = normalize_sentence(g["sentence"])
        if norm and norm not in gt_by_norm:
            gt_by_norm[norm] = {
                "sentence": g["sentence"],
                "section": g.get("section"),
                "field": g.get("field"),
            }
    gt_norms = set(gt_by_norm)

    pred_by_norm = {p["normalized"]: p for p in pred_sentences}
    pred_norms = set(pred_by_norm)

    right_norms = gt_norms & pred_norms
    missed_norms = gt_norms - pred_norms
    wrong_norms = pred_norms - gt_norms

    right_list = [
        {
            "sentence": gt_by_norm[n]["sentence"],
            "section": gt_by_norm[n]["section"],
            "field": gt_by_norm[n]["field"],
            "pred_header": pred_by_norm[n]["header"],
            "pred_header_html": pred_by_norm[n]["header_html"],
        }
        for n in sorted(right_norms)
    ]
    missed_list = [
        {
            "sentence": gt_by_norm[n]["sentence"],
            "section": gt_by_norm[n]["section"],
            "field": gt_by_norm[n]["field"],
        }
        for n in sorted(missed_norms)
    ]
    wrong_list = [
        {
            "sentence": pred_by_norm[n]["raw"],
            "header": pred_by_norm[n]["header"],
            "header_html": pred_by_norm[n]["header_html"],
        }
        for n in sorted(wrong_norms)
    ]

    n_gt = len(gt_norms)
    n_right = len(right_norms)
    n_missed = len(missed_norms)
    n_wrong = len(wrong_norms)

    return {
        "n_gt": n_gt,
        "n_pred": len(pred_norms),
        "right": n_right,
        "missed": n_missed,
        "wrong": n_wrong,
        "fully_correct": (n_missed == 0 and n_wrong == 0),
        "fully_missed":  (n_gt > 0 and n_right == 0 and n_wrong == 0),
        "right_sentences": right_list,
        "missed_sentences": missed_list,
        "wrong_sentences": wrong_list,
        "errors": pred_errors,
        "has_missing_info":  any(e["type"] == "Missing info"   for e in pred_errors),
        "has_vague_question": any(e["type"] == "Vague question" for e in pred_errors),
    }


def aggregate(items):
    return {
        "n_questions": len(items),
        "total_ground_truth_sentences": sum(r["n_gt"]    for r in items),
        "right":  sum(r["right"]  for r in items),
        "missed": sum(r["missed"] for r in items),
        "wrong":  sum(r["wrong"]  for r in items),
        "questions_fully_correct": sum(1 for r in items if r["fully_correct"]),
        "questions_partially_correct": sum(1 for r in items if r["right"] > 0 and not r["fully_correct"]),
        "questions_wrong": sum(1 for r in items if r["right"] == 0),
        "questions_fully_missed":  sum(1 for r in items if r["fully_missed"]),
        "questions_with_wrong_predictions":  sum(1 for r in items if r["wrong"]  > 0),
        "questions_with_missed_predictions": sum(1 for r in items if r["missed"] > 0),
        "questions_with_missing_info_error":  sum(1 for r in items if r["has_missing_info"]),
        "questions_with_vague_question_error": sum(1 for r in items if r["has_vague_question"]),
    }


def score_one(folder: Path, pred_file: Path) -> dict:
    with pred_file.open(encoding="utf-8") as f:
        predictions = json.load(f)
    ground_truth = load_ground_truth(folder)

    per_question = {}
    for category, entries in predictions.items():
        if category.startswith("_"):
            continue
        gt_lookup = index_ground_truth(ground_truth.get(category, []))
        cat_results = []
        for entry in entries:
            q = entry["question"]
            preds, errors = parse_prediction_html(entry.get("answer", ""))
            r = score_question(gt_lookup.get(q, []), preds, errors)
            r["question"] = q
            cat_results.append(r)
        per_question[category] = cat_results

    per_category = {cat: aggregate(items) for cat, items in per_question.items()}
    overall = aggregate([r for items in per_question.values() for r in items])

    return {
        "_meta": {
            "model_card_folder": str(folder),
            "predictions_file": str(pred_file),
        },
        "overall": overall,
        "per_category": per_category,
        "per_question": per_question,
    }


def main():
    dataset_dir = Path("dataset")
    predictions_dir = Path("predictions")
    scores_dir = Path("scores")
    scores_dir.mkdir(exist_ok=True)

    def numeric_key(p: Path):
        return int(p.name) if p.name.isdigit() else -1

    summary = {"per_model": {}, "overall": {}}
    grand = {"total_ground_truth_sentences": 0, "right": 0,
             "missed": 0, "wrong": 0, "n_questions": 0,
             "questions_fully_correct": 0,
             "questions_partially_correct": 0,
             "questions_wrong": 0}

    for folder in sorted(dataset_dir.iterdir(), key=numeric_key):
        if not folder.is_dir() or not folder.name.isdigit():
            continue
        pred_file = predictions_dir / f"{folder.name}.json"
        if not pred_file.exists():
            print(f"⚠️  skipping {folder.name}: no predictions file")
            continue

        print(f"Scoring {folder.name}…")
        result = score_one(folder, pred_file)
        with (scores_dir / f"{folder.name}.json").open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        ov = result["overall"]
        summary["per_model"][folder.name] = {
            "n_questions": ov["n_questions"],
            "total_ground_truth_sentences": ov["total_ground_truth_sentences"],
            "right":  ov["right"],
            "missed": ov["missed"],
            "wrong":  ov["wrong"],
            "questions_fully_correct": ov["questions_fully_correct"],
            "per_category": {
                c: {
                    "right":  m["right"],
                    "missed": m["missed"],
                    "wrong":  m["wrong"],
                    "total_ground_truth_sentences": m["total_ground_truth_sentences"],
                    "questions_fully_correct": m["questions_fully_correct"],
                    "n_questions": m["n_questions"],
                }
                for c, m in result["per_category"].items()
            },
        }
        for k in grand:
            grand[k] += ov[k]
        print(f"  right={ov['right']}  missed={ov['missed']}  "
              f"wrong={ov['wrong']}  (out of {ov['total_ground_truth_sentences']} GT)  "
              f"fully_correct={ov['questions_fully_correct']}/{ov['n_questions']}")

    summary["overall"] = grand
    with (scores_dir / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\n=== Overall ===")
    print(json.dumps(grand, indent=2))


if __name__ == "__main__":
    main()