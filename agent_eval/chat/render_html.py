"""
Generates scores/report.html — single self-contained page.

For every predicted sentence the original <h3 class='success title'>...</h3>
header is shown verbatim alongside the sentence text. For every ground-truth
sentence the section.field is shown.

The report shows TWO complementary views:

  Question-level (are answers correct?):
      right   - question fully correct (all GT found, nothing extra)
      partial - some GT found, at least one missed or extra
      missed  - GT exists but matcher returned nothing (declined)
      wrong   - predictions exist but none matched, and not a "missed" case

  Sentence-level (how much of the GT was retrieved?):
      right   - GT sentence returned by matcher
      missed  - GT sentence not returned
      wrong   - matcher returned a sentence not in GT

Both views appear in the model summary, per-category headers, and the
grand total at the top of the page.

Works with score files produced by both older and newer versions of
score_predictions.py.

Reads:  scores/*.json
Writes: scores/report.html
"""

import json
from html import escape
from pathlib import Path
from datetime import datetime, timezone

SCORES_DIR = Path("scores")
OUTPUT = SCORES_DIR / "report.html"


# ── Question-level buckets (right / partial / missed / wrong) ─────────
def _quad_from_question(q):
    if q.get("fully_correct"):
        return "right"
    if q.get("fully_missed"):
        return "missed"
    if q.get("right", 0) == 0:
        return "wrong"
    return "partial"


def _question_quad(data):
    right = partial = missed = wrong = 0
    for items in data.get("per_question", {}).values():
        for q in items:
            cat = _quad_from_question(q)
            if cat == "right":
                right += 1
            elif cat == "partial":
                partial += 1
            elif cat == "missed":
                missed += 1
            else:
                wrong += 1
    return right, partial, missed, wrong, right + partial + missed + wrong


def _category_quad(items):
    right = partial = missed = wrong = 0
    for q in items:
        cat = _quad_from_question(q)
        if cat == "right":
            right += 1
        elif cat == "partial":
            partial += 1
        elif cat == "missed":
            missed += 1
        else:
            wrong += 1
    return right, partial, missed, wrong, right + partial + missed + wrong


def _grand_quad(per_model):
    r = p = m = w = 0
    for data in per_model.values():
        ri, pa, mi, wr, _ = _question_quad(data)
        r += ri
        p += pa
        m += mi
        w += wr
    return r, p, m, w, r + p + m + w


# ── Sentence-level counts (right / missed / wrong) ────────────────────
def _category_sent(items):
    right  = sum(i["right"]  for i in items)
    missed = sum(i["missed"] for i in items)
    wrong  = sum(i["wrong"]  for i in items)
    n_gt   = sum(i["n_gt"]   for i in items)
    return right, missed, wrong, n_gt


# ── Compact count renderers ───────────────────────────────────────────
def count_quad(n_right, n_partial, n_missed, n_wrong, total, size="sm"):
    """Question-level: right / partial / missed / wrong."""
    return (
        f'<span class="cat-counts cat-counts-{size}" '
        f'title="right / partial / missed / wrong (questions)">'
        f'<span class="count-badge count-right">{n_right}</span>'
        f'<span class="count-sep">/</span>'
        f'<span class="count-badge count-partial">{n_partial}</span>'
        f'<span class="count-sep">/</span>'
        f'<span class="count-badge count-q-missed">{n_missed}</span>'
        f'<span class="count-sep">/</span>'
        f'<span class="count-badge count-wrong">{n_wrong}</span>'
        f'<span class="cat-total">of {total}</span>'
        f'</span>'
    )


def count_sent(n_right, n_missed, n_wrong, n_gt, size="sm"):
    """Sentence-level: right / missed / wrong out of GT."""
    return (
        f'<span class="cat-counts cat-counts-{size}" '
        f'title="right / missed / wrong (sentences)">'
        f'<span class="count-badge count-right">{n_right}</span>'
        f'<span class="count-sep">/</span>'
        f'<span class="count-badge count-s-missed">{n_missed}</span>'
        f'<span class="count-sep">/</span>'
        f'<span class="count-badge count-wrong">{n_wrong}</span>'
        f'<span class="cat-total">of {n_gt} GT</span>'
        f'</span>'
    )


# ── Sentence rendering ─────────────────────────────────────────────────
def gt_meta_html(section, field):
    if not section or not field:
        return ""
    return (f'<span class="meta-pill meta-gt" title="GT section.field">'
            f'GT&nbsp;·&nbsp;{escape(section)}.{escape(field)}</span>')


