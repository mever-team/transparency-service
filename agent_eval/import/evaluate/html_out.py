from collections import defaultdict
from html import escape
from pathlib import Path
def generate_correct_predictions(correct_predictions):
    cards = []

    for prediction in correct_predictions:
        cards.append(
            f"""
            <div class="sentence correct">
                <div class="meta">
                    <strong>File:</strong>
                    {escape(prediction["name"])}
                    &nbsp;&nbsp;
                    <strong>Similarity:</strong>
                    {prediction["similarity"]}
                    &nbsp;&nbsp;
                    <strong>Field:</strong>
                    {escape(prediction["field"])}
                </div>

                <div class="label">Predicted text</div>
                <div class="text predicted">
                    {escape(prediction["pred_text"])}
                </div>

                <div class="label">Ground-truth text</div>
                <div class="text ground-truth">
                    {escape(prediction["gt_text"])}
                </div>
            </div>
            """
        )

    return f"""
    <section>
        <h2>Correct Predictions ({len(correct_predictions)})</h2>

        <details>
            <summary>Show correct predictions</summary>
            {"".join(cards)}
        </details>
    </section>
    """
def generate_html(detailed_results, output_path: Path, confusion_matrix):
    """
    Generate an interactive HTML report containing accumulated
    field mismatches and the sentences responsible for them.

    detailed_results:
        [
            {
                "name": "...",
                "result": {...},
            },
            ...
        ]
    """
    correct_predictions = []

    for item in detailed_results:
        name = item["name"]
        result = item["result"]

        for match in result["matches"]:
            if match["status"] != "correct":
                continue

            correct_predictions.append({
                "name": name,
                "similarity": match["similarity"],
                "field": match["pred_field"],
                "pred_text": match["pred_text"],
                "gt_text": match["gt_text"],
            })
    # ---------------------------------------------------------
    # Collect all mismatches
    # ---------------------------------------------------------

    mismatches = defaultdict(list)

    for item in detailed_results:
        name = item["name"]
        result = item["result"]

        for match in result["matches"]:
            if match["status"] != "misclassified":
                continue

            key = (
                match["gt_field"],
                match["pred_field"],
            )

            mismatches[key].append({
                "name": name,
                "similarity": match["similarity"],
                "pred_text": match["pred_text"],
                "gt_text": match["gt_text"],
            })

    # Sort by number of mismatches
    sorted_mismatches = sorted(
        mismatches.items(),
        key=lambda item: len(item[1]),
        reverse=True,
    )

    # ---------------------------------------------------------
    # Build mismatch HTML
    # ---------------------------------------------------------

    mismatch_html = []

    for (gt_field, pred_field), sentences in sorted_mismatches:

        count = len(sentences)

        sentence_html = []

        for sentence in sentences:
            sentence_html.append(
                f"""
                <div class="sentence">
                    <div class="meta">
                        <strong>File:</strong>
                        {escape(sentence["name"])}
                        &nbsp;&nbsp;
                        <strong>Similarity:</strong>
                        {sentence["similarity"]}
                    </div>

                    <div class="label">Predicted text</div>
                    <div class="text predicted">
                        {escape(sentence["pred_text"])}
                    </div>

                    <div class="label">Ground truth text</div>
                    <div class="text ground-truth">
                        {escape(sentence["gt_text"])}
                    </div>
                </div>
                """
            )

        mismatch_html.append(
            f"""
            <details class="mismatch">
                <summary>
                    <span class="field gt">
                        {escape(gt_field)}
                    </span>

                    <span class="arrow">→</span>

                    <span class="field predicted-field">
                        {escape(pred_field)}
                    </span>

                    <span class="count">
                        {count}
                    </span>
                </summary>

                <div class="details-content">
                    {"".join(sentence_html)}
                </div>
            </details>
            """
        )
    # ---------------------------------------------------------
    # Collect extra / unmatched predictions
    # ---------------------------------------------------------

    extra_predictions = []

    for item in detailed_results:
        name = item["name"]
        result = item["result"]

        for extra in result["extra"]:
            extra_predictions.append({
                "name": name,
                **extra,
            })

    # ---------------------------------------------------------
    # Collect missing GT paragraphs
    # ---------------------------------------------------------

    missing_gt = []

    for item in detailed_results:
        name = item["name"]
        result = item["result"]

        for missing in result["missing"]:
            missing_gt.append({
                "name": name,
                "field": missing["field"],
                "text": missing["text"],
            })
            
    # ---------------------------------------------------------
    # Extra HTML
    # ---------------------------------------------------------

    extra_html = []

    for extra in extra_predictions:
        extra_html.append(
            f"""
            <div class="sentence">
                <div class="meta">
                    <strong>File:</strong>
                    {escape(extra["name"])}
                    &nbsp;&nbsp;
                    <strong>Best similarity:</strong>
                    {extra["similarity"]}
                    &nbsp;&nbsp;
                    <strong>Predicted field:</strong>
                    {escape(extra["pred_field"])}
                </div>

                <div class="label">Predicted text</div>
                <div class="text predicted">
                    {escape(extra["pred_text"])}
                </div>

                <div class="label">Best matching ground truth</div>
                <div class="meta">
                    <strong>GT field:</strong>
                    {escape(extra["best_gt_field"] or "None")}
                </div>

                <div class="text ground-truth">
                    {escape(extra["best_gt_text"] or "None")}
                </div>
            </div>
            """
        )

    # ---------------------------------------------------------
    # Missing GT HTML
    # ---------------------------------------------------------

    missing_html = []

    for missing in missing_gt:
        missing_html.append(
            f"""
            <div class="sentence">
                <div class="meta">
                    <strong>File:</strong>
                    {escape(missing["name"])}
                    &nbsp;&nbsp;
                    <strong>GT field:</strong>
                    {escape(missing["field"])}
                </div>

                <div class="label">Ground truth text</div>
                <div class="text ground-truth">
                    {escape(missing["text"])}
                </div>
            </div>
            """
        )
    correct_predictions_html = generate_correct_predictions(correct_predictions)
    # ---------------------------------------------------------
    # Full HTML document
    # ---------------------------------------------------------

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Model Card Evaluation - Field Mismatches</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background: #f5f5f5;
    color: #222;
    margin: 0;
    padding: 30px;
}}
.correct {{
    border-left: 5px solid #28a745;
    background: #f0fff4;
}}
.legend {{
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
    font-size: 13px;
    color: #555;
}}

