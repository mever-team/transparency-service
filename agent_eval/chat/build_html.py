"""
Render scores/fields/*.json as a single self-contained HTML report.
"""
import html
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCORES = HERE / "scores" / "fields"

def esc(x): return "" if x is None else html.escape(str(x))
def pct(x, places=1): return "—" if x is None else f"{x * 100:.{places}f}%"

def pill(text, kind):
    return f'<span class="pill pill-{kind}">{esc(text)}</span>'

def chip(text, kind):
    return f'<span class="chip chip-{kind}">{esc(text)}</span>'

def bar(score):
    w = 0.0 if score is None else max(0.0, min(100.0, score * 100.0))
    return f'<span class="bar"><span style="width:{w:.1f}%"></span></span>'

def status_pill(q):
    if q.get("correct"): return pill("correct", "correct")
    if q.get("wrong"): return pill("wrong", "miss")
    n_h = len(q.get("hit") or [])
    n_t = len(q.get("targets") or [])
    return pill(f"partial {n_h}/{n_t}", "partial")

def render_question(q):
    parts = ['<div class="q">']
    parts.append(
        '<div class="q-head">'
        + status_pill(q)
        + f'<span class="q-text">{esc(q.get("question"))}</span>'
        + '</div>'
    )
    parts.append('<div class="q-fields">')
    if q.get("targets"):
        parts.append('<div class="row"><span class="lbl">targets</span>' + "".join(chip(t, "target") for t in q["targets"]) + '</div>')
    if q.get("hit"):
        parts.append('<div class="row"><span class="lbl">hit</span>' + "".join(chip(t, "hit") for t in q["hit"]) + '</div>')
    if q.get("missed"):
        parts.append('<div class="row"><span class="lbl">missed</span>' + "".join(chip(t, "miss") for t in q["missed"]) + '</div>')
    if q.get("off_target"):
        parts.append('<div class="row"><span class="lbl">off-target</span>' + "".join(chip(t, "off") for t in q["off_target"]) + '</div>')
    parts.append('</div></div>')
    return "".join(parts)

def render_category_block(cat, items):
    n = len(items)
    if n == 0: return ""
    c = sum(1 for r in items if r.get("correct"))
    p = sum(1 for r in items if r.get("partial"))
    w = sum(1 for r in items if r.get("wrong"))

    summary = f'{esc(cat)} — {c} correct · {p} partial · {w} wrong'
    body = "".join(render_question(q) for q in items)
    return f'<details><summary>{summary}</summary><div class="qlist">{body}</div></details>'

# ------------------------------------------------------------------ derived aggregates

def compute_per_field(models_data):
    """Aggregate per-field recall from each model's per_question data."""
    stats = defaultdict(lambda: {"n_questions": 0, "n_hit": 0})
    for data in models_data:
        for items in data.get("per_question", {}).values():
            for r in items:
                for t in r.get("targets", []):
                    stats[t]["n_questions"] += 1
                    if t in r.get("hit", []):
                        stats[t]["n_hit"] += 1
    return {
        fid: {
            "n_questions": s["n_questions"],
            "n_hit": s["n_hit"],
            "recall": s["n_hit"] / s["n_questions"] if s["n_questions"] else None,
        }
        for fid, s in sorted(stats.items())
    }

def compute_confusions(models_data, limit=50):
    """Aggregate (missed_target → returned_off_target) pairs."""
    pairs = defaultdict(int)
    for data in models_data:
        for items in data.get("per_question", {}).values():
            for r in items:
                for t in r.get("missed", []):
                    for o in r.get("off_target", []):
                        pairs[(t, o)] += 1
    return [
        {"missed": t, "returned": o, "n": n}
        for (t, o), n in sorted(pairs.items(), key=lambda kv: -kv[1])[:limit]
    ]

# ------------------------------------------------------------------ tables