def pred_meta_html(header):
    if not header:
        return ""
    return (f'<span class="meta-pill meta-pred" title="matcher header (verbatim)">'
            f'Pred&nbsp;·&nbsp;{escape(header)}</span>')


def render_sentence(sentence, css_class, section=None, field=None, pred_header=None):
    metas = gt_meta_html(section, field) + pred_meta_html(pred_header)
    return (
        f'<li class="sentence {css_class}">'
        f'<div class="sentence-text">{escape(sentence)}</div>'
        f'<div class="meta-row">{metas}</div>'
        f'</li>'
    )


def render_block(items, css_class, label, kind):
    if not items:
        return f'<div class="list-label">{escape(label)} (0)</div>'
    lis = ""
    if kind in ("right", "missed"):
        for it in items:
            lis += render_sentence(
                it["sentence"], css_class,
                section=it.get("section"),
                field=it.get("field"),
                pred_header=it.get("pred_header"),
            )
    else:
        for it in items:
            lis += render_sentence(
                it["sentence"], css_class,
                pred_header=it.get("header"),
            )
    return (f'<div class="list-label">{escape(label)} ({len(items)})</div>'
            f'<ul class="sentences">{lis}</ul>')


def render_errors(errors):
    if not errors:
        return ""
    parts = []
    for e in errors:
        cls = ("error-vague"   if e["type"] == "Vague question" else
               "error-missing" if e["type"] == "Missing info"  else
               "error-other")
        parts.append(
            f'<div class="error-item {cls}">'
            f'<strong>{escape(e["type"])}:</strong> {escape(e["message"])}'
            f'</div>'
        )
    return f'<div class="errors">{"".join(parts)}</div>'


def badge(label, count, cls):
    return f'<span class="badge badge-{cls}">{escape(label)} {count}</span>'


# ── Question / category / model ────────────────────────────────────────
def render_question(q, idx):
    n_gt     = q["n_gt"]
    n_right  = q["right"]
    n_missed = q["missed"]
    n_wrong  = q["wrong"]

    cat = _quad_from_question(q)
    if cat == "right":
        status_cls, status_txt = "status-right",   "RIGHT"
    elif cat == "partial":
        status_cls, status_txt = "status-partial", "PARTIAL"
    elif cat == "missed":
        status_cls, status_txt = "status-missed",  "MISSED"
    else:
        status_cls, status_txt = "status-wrong",   "WRONG"

    header = (
        f'<span class="status {status_cls}">{status_txt}</span> '
        f'<span class="qtext">Q{idx}: {escape(q["question"])}</span> '
        f'<span class="qcounts">'
        f'{badge("right",  n_right,  "right")}'
        f'{badge("missed", n_missed, "missed")}'
        f'{badge("wrong",  n_wrong,  "wrong")}'
        f'<span class="gt-total">of {n_gt} GT</span>'
        f'</span>'
    )

    body = (
        render_block(q["right_sentences"],  "right",  "Right — GT sentence found",
                     kind="right")
        + render_block(q["missed_sentences"], "missed", "Missed — GT sentence not found",
                       kind="missed")
        + render_block(q["wrong_sentences"],  "wrong",  "Wrong — predicted but not in GT",
                       kind="wrong")
        + render_errors(q["errors"])
    )

    cls = "question ok" if cat == "right" else "question"
    return (f'<details class="{cls}" '
            f'data-perfect="{str(cat == "right").lower()}" '
            f'data-question="{escape(q["question"]).lower()}">'
            f'<summary>{header}</summary>'
            f'<div class="detail">{body}</div>'
            f'</details>')


def render_category(cat, items):
    q_right, q_partial, q_missed, q_wrong, q_total = _category_quad(items)
    s_right, s_missed, s_wrong, s_gt = _category_sent(items)

    header = (
        f'<span class="cat-name">{escape(cat)}</span>'
        f'<span class="cat-counts-wrap">'
        f'<span class="counts-group">'
        f'<span class="counts-label">Qs</span>'
        f'{count_quad(q_right, q_partial, q_missed, q_wrong, q_total, size="sm")}'
        f'</span>'
        f'<span class="counts-group">'
        f'<span class="counts-label">Sent</span>'
        f'{count_sent(s_right, s_missed, s_wrong, s_gt, size="sm")}'
        f'</span>'
        f'</span>'
    )
    questions_html = "".join(render_question(q, i + 1)
                             for i, q in enumerate(items))
    return (f'<details class="category" open>'
            f'<summary>{header}</summary>'
            f'<div class="questions">{questions_html}</div>'
            f'</details>')


