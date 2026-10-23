"""
Field-level scoring of predictions vs ground truth.

For each question in ground_truth.py:

    target_fields    - from the GT ("section.field" list)
    predicted_fields - parsed from the matcher's response headers
    hit              - target_fields & predicted_fields
    
A question gets a numerical score = (number of targets hit) / (total targets).
    - A single-target question is 1.0 if hit, 0.0 if missed.
    - A cross-field question (e.g. 2 targets) gets 0.5 if exactly one is hit.

Questions with an empty target_fields list are skipped entirely. 
Categories "negative" and "ambiguous" are skipped entirely.
"""

import json
import re
from collections import defaultdict
from pathlib import Path

from score_predictions import SUCCESS_RE, load_ground_truth, parse_prediction_html

HERE = Path(__file__).resolve().parent
FIELDS_DOC = json.load((HERE / "fields.json").open(encoding="utf-8"))
VALID_FIELDS = set(FIELDS_DOC["fields"])
EXCLUDED_FIELDS = set(FIELDS_DOC.get("excluded", []))
SKIP_CATEGORIES = {"negative", "ambiguous"}

FROM_RE = re.compile(r"^From (.+?) in ([a-z0-9_]+)$")
IS_RE = re.compile(r"^(.+?) in ([a-z0-9_]+) is$")


# --------------------------------------------------------------------------- #
# header parsing
# --------------------------------------------------------------------------- #
def _field_words_to_id(words: str) -> str:
    return re.sub(r"\s+", "_", words.strip().lower())


def parse_header(header_text: str):
    h = header_text.strip()
    m = FROM_RE.match(h) or IS_RE.match(h)
    if not m:
        return None, f"unparsed header: {h!r}"
    fid = f"{m.group(2)}.{_field_words_to_id(m.group(1))}"
    if fid in EXCLUDED_FIELDS:
        return fid, None
    if fid not in VALID_FIELDS:
        return None, f"unknown field: {fid!r} (header {h!r})"
    return fid, None


def extract_field_headers(html: str):
    return [m.group(2).strip() for m in SUCCESS_RE.finditer(html or "")]


# --------------------------------------------------------------------------- #
# ground-truth indexing
# --------------------------------------------------------------------------- #
def index_ground_truth(gt_category):
    return {item["question"]: item for item in gt_category}


def clean_targets(raw_targets):
    kept, dropped = [], []
    for t in raw_targets or []:
        if not isinstance(t, str):
            dropped.append({"value": t, "reason": "not a string"})
        elif t.endswith(".more"):
            dropped.append({"value": t, "reason": "'more' fields are never scored"})
        elif t not in VALID_FIELDS:
            dropped.append({"value": t, "reason": "unknown field id"})
        else:
            kept.append(t)
    return kept, dropped


# --------------------------------------------------------------------------- #
# per-question scoring
# --------------------------------------------------------------------------- #
def score_question(gt_item, html_answer):
    targets, dropped = clean_targets(gt_item.get("target_fields"))

    predicted = set()
    unparsed = []
    for header in extract_field_headers(html_answer):
        fid, err = parse_header(header)
        if fid is None:
            unparsed.append(err)
        else:
            predicted.add(fid)

    _, errors = parse_prediction_html(html_answer or "")
    vague = any(e["type"] == "Vague question" for e in errors)
    missing_info = any(e["type"] == "Missing info" for e in errors)

    tgt_set = set(targets)
    hit = tgt_set & predicted
    missed = tgt_set - predicted
    off_target = predicted - tgt_set

    coverage = (len(hit) / len(tgt_set)) if tgt_set else 0.0
    score = coverage if coverage is not None else 0.0

    return {
        "targets": sorted(tgt_set),
        "predicted": sorted(predicted),
        "hit": sorted(hit),
        "missed": sorted(missed),
        "off_target": sorted(off_target),
        "n_targets": len(tgt_set),
        "n_predicted_fields": len(predicted),
        "n_off_target": len(off_target),
        "coverage": coverage,
        "score": score,
        "correct": score == 1.0,
        "partial": 0.0 < score < 1.0,
        "wrong": score == 0.0,
        "vague_question": vague,
        "missing_info": missing_info,
        "invalid_targets": dropped,
        "unparsed_headers": unparsed,
    }