def per_category_table(per_cat):
    rows = []
    cats = sorted(per_cat.keys(), key=lambda x: (x == "cross_field", x))
    for cat in cats:
        s = per_cat[cat]
        if s["n_questions"] == 0:
            continue
        rows.append(
            '<tr>'
            f'<td>{esc(cat)}</td>'
            f'<td class="num">{s["n_questions"]}</td>'
            f'<td class="num">{s["correct"]}</td>'
            f'<td class="num">{s["partial"]}</td>'
            f'<td class="num">{s["wrong"]}</td>'
            f'<td class="num">{bar(s["avg_score"])}{pct(s["avg_score"])}</td>'
            '</tr>'
        )
    return (
        '<table><thead><tr>'
        '<th>question type</th><th class="num">questions</th>'
        '<th class="num">correct</th><th class="num">partial</th><th class="num">wrong</th>'
        '<th class="num">avg score</th>'
        '</tr></thead><tbody>' + "".join(rows) + '</tbody></table>'
    )

def per_field_table(per_field, limit=None):
    items = sorted(per_field.items(), key=lambda kv: (-kv[1]["n_questions"], kv[0]))
    if limit: items = items[:limit]
    if not items: return '<p class="meta">No per-field data.</p>'
    rows = []
    for fid, s in items:
        rows.append(
            '<tr>'
            f'<td><code>{esc(fid)}</code></td>'
            f'<td class="num">{s["n_questions"]}</td>'
            f'<td class="num">{s["n_hit"]}</td>'
            f'<td class="num">{bar(s["recall"])}{pct(s["recall"])}</td>'
            '</tr>'
        )
    return (
        '<table><thead><tr>'
        '<th>field</th><th class="num">questions</th><th class="num">hits</th><th class="num">recall</th>'
        '</tr></thead><tbody>' + "".join(rows) + '</tbody></table>'
    )

def confusion_table(confusions, limit=None):
    items = confusions[:limit] if limit else confusions
    if not items: return '<p class="meta">No confusion pairs.</p>'
    rows = []
    for c in items:
        rows.append(
            '<tr>'
            f'<td><code>{esc(c["missed"])}</code></td>'
            '<td>→</td>'
            f'<td><code>{esc(c["returned"])}</code></td>'
            f'<td class="num">{c["n"]}</td>'
            '</tr>'
        )
    return (
        '<table><thead><tr>'
        '<th>missed target</th><th></th><th>returned instead</th><th class="num">count</th>'
        '</tr></thead><tbody>' + "".join(rows) + '</tbody></table>'
    )

# ------------------------------------------------------------------ aggregation & layout

def aggregate_categories(summary):
    agg = defaultdict(lambda: {
        "n_questions": 0, "correct": 0, "partial": 0, "wrong": 0,
        "total_score": 0.0, "avg_score": 0.0,
    })
    for mdata in summary.get("per_model", {}).values():
        for cat, cdata in mdata.get("per_category", {}).items():
            agg[cat]["n_questions"] += cdata.get("n_questions", 0)
            agg[cat]["correct"] += cdata.get("correct", 0)
            agg[cat]["partial"] += cdata.get("partial", 0)
            agg[cat]["wrong"] += cdata.get("wrong", 0)
            agg[cat]["total_score"] += cdata.get("avg_score", 0.0) * cdata.get("n_questions", 0)

    for cat, data in agg.items():
        n = data["n_questions"]
        data["avg_score"] = (data["total_score"] / n) if n else 0.0

    return dict(agg)

def render_model(mid, data):
    ov = data["overall"]
    meta_bits = []
    if data.get("_meta", {}).get("card"):
        meta_bits.append(f'card: <code>{esc(data["_meta"]["card"])}</code>')

    per_field = compute_per_field([data])
    confusions = compute_confusions([data])

    cat_blocks = "".join(
        render_category_block(cat, data["per_question"].get(cat, []))
        for cat in data["per_question"]
    )

    return (
        f'<section id="model-{esc(mid)}">'
        f'<h2>Model {esc(mid)} <a class="toplink" href="#top">↑ top</a></h2>'
        + (f'<p class="meta">{" · ".join(meta_bits)}</p>' if meta_bits else '') +
        '<div class="cards">'
        f'<div class="card"><div class="num">{ov["n_questions"]}</div><div class="lbl">questions</div></div>'
        f'<div class="card"><div class="num">{pct(ov["avg_score"])}</div><div class="lbl">avg score</div></div>'
        f'<div class="card"><div class="num">{ov["correct"]}</div><div class="lbl">correct</div></div>'
        f'<div class="card"><div class="num">{ov["partial"]}</div><div class="lbl">partial</div></div>'
        f'<div class="card"><div class="num">{ov["wrong"]}</div><div class="lbl">wrong</div></div>'
        '</div>'
        '<h3>Per category</h3>' + per_category_table(data["per_category"]) +
        '<h3>Per field</h3>' + per_field_table(per_field) +
        '<h3>Confusion pairs</h3>' + confusion_table(confusions) +
        '<h3>Per question</h3>' + cat_blocks +
        '</section>'
    )