def _render_summary_row(label, stat_boxes):
    """stat_boxes: list of (value_html, label) tuples."""
    boxes = "".join(
        f'<div class="stat-box"><div class="stat-value">{v}</div>'
        f'<div class="stat-label">{l}</div></div>'
        for v, l in stat_boxes
    )
    return (f'<div class="summary-label">{escape(label)}</div>'
            f'<div class="summary-row">{boxes}</div>')


def render_model(model_id, data):
    ov = data["overall"]

    q_right, q_partial, q_missed, q_wrong, q_total = _question_quad(data)
    s_right  = ov.get("right", 0)
    s_missed = ov.get("missed", 0)
    s_wrong  = ov.get("wrong", 0)
    s_gt     = ov.get("total_ground_truth_sentences", 0)

    question_row = _render_summary_row(
        "QUESTION-LEVEL — did the matcher answer each question correctly?",
        [
            (q_right,   "Right"),
            (q_partial, "Partial"),
            (q_missed,  "Missed"),
            (q_wrong,   "Wrong"),
            (count_quad(q_right, q_partial, q_missed, q_wrong, q_total,
                        size="lg"), "Right / Partial / Missed / Wrong"),
        ],
    )
    sentence_row = _render_summary_row(
        "SENTENCE-LEVEL — how many ground-truth sentences were retrieved?",
        [
            (s_right,  "Right sentences"),
            (s_missed, "Missed sentences"),
            (s_wrong,  "Wrong sentences"),
            (count_sent(s_right, s_missed, s_wrong, s_gt, size="lg"),
             "Right / Missed / Wrong"),
            (s_gt, "Total GT sentences"),
        ],
    )

    categories_html = "".join(
        render_category(cat, items)
        for cat, items in data["per_question"].items()
    )
    return (
        f'<section class="model" id="model-{escape(model_id)}">'
        f'<h2>Model {escape(model_id)}</h2>'
        f'{question_row}{sentence_row}{categories_html}'
        f'</section>'
    )