# --------------------------------------------------------------------------- #
# aggregation
# --------------------------------------------------------------------------- #
def aggregate(items):
    n = len(items)
    if n == 0:
        return {
            "n_questions": 0, "n_target_fields": 0, "target_fields_hit": 0,
            "target_fields_missed": 0, "field_recall": None,
            "questions_correct": 0, "questions_partial": 0, "questions_wrong": 0,
            "total_score": 0.0, "avg_score": 0.0,
            "questions_vague": 0, "questions_missing_info": 0,
            "avg_off_target_fields": 0.0,
            "cross_field": {"n_questions": 0, "fully_covered": 0, "avg_coverage": None},
        }

    n_targets = sum(r["n_targets"] for r in items)
    n_hit = sum(len(r["hit"]) for r in items)
    n_missed = sum(len(r["missed"]) for r in items)
    
    cross = [r for r in items if r["n_targets"] > 1]
    cross_full = sum(1 for r in cross if r["coverage"] == 1.0)
    cross_cov = (sum(r["coverage"] for r in cross) / len(cross)) if cross else None
    
    total_score = sum(r["score"] for r in items)
    avg_score = total_score / n

    return {
        "n_questions": n,
        "n_target_fields": n_targets,
        "target_fields_hit": n_hit,
        "target_fields_missed": n_missed,
        "field_recall": (n_hit / n_targets) if n_targets else None,
        "questions_correct": sum(1 for r in items if r["correct"]),
        "questions_partial": sum(1 for r in items if r["partial"]),
        "questions_wrong": sum(1 for r in items if r["wrong"]),
        "total_score": total_score,
        "avg_score": avg_score,
        "questions_vague": sum(1 for r in items if r["vague_question"]),
        "questions_missing_info": sum(1 for r in items if r["missing_info"]),
        "avg_off_target_fields": sum(r["n_off_target"] for r in items) / n,
        "cross_field": {
            "n_questions": len(cross),
            "fully_covered": cross_full,
            "avg_coverage": cross_cov,
        },
    }


def per_field_stats(items):
    stats = defaultdict(lambda: {"n_questions": 0, "n_hit": 0})
    for r in items:
        for t in r["targets"]:
            stats[t]["n_questions"] += 1
            if t in r["hit"]:
                stats[t]["n_hit"] += 1
    return {
        fid: {
            "n_questions": s["n_questions"],
            "n_hit": s["n_hit"],
            "recall": s["n_hit"] / s["n_questions"],
        }
        for fid, s in sorted(stats.items())
    }


def confusion_pairs(per_question, limit=50):
    pairs = defaultdict(int)
    for items in per_question.values():
        for r in items:
            for t in r["missed"]:
                for o in r["off_target"]:
                    pairs[(t, o)] += 1
    return [
        {"missed": t, "returned": o, "n": n}
        for (t, o), n in sorted(pairs.items(), key=lambda kv: -kv[1])[:limit]
    ]


# --------------------------------------------------------------------------- #
# driver
# --------------------------------------------------------------------------- #
def score_one(folder: Path, pred_file: Path) -> dict:
    with pred_file.open(encoding="utf-8") as f:
        predictions = json.load(f)
    ground_truth = load_ground_truth(folder)

    per_question = {}
    for category, entries in predictions.items():
        if category.startswith("_") or category in SKIP_CATEGORIES:
            continue
        gt_lookup = index_ground_truth(ground_truth.get(category, []))
        cat_results = []
        for entry in entries:
            q = entry["question"]
            gt_item = gt_lookup.get(q, {})
            raw_targets = gt_item.get("target_fields") or []
            if not raw_targets:
                continue
            r = score_question(gt_item, entry.get("answer", ""))
            r["question"] = q
            cat_results.append(r)
        per_question[category] = cat_results

    per_category = {cat: aggregate(items) for cat, items in per_question.items()}
    all_items = [r for items in per_question.values() for r in items]
    overall = aggregate(all_items)

    return {
        "_meta": {
            "model_card_folder": str(folder),
            "predictions_file": str(pred_file),
            "scorer": "score_fields.py",
        },
        "overall": overall,
        "per_category": per_category,
        "per_field": per_field_stats(all_items),
        "confusions": confusion_pairs(per_question),
        "per_question": per_question,
    }