def render_overview(summary):
    ov = summary["overall"]
    per_model = summary["per_model"]

    model_rows = []
    for mid in sorted(per_model, key=lambda x: (not str(x).isdigit(), str(x).zfill(4))):
        s = per_model[mid]["overall"]
        model_rows.append(
            '<tr>'
            f'<td><a href="#model-{esc(mid)}">Model {esc(mid)}</a></td>'
            f'<td class="num">{s["n_questions"]}</td>'
            f'<td class="num">{s["correct"]}</td>'
            f'<td class="num">{s["partial"]}</td>'
            f'<td class="num">{s["wrong"]}</td>'
            f'<td class="num">{bar(s["avg_score"])}{pct(s["avg_score"])}</td>'
            '</tr>'
        )

    cat_agg = aggregate_categories(summary)
    all_data = list(per_model.values())
    per_field = compute_per_field(all_data)
    confusions = compute_confusions(all_data)

    return (
        '<section id="overview">'
        '<h2>Overview <a class="toplink" href="#top">↑ top</a></h2>'

        '<div class="cards">'
        f'<div class="card"><div class="num">{ov["n_questions"]}</div><div class="lbl">questions</div></div>'
        f'<div class="card"><div class="num">{pct(ov["avg_score"])}</div><div class="lbl">avg score</div></div>'
        f'<div class="card"><div class="num">{ov["correct"]}</div><div class="lbl">correct</div></div>'
        f'<div class="card"><div class="num">{ov["partial"]}</div><div class="lbl">partial</div></div>'
        f'<div class="card"><div class="num">{ov["wrong"]}</div><div class="lbl">wrong</div></div>'
        '</div>'

        '<h3>Per question type (across all models)</h3>'
        + per_category_table(cat_agg) +

        '<h3>Per model</h3>'
        '<table><thead><tr>'
        '<th>model</th><th class="num">questions</th>'
        '<th class="num">correct</th><th class="num">partial</th><th class="num">wrong</th>'
        '<th class="num">avg score</th>'
        '</tr></thead><tbody>' + "".join(model_rows) + '</tbody></table>'

        '<h3>Per field (across all models)</h3>' + per_field_table(per_field) +
        '<h3>Confusion pairs (across all models)</h3>' + confusion_table(confusions, limit=30) +
        '</section>'
    )