.legend-item {{
    display: flex;
    align-items: center;
    gap: 7px;
}}

.legend-color {{
    width: 14px;
    height: 14px;
    border-radius: 3px;
    display: inline-block;
}}

.predicted-legend {{
    background: #fff4e6;
    border: 1px solid #f0a000;
}}

.ground-truth-legend {{
    background: #eef5ff;
    border: 1px solid #4285f4;
}}

.container {{
    max-width: 1400px;
    margin: auto;
}}

h1 {{
    margin-bottom: 5px;
}}

.subtitle {{
    color: #666;
    margin-bottom: 30px;
}}

.mismatch {{
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    margin-bottom: 10px;
    overflow: hidden;
}}

.mismatch summary {{
    cursor: pointer;
    padding: 15px 18px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 15px;
    list-style: none;
}}

.mismatch summary::-webkit-details-marker {{
    display: none;
}}

.mismatch summary:hover {{
    background: #f8f8f8;
}}

.field {{
    font-family: monospace;
    padding: 5px 8px;
    border-radius: 4px;
}}

.gt {{
    background: #e8f0ff;
}}

.predicted-field {{
    background: #fff0e0;
}}

.arrow {{
    color: #777;
    font-size: 18px;
}}

.count {{
    margin-left: auto;
    background: #333;
    color: white;
    border-radius: 20px;
    padding: 4px 10px;
    font-weight: bold;
}}

.details-content {{
    border-top: 1px solid #ddd;
    padding: 10px 18px 18px 18px;
}}

.sentence {{
    border: 1px solid #ddd;
    border-radius: 6px;
    padding: 15px;
    margin-top: 10px;
    background: #fafafa;
}}

.meta {{
    color: #666;
    font-size: 13px;
    margin-bottom: 15px;
}}

.label {{
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 5px;
}}

.text {{
    white-space: pre-wrap;
    word-break: break-word;
    padding: 10px;
    border-radius: 5px;
    font-family: monospace;
    font-size: 13px;
}}

.predicted {{
    background: #fff4e6;
    border-left: 4px solid #f0a000;
}}

.ground-truth {{
    background: #eef5ff;
    border-left: 4px solid #4285f4;
}}
.section {{
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    margin-top: 25px;
    overflow: hidden;
}}

.section summary {{
    cursor: pointer;
    padding: 15px 18px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 16px;
    font-weight: bold;
    list-style: none;
}}

.section summary::-webkit-details-marker {{
    display: none;
}}

.section summary:hover {{
    background: #f8f8f8;
}}

.section .details-content {{
    border-top: 1px solid #ddd;
    padding: 10px 18px 18px 18px;
}}

</style>
</head>

<body>

<div class="container">

<h1>Model Card Evaluation</h1>

<div class="subtitle">
Accumulated field mismatches across all evaluated model cards
</div>

<div class="legend">
    <div class="legend-item">
        <span class="legend-color predicted-legend"></span>
        <span>Predicted</span>
    </div>

    <div class="legend-item">
        <span class="legend-color ground-truth-legend"></span>
        <span>Ground Truth</span>
    </div>
</div>
<div>
    {"".join(mismatch_html)}
</div>
        <details class="section">
            <summary>
                <span>Extra / Unmatched Predictions</span>
                <span class="count">
                    {len(extra_predictions)}
                </span>
            </summary>

            <div class="details-content">
                {"".join(extra_html)}
            </div>
        </details>
        {correct_predictions_html}
        <details class="section">
            <summary>
                <span>Missing Ground Truth</span>
                <span class="count">
                    {len(missing_gt)}
                </span>
            </summary>

            <div class="details-content">
                {"".join(missing_html)}
            </div>
        </details>
</div>

</body>
</html>
"""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        html,
        encoding="utf-8",
    )