def main():
    dataset_dir = Path("dataset")
    predictions_dir = Path("predictions")
    out_dir = Path("scores") / "fields"
    out_dir.mkdir(parents=True, exist_ok=True)

    def numeric_key(p: Path):
        return int(p.name) if p.name.isdigit() else -1

    summary = {"per_model": {}, "overall": {}}
    grand = defaultdict(int)
    grand_fields = defaultdict(lambda: {"n_questions": 0, "n_hit": 0})
    grand_confusions = defaultdict(int)

    for folder in sorted(dataset_dir.iterdir(), key=numeric_key):
        if not folder.is_dir() or not folder.name.isdigit():
            continue
        pred_file = predictions_dir / f"{folder.name}.json"
        if not pred_file.exists():
            print(f"⚠️  skipping {folder.name}: no predictions file")
            continue

        print(f"Scoring {folder.name}…")
        result = score_one(folder, pred_file)
        with (out_dir / f"{folder.name}.json").open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        ov = result["overall"]
        summary["per_model"][folder.name] = {
            "overall": ov,
            "per_category": result["per_category"],
            "per_field": result["per_field"],
        }

        for k in (
            "n_questions", "n_target_fields", "target_fields_hit",
            "target_fields_missed", "questions_correct", "questions_partial", 
            "questions_wrong", "questions_vague", "questions_missing_info", 
            "total_score",
        ):
            grand[k] += ov.get(k, 0)

        for fid, s in result["per_field"].items():
            grand_fields[fid]["n_questions"] += s["n_questions"]
            grand_fields[fid]["n_hit"] += s["n_hit"]

        for c in result["confusions"]:
            grand_confusions[(c["missed"], c["returned"])] += c["n"]

        score_str = f"{ov['avg_score']:.1%}"
        print(
            f"  questions={ov['n_questions']}  "
            f"correct={ov['questions_correct']}  "
            f"partial={ov['questions_partial']}  "
            f"wrong={ov['questions_wrong']}  "
            f"score={score_str}"
        )

    summary["overall"] = {
        "n_questions": grand["n_questions"],
        "n_target_fields": grand["n_target_fields"],
        "target_fields_hit": grand["target_fields_hit"],
        "target_fields_missed": grand["target_fields_missed"],
        "field_recall": (
            grand["target_fields_hit"] / grand["n_target_fields"]
            if grand["n_target_fields"] else None
        ),
        "questions_correct": grand["questions_correct"],
        "questions_partial": grand["questions_partial"],
        "questions_wrong": grand["questions_wrong"],
        "total_score": grand["total_score"],
        "avg_score": (grand["total_score"] / grand["n_questions"]) if grand["n_questions"] else 0.0,
        "questions_vague": grand["questions_vague"],
        "questions_missing_info": grand["questions_missing_info"],
    }
    summary["per_field"] = {
        fid: {
            "n_questions": s["n_questions"],
            "n_hit": s["n_hit"],
            "recall": s["n_hit"] / s["n_questions"] if s["n_questions"] else None,
        }
        for fid, s in sorted(grand_fields.items())
    }
    summary["confusions"] = [
        {"missed": t, "returned": o, "n": n}
        for (t, o), n in sorted(grand_confusions.items(), key=lambda kv: -kv[1])[:50]
    ]

    with (out_dir / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\n=== Overall ===")
    print(json.dumps(summary["overall"], indent=2))


if __name__ == "__main__":
    main()