# ── Page shell ─────────────────────────────────────────────────────────
CSS = """
:root {
  --bg: #f4f6f8;
  --card: #ffffff;
  --border: #e3e7eb;
  --text: #26303b;
  --muted: #7a8896;
  --right: #2f9e44;    --right-bg: #e6f6ea;
  --partial: #d99400;  --partial-bg: #fff5db;
  --q-missed: #2563a8; --q-missed-bg: #e3edf9;
  --wrong: #d63847;    --wrong-bg: #fde8ea;
  --vague: #7048a8;    --vague-bg: #efe6f8;
  --missing-info: #2563a8; --missing-info-bg: #e3edf9;
  --gt-meta: #3b5b85; --gt-meta-bg: #e6eef8;
  --pred-meta: #8a4ca8; --pred-meta-bg: #f2e8f8;
}
* { box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  margin: 0; background: var(--bg); color: var(--text);
  font-size: 14px; line-height: 1.45;
}
.container { max-width: 1400px; margin: 0 auto; padding: 24px; }
h1 { margin: 0 0 6px; font-size: 24px; }
h2 { margin: 32px 0 16px; font-size: 20px; border-bottom: 2px solid var(--border);
     padding-bottom: 8px; }
.subtitle { color: var(--muted); font-size: 13px; margin-bottom: 24px; }

.controls {
  position: sticky; top: 0; background: var(--card); padding: 12px 16px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.06); border-radius: 8px;
  margin-bottom: 24px; display: flex; gap: 12px; align-items: center;
  flex-wrap: wrap; z-index: 100;
}
.controls label { font-size: 13px; color: var(--muted); display: flex;
                  align-items: center; gap: 6px; }
.controls input[type=text] {
  padding: 6px 10px; border: 1px solid var(--border); border-radius: 6px;
  width: 320px; font-size: 13px;
}
.controls button {
  padding: 6px 12px; border: 1px solid var(--border); border-radius: 6px;
  background: var(--card); cursor: pointer; font-size: 13px;
}
.controls button:hover { background: var(--bg); }

.summary-label {
  font-size: 11px; font-weight: 700; color: var(--muted);
  text-transform: uppercase; letter-spacing: 0.6px;
  margin: 24px 0 8px;
}
.summary-label:first-child { margin-top: 0; }
.summary-row {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 12px; margin-bottom: 8px;
}
.stat-box { background: var(--card); padding: 16px; border-radius: 8px;
            border: 1px solid var(--border); text-align: center; }
.stat-value { font-size: 26px; font-weight: 700; }
.stat-label { font-size: 11px; color: var(--muted); text-transform: uppercase;
              letter-spacing: 0.5px; margin-top: 4px; }

details.category {
  background: var(--card); border-radius: 8px; border: 1px solid var(--border);
  margin-bottom: 12px; overflow: hidden;
}
details.category > summary {
  padding: 12px 16px; cursor: pointer; display: flex; gap: 12px;
  align-items: center; font-weight: 600; background: #fbfcfd;
  border-bottom: 1px solid var(--border); list-style: none;
}
details.category > summary::-webkit-details-marker { display: none; }
details.category > summary::before {
  content: "▸"; color: var(--muted); transition: transform 0.15s;
  display: inline-block; margin-right: 4px;
}
details.category[open] > summary::before { transform: rotate(90deg); }
.cat-name { font-size: 15px; min-width: 120px; }

.cat-counts-wrap {
  display: flex; gap: 24px; margin-left: auto; align-items: center;
  flex-wrap: wrap;
}
.counts-group { display: inline-flex; gap: 6px; align-items: center; }
.counts-label {
  font-size: 10px; font-weight: 700; color: var(--muted);
  text-transform: uppercase; letter-spacing: 0.5px;
}

details.question {
  margin: 8px 16px 8px; border: 1px solid var(--border); border-radius: 6px;
  background: #fcfdfe;
}
details.question.ok { border-left: 3px solid var(--right); }
details.question > summary {
  padding: 10px 12px; cursor: pointer; display: flex; gap: 10px;
  align-items: center; list-style: none;
}
details.question > summary::-webkit-details-marker { display: none; }
details.question > summary::before {
  content: "▸"; color: var(--muted); display: inline-block; margin-right: 4px;
  transition: transform 0.15s;
}
details.question[open] > summary::before { transform: rotate(90deg); }
.qtext { flex: 1; font-size: 13px; color: var(--text); }
.qcounts { display: flex; gap: 6px; align-items: center; font-size: 12px; }
.gt-total { color: var(--muted); font-size: 11px; }

/* Question status pill */
.status {
  display: inline-block; font-size: 10px; font-weight: 700;
  padding: 3px 8px; border-radius: 10px; letter-spacing: 0.4px;
  text-transform: uppercase;
}
.status-right   { background: var(--right-bg);     color: var(--right); }
.status-partial { background: var(--partial-bg);   color: var(--partial); }
.status-missed  { background: var(--q-missed-bg);  color: var(--q-missed); }
.status-wrong   { background: var(--wrong-bg);     color: var(--wrong); }

/* Per-question sentence badges */
.badge {
  display: inline-block; padding: 2px 8px; border-radius: 10px;
  font-size: 11px; font-weight: 600;
}
.badge-right  { background: var(--right-bg);   color: var(--right); }
.badge-missed { background: var(--partial-bg); color: var(--partial); }
.badge-wrong  { background: var(--wrong-bg);   color: var(--wrong); }

.detail {
  padding: 12px 16px 16px; border-top: 1px solid var(--border);
  background: var(--card);
}
.list-label {
  font-size: 11px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.5px; color: var(--muted); margin: 12px 0 6px;
}
.list-label:first-child { margin-top: 0; }
.sentences { list-style: none; padding: 0; margin: 0; }
.sentence {
  padding: 8px 12px; margin: 4px 0; border-radius: 5px; font-size: 13px;
}
.sentence.right  { background: var(--right-bg);   border-left: 3px solid var(--right); }
.sentence.missed { background: var(--partial-bg); border-left: 3px solid var(--partial); }
.sentence.wrong  { background: var(--wrong-bg);   border-left: 3px solid var(--wrong); }
.sentence-text { color: var(--text); }
.meta-row { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 6px; }
.meta-pill {
  display: inline-block; font-size: 10px; padding: 2px 7px;
  border-radius: 8px; font-family: ui-monospace, Menlo, monospace;
}
.meta-gt   { background: var(--gt-meta-bg);   color: var(--gt-meta); }
.meta-pred { background: var(--pred-meta-bg); color: var(--pred-meta); }

.errors { margin-top: 12px; }
.error-item {
  padding: 8px 12px; margin: 6px 0; border-radius: 5px; font-size: 12px;
}
.error-vague   { background: var(--vague-bg);        border-left: 3px solid var(--vague); }
.error-missing { background: var(--missing-info-bg); border-left: 3px solid var(--missing-info); }
.error-other   { background: var(--bg); border-left: 3px solid var(--muted); }
.hidden { display: none !important; }

/* Compact count badges */
.cat-counts {
  display: inline-flex; align-items: center; gap: 5px;
}
.cat-counts-sm .count-badge { padding: 3px 9px; font-size: 12px; }
.cat-counts-lg .count-badge { padding: 4px 11px; font-size: 15px; }
.count-badge {
  display: inline-block; min-width: 26px; text-align: center;
  border-radius: 10px; font-weight: 700; line-height: 1;
}
.count-right    { background: var(--right-bg);    color: var(--right); }
.count-partial  { background: var(--partial-bg);  color: var(--partial); }
.count-q-missed { background: var(--q-missed-bg); color: var(--q-missed); }
.count-s-missed { background: var(--partial-bg);  color: var(--partial); }
.count-wrong    { background: var(--wrong-bg);    color: var(--wrong); }
.count-sep { color: var(--muted); font-weight: 600; font-size: 12px; }
.cat-total { color: var(--muted); font-size: 11px; margin-left: 4px; }
"""

