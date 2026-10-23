"""
Field-level scoring: does the matcher return the right fields?

For each question, compare the target fields (from dataset/gt.json) with the
fields the matcher actually returned (parsed from its <h3> headers).
Score = hits / targets. A question with 2 targets and 1 hit scores 0.5.

If a target field is empty in the card JSON, it's dropped from the target set
for that card. If all targets are empty, the question is skipped.
"""

import json
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
VALID_FIELDS = set(json.load((HERE / "fields.json").open())["fields"])
GT = json.load((HERE / "dataset" / "gt.json").open())

# Matches: <h3 class='success title'>From <field> in <section></h3>
SUCCESS_RE = re.compile(
    r"<h3 class='success title'>(.*?)</h3>(.*?)(?=<h3 class=|$)", re.DOTALL
)
HEADER_RE = re.compile(r"^(?:From (.+?) in |(.+?) in )(\w+)(?: is)?$")


def parse_predicted_fields(html):
    """Extract 'section.field' ids from matcher HTML headers."""
    fields = set()
    for m in SUCCESS_RE.finditer(html or ""):
        h = m.group(1).strip()
        match = HEADER_RE.match(h)
        if not match:
            continue
        field_words = match.group(1) or match.group(2)
        section = match.group(3)
        fid = f"{section}.{field_words.strip().lower().replace(' ', '_')}"
        if fid in VALID_FIELDS:
            fields.add(fid)
    return fields


def get_field_value(card_json, fid):
    """Return the raw value of 'section.field' from a card JSON, or None."""
    section, _, field = fid.partition(".")
    for sec in card_json.get("data", []):
        if sec["name"] != section:
            continue
        for fld in sec["value"]:
            if fld["name"] == field:
                return fld["value"]
    return None


def is_empty(v):
    return v is None or (isinstance(v, str) and not v.strip())


def score_question(gt_item, html, card_json):
    """Score one question, or return None if all its targets are empty."""
    targets = []
    for t in gt_item.get("target_fields", []):
        if t in VALID_FIELDS and not t.endswith(".more") and not is_empty(get_field_value(card_json, t)):
            targets.append(t)

    if not targets:
        return None

    targets_set = set(targets)
    predicted = parse_predicted_fields(html)
    hit = targets_set & predicted
    missed = targets_set - predicted
    off_target = predicted - targets_set
    coverage = len(hit) / len(targets_set)

    return {
        "question": gt_item["question"],
        "targets": sorted(targets_set),
        "predicted": sorted(predicted),
        "hit": sorted(hit),
        "missed": sorted(missed),
        "off_target": sorted(off_target),
        "coverage": coverage,
        "correct": coverage == 1.0,
        "partial": 0.0 < coverage < 1.0,
        "wrong": coverage == 0.0,
    }


def aggregate(items):
    n = len(items)
    if n == 0:
        return {"n_questions": 0, "correct": 0, "partial": 0, "wrong": 0,
                "avg_score": 0.0, "n_target_fields": 0, "n_hit": 0}
    n_targets = sum(len(r["targets"]) for r in items)
    n_hit = sum(len(r["hit"]) for r in items)
    total = sum(r["coverage"] for r in items)
    return {
        "n_questions": n,
        "correct": sum(1 for r in items if r["correct"]),
        "partial": sum(1 for r in items if r["partial"]),
        "wrong": sum(1 for r in items if r["wrong"]),
        "avg_score": total / n,
        "n_target_fields": n_targets,
        "n_hit": n_hit,
        "field_recall": (n_hit / n_targets) if n_targets else None,
    }


def score_one(folder, pred_file):
    predictions = json.load(pred_file.open())
    card_json = json.load(next(folder.glob("*.json")).open())

    per_question = {}
    skipped = []
    for category, gt_entries in GT.items():
        pred_by_q = {e["question"]: e for e in predictions.get(category, [])}
        results = []
        for gt_item in gt_entries:
            pred = pred_by_q.get(gt_item["question"], {})
            r = score_question(gt_item, pred.get("answer", ""), card_json)
            if r is None:
                skipped.append({"category": category, "question": gt_item["question"]})
            else:
                results.append(r)
        per_question[category] = results

    all_items = [r for items in per_question.values() for r in items]
    return {
        "_meta": {"card": str(folder), "predictions": str(pred_file)},
        "overall": aggregate(all_items),
        "per_category": {c: aggregate(items) for c, items in per_question.items()},
        "skipped_questions": skipped,
        "per_question": per_question,
    }


def main():
    out_dir = Path("scores") / "fields"
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = {"per_model": {}, "overall": {}}
    grand = defaultdict(int)
    all_skipped = defaultdict(int)

    folders = sorted(
        (f for f in Path("dataset").iterdir() if f.is_dir() and f.name.isdigit()),
        key=lambda p: int(p.name),
    )
    for folder in folders:
        pred_file = Path("predictions") / f"{folder.name}.json"
        if not pred_file.exists():
            print(f"⚠️  skip {folder.name}: no predictions")
            continue

        print(f"Scoring {folder.name}…")
        result = score_one(folder, pred_file)
        json.dump(result, (out_dir / f"{folder.name}.json").open("w"), indent=2)

        summary["per_model"][folder.name] = result
        ov = result["overall"]
        for k in ("n_questions", "correct", "partial", "wrong",
                  "n_target_fields", "n_hit"):
            grand[k] += ov[k]
        grand["total_score"] += ov["avg_score"] * ov["n_questions"]

        for s in result["skipped_questions"]:
            all_skipped[(s["category"], s["question"])] += 1

        print(f"  q={ov['n_questions']} correct={ov['correct']} "
              f"partial={ov['partial']} wrong={ov['wrong']} "
              f"score={ov['avg_score']:.1%} skipped={len(result['skipped_questions'])}")

    n = grand["n_questions"]
    summary["overall"] = {
        "n_questions": n,
        "correct": grand["correct"],
        "partial": grand["partial"],
        "wrong": grand["wrong"],
        "avg_score": (grand["total_score"] / n) if n else 0.0,
        "n_target_fields": grand["n_target_fields"],
        "n_hit": grand["n_hit"],
        "field_recall": (grand["n_hit"] / grand["n_target_fields"]) if grand["n_target_fields"] else None,
    }
    summary["skipped_questions"] = [
        {"category": c, "question": q, "n_cards": n}
        for (c, q), n in sorted(all_skipped.items(), key=lambda kv: -kv[1])
    ]

    json.dump(summary, (out_dir / "summary.json").open("w"), indent=2)
    print("\n=== Overall ===")
    print(json.dumps(summary["overall"], indent=2))


if __name__ == "__main__":
    main()