CSS = """
* { box-sizing: border-box; }
body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 14px; line-height: 1.5; color: #1f2328; background: #ffffff; }
.wrap { max-width: 1200px; margin: 0 auto; padding: 32px 24px 64px; }
h1 { font-size: 24px; margin: 0 0 4px; }
h2 { font-size: 18px; margin: 40px 0 12px; padding-bottom: 8px; border-bottom: 1px solid #d0d7de; display: flex; align-items: baseline; justify-content: space-between; }
h3 { font-size: 12px; margin: 24px 0 8px; color: #656d76; text-transform: uppercase; letter-spacing: 0.06em; }
.meta { color: #656d76; margin: 0 0 20px; font-size: 13px; }
code { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 12px; background: #f6f8fa; padding: 1px 4px; border-radius: 3px; }
a { color: #0969da; text-decoration: none; }
a:hover { text-decoration: underline; }
.toplink { font-size: 12px; font-weight: 400; color: #656d76; }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; margin-bottom: 20px; }
.card { background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 8px; padding: 12px 14px; }
.card .num { font-size: 24px; font-weight: 600; line-height: 1.2; }
.card .lbl { color: #656d76; font-size: 11px; margin-top: 2px; text-transform: uppercase; letter-spacing: 0.05em; }
nav.models { margin: 0 0 8px; }
nav.models a { margin-right: 14px; font-weight: 500; }
table { width: 100%; border-collapse: collapse; margin: 8px 0 20px; font-size: 13px; }
th, td { text-align: left; padding: 6px 10px; border-bottom: 1px solid #eaeef2; vertical-align: middle; }
th { background: #f6f8fa; font-weight: 600; font-size: 12px; }
td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; }
tr:hover td { background: #fafbfc; }
.pill { display: inline-block; padding: 1px 8px; border-radius: 999px; font-size: 11px; font-weight: 600; line-height: 1.6; white-space: nowrap; }
.pill-correct { background: #dafbe1; color: #1a7f37; }
.pill-partial { background: #fff8c5; color: #7d4e00; }
.pill-miss    { background: #ffebe9; color: #cf222e; }
.chip { display: inline-block; padding: 1px 7px; margin: 1px 3px 1px 0; border-radius: 4px; font-family: ui-monospace, SFMono-Regular, monospace; font-size: 11.5px; }
.chip-target { background: #eaeef2; color: #1f2328; }
.chip-hit    { background: #dafbe1; color: #1a7f37; }
.chip-miss   { background: #ffebe9; color: #cf222e; }
.chip-off    { background: #fff8c5; color: #7d4e00; }
details { margin: 6px 0; border: 1px solid #d0d7de; border-radius: 8px; overflow: hidden; background: #fff; }
details[open] summary { border-bottom: 1px solid #d0d7de; }
details summary { padding: 8px 14px; background: #f6f8fa; cursor: pointer; font-weight: 600; font-size: 13px; }
details summary:hover { background: #eaeef2; }
.qlist { padding: 0; }
.q { padding: 10px 14px; border-top: 1px solid #eaeef2; }
.q:first-child { border-top: 0; }
.q-head { display: flex; gap: 10px; align-items: baseline; flex-wrap: wrap; margin-bottom: 6px; }
.q-text { font-weight: 500; }
.q-fields { font-size: 12px; }
.row { margin: 3px 0; display: flex; gap: 6px; flex-wrap: wrap; align-items: baseline; }
.lbl { color: #656d76; min-width: 72px; font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.05em; }
.bar { display: inline-block; width: 80px; height: 7px; background: #eaeef2; border-radius: 4px; overflow: hidden; vertical-align: middle; margin-right: 8px; }
.bar > span { display: block; height: 100%; background: #1a7f37; }
.foot { margin-top: 48px; color: #656d76; font-size: 12px; border-top: 1px solid #eaeef2; padding-top: 16px; }
"""

def main():
    summary_path = SCORES / "summary.json"
    if not summary_path.exists():
        raise SystemExit(f"missing {summary_path}; run score_fields.py first")
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    model_files = sorted(
        [p for p in SCORES.glob("*.json") if p.stem.isdigit()],
        key=lambda p: int(p.stem),
    )

    model_blocks = []
    for p in model_files:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"skip {p}: {e}")
            continue
        model_blocks.append(render_model(p.stem, data))

    nav = " ".join(f'<a href="#model-{p.stem}">Model {p.stem}</a>' for p in model_files)

    page = (
        '<!doctype html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<title>Field-level scoring report</title>\n'
        f'<style>{CSS}</style>\n'
        '</head>\n<body id="top">\n<div class="wrap">\n'
        '<h1>Field-level scoring report</h1>\n'
        '<p class="meta">'
        'A question is <strong>correct</strong> if all targets are hit. '
        'If a multi-target question hits only some, it is <strong>partial</strong>. '
        '<strong>Avg score</strong> gives proportional credit (e.g. 1/2 targets = 0.5).'
        '</p>\n'
        f'<nav class="models">{nav}</nav>\n'
        + render_overview(summary)
        + "".join(model_blocks) +
        '<p class="foot">Field-level scoring · see <code>score_fields.py</code> for definitions.</p>\n'
        '</div>\n</body>\n</html>\n'
    )

    out = SCORES / "report.html"
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out}")

if __name__ == "__main__":
    main()