JS = """
function applyFilters() {
  const hidePerfect = document.getElementById('hide-perfect').checked;
  const query = document.getElementById('search').value.toLowerCase().trim();
  document.querySelectorAll('details.question').forEach(q => {
    const isPerfect = q.dataset.perfect === 'true';
    const text = q.dataset.question || '';
    let show = true;
    if (hidePerfect && isPerfect) show = false;
    if (query && !text.includes(query)) show = false;
    q.classList.toggle('hidden', !show);
  });
  document.querySelectorAll('details.category').forEach(cat => {
    const visible = cat.querySelectorAll('details.question:not(.hidden)').length;
    cat.classList.toggle('hidden', visible === 0);
  });
}
function expandAll() { document.querySelectorAll('details').forEach(d => d.open = true); }
function collapseAll() { document.querySelectorAll('details').forEach(d => d.open = false); }
"""


def build_page(per_model):
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    models_html = "".join(render_model(mid, data) for mid, data in per_model.items())

    g_right, g_partial, g_missed, g_wrong, g_total = _grand_quad(per_model)
    grand_gt_right  = sum(d["overall"].get("right",  0) for d in per_model.values())
    grand_gt_missed = sum(d["overall"].get("missed", 0) for d in per_model.values())
    grand_gt_wrong  = sum(d["overall"].get("wrong",  0) for d in per_model.values())
    grand_gt        = sum(d["overall"].get("total_ground_truth_sentences", 0)
                          for d in per_model.values())

    question_row = _render_summary_row(
        "QUESTION-LEVEL — did the matcher answer each question correctly?",
        [
            (g_right,   "Right"),
            (g_partial, "Partial"),
            (g_missed,  "Missed"),
            (g_wrong,   "Wrong"),
            (count_quad(g_right, g_partial, g_missed, g_wrong, g_total,
                        size="lg"), "Right / Partial / Missed / Wrong"),
        ],
    )
    sentence_row = _render_summary_row(
        "SENTENCE-LEVEL — how many ground-truth sentences were retrieved?",
        [
            (grand_gt_right,  "Right sentences"),
            (grand_gt_missed, "Missed sentences"),
            (grand_gt_wrong,  "Wrong sentences"),
            (count_sent(grand_gt_right, grand_gt_missed, grand_gt_wrong,
                        grand_gt, size="lg"), "Right / Missed / Wrong"),
            (grand_gt, "Total GT sentences"),
        ],
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Semantic Matcher — Evaluation Report</title>
<style>{CSS}</style>
</head>
<body>
<div class="container">
<h1>Semantic Matcher — Evaluation Report</h1>
<div class="subtitle">Generated {generated} · {len(per_model)} model card(s)</div>

{question_row}
{sentence_row}

<div class="controls">
  <input type="text" id="search" placeholder="Search question text…"
         oninput="applyFilters()">
  <label><input type="checkbox" id="hide-perfect" onchange="applyFilters()">
    Hide fully-correct questions</label>
  <button onclick="expandAll()">Expand all</button>
  <button onclick="collapseAll()">Collapse all</button>
</div>

{models_html}
</div>
<script>{JS}</script>
</body>
</html>
"""


def main():
    if not SCORES_DIR.exists():
        print("No scores/ folder. Run score_predictions.py first.")
        return

    def numeric_key(p: Path):
        return int(p.stem) if p.stem.isdigit() else -1

    per_model = {}
    for f in sorted(SCORES_DIR.glob("*.json"), key=numeric_key):
        if f.name == "summary.json":
            continue
        with f.open(encoding="utf-8") as fh:
            data = json.load(fh)
        if "per_question" not in data:
            continue
        per_model[f.stem] = data

    if not per_model:
        print("No per-model score files found in scores/.")
        return

    html = build_page(per_model)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"✅ Wrote {OUTPUT}  ({len(html):,} bytes, {len(per_model)} model(s))")


if __name__ == "__main__":
    main()