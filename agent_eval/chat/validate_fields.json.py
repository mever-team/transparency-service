import json

NS = json.load(open("fields.json"))["fields"]
VALID = {"field", "paraphrase", "cross_field"}

def validate(path):
    errs = []
    gt = json.load(open(path))
    items = gt if isinstance(gt, list) else gt.get("questions", [])
    for i, q in enumerate(items):
        qid = q.get("id", f"#{i}")
        qt  = q.get("question_type")
        tf  = q.get("target_fields") or []

        if qt not in VALID:
            errs.append(f"{qid}: bad question_type {qt!r}")

        if not tf:
            errs.append(f"{qid}: empty target_fields")

        for f in tf:
            if f.endswith(".more"):
                errs.append(f"{qid}: targets excluded 'more' field {f!r}")
            elif f not in NS:
                errs.append(f"{qid}: unknown field {f!r}")

        if qt == "cross_field" and len(tf) < 2:
            errs.append(f"{qid}: cross_field needs >=2 targets")
        if qt in ("field", "paraphrase") and len(tf) != 1:
            errs.append(f"{qid}: {qt} needs exactly 1 target")

    return errs