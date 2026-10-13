import json
import html
from pathlib import Path


DATASET_PATH = "dataset.json"
EVALUATION_RESULTS_PATH = "evaluation_results.json"
ANALYSIS_REPORT_PATH = "analysis_report.json"
FAITHFULNESS_RESULTS_PATH = "faithfulness_results.json"

OUTPUT_PATH = "evaluation_report.html"


# ============================================================
# Helpers
# ============================================================

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def esc(value):
    """Escape text for safe HTML output."""
    return html.escape(str(value))


def percent(value):
    return f"{value * 100:.2f}%"


def metric_card(title, value, subtitle=""):
    return f"""
    <div class="metric-card">
        <div class="metric-title">{esc(title)}</div>
        <div class="metric-value">{esc(value)}</div>
        <div class="metric-subtitle">{esc(subtitle)}</div>
    </div>
    """


def status_badge(value):
    value = str(value).upper()

    classes = {
        "YES": "yes",
        "SUPPORTED": "yes",
        "PARTIAL": "partial",
        "NO": "no",
        "UNSUPPORTED": "no",
        "CONTRADICTION": "contradiction",
    }

    css_class = classes.get(value, "neutral")

    return (
        f'<span class="badge {css_class}">'
        f'{esc(value)}'
        f'</span>'
    )


def get_type_metrics(metrics, item_type):
    return metrics.get("by_type", {}).get(
        item_type,
        {
            "total_requirements": 0,
            "information_present": 0,
            "information_presence": 0,
            "fully_satisfied": 0,
            "partially_satisfied": 0,
            "not_satisfied": 0,
            "satisfaction_score": 0,
        }
    )


# ============================================================
# Metric sections
# ============================================================

def render_metric_table(metrics):
    rows = ""

    for item_type in (
        "mention",
        "explain",
        "constraint",
    ):

        m = get_type_metrics(metrics, item_type)

        total = m["total_requirements"]

        if total == 0:
            continue

        rows += f"""
        <tr>
            <td>
                <strong>{esc(item_type.capitalize())}</strong>
            </td>

            <td>{m["total_requirements"]}</td>

            <td>
                {m["information_present"]} /
                {total}
                <span class="muted">
                    ({percent(m["information_presence"])})
                </span>
            </td>

            <td>
                {m["fully_satisfied"]} /
                {total}
                <span class="muted">
                    ({percent(
                        m["fully_satisfied"] / total
                    )})
                </span>
            </td>

            <td>
                {m["partially_satisfied"]} /
                {total}
                <span class="muted">
                    ({percent(
                        m["partially_satisfied"] / total
                    )})
                </span>
            </td>

            <td>
                {m["not_satisfied"]} /
                {total}
                <span class="muted">
                    ({percent(
                        m["not_satisfied"] / total
                    )})
                </span>
            </td>

            <td>
                <strong>
                    {percent(m["satisfaction_score"])}
                </strong>
            </td>
        </tr>
        """

    return f"""
    <table>
        <thead>
            <tr>
                <th>Type</th>
                <th>Total</th>
                <th>Information present</th>
                <th>Fully satisfied</th>
                <th>Partially satisfied</th>
                <th>Not satisfied</th>
                <th>Satisfaction score</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
    """


# ============================================================
# Requirement evaluation
# ============================================================

def render_requirements(evaluation_sample):

    checklist = {
        item["id"]: item
        for item in evaluation_sample["checklist"]
    }

    rows = ""

    for result in evaluation_sample["checklist_results"]:

        item = checklist.get(result["id"], {})

        item_type = item.get(
            "type",
            result.get("type", "unknown")
        )

        rows += f"""
        <tr
            data-type="{esc(item_type)}"
            data-satisfaction="{esc(
                result["satisfaction"]
            )}"
        >

            <td>{result["id"]}</td>

            <td>
                {status_badge(item_type)}
            </td>

            <td>
                {esc(result["requirement"])}
            </td>

            <td>
                {status_badge(
                    "YES"
                    if result["information_present"]
                    else "NO"
                )}
            </td>

            <td>
                {status_badge(
                    result["satisfaction"]
                )}
            </td>

            <td class="reason">
                {esc(result.get("reason", ""))}
            </td>

        </tr>
        """

    return f"""
    <div class="table-controls">

        <select
            onchange="filterRequirements(this)"
        >
            <option value="all">
                All types
            </option>

            <option value="mention">
                Mention
            </option>

            <option value="explain">
                Explain
            </option>

            <option value="constraint">
                Constraint
            </option>
        </select>

        <select
            onchange="filterSatisfaction(this)"
        >
            <option value="all">
                All satisfaction results
            </option>

            <option value="YES">
                Fully satisfied
            </option>

            <option value="PARTIAL">
                Partially satisfied
            </option>

            <option value="NO">
                Not satisfied
            </option>
        </select>

    </div>

    <table class="requirements-table">

        <thead>
            <tr>
                <th>ID</th>
                <th>Type</th>
                <th>Requirement</th>
                <th>Information</th>
                <th>Satisfaction</th>
                <th>Reason</th>
            </tr>
        </thead>

        <tbody>
            {rows}
        </tbody>

    </table>
    """


# ============================================================
# Faithfulness
# ============================================================

def render_faithfulness(faithfulness_sample):

    metrics = faithfulness_sample["metrics"]

    rows = ""

    for claim in faithfulness_sample.get(
        "claims",
        []
    ):

        verdict = claim.get(
            "verdict",
            "UNKNOWN"
        )

        rows += f"""
        <tr
            data-verdict="{esc(verdict)}"
        >

            <td class="claim">
                {esc(claim.get("claim", ""))}
            </td>

            <td>
                {status_badge(verdict)}
            </td>

            <td class="evidence">
                {esc(claim.get("evidence", ""))}
            </td>

            <td class="reason">
                {esc(claim.get("reason", ""))}
            </td>

        </tr>
        """

    return f"""
    <div class="faithfulness-summary">

        {metric_card(
            "Total claims",
            metrics["total_claims"]
        )}

        {metric_card(
            "Supported",
            metrics["supported_claims"]
        )}

        {metric_card(
            "Partial",
            metrics["partial_claims"]
        )}

        {metric_card(
            "Unsupported",
            metrics["unsupported_claims"]
        )}

        {metric_card(
            "Contradictions",
            metrics["contradiction_claims"]
        )}

        {metric_card(
            "Factual faithfulness",
            percent(
                metrics["factual_faithfulness"]
            )
        )}

        {metric_card(
            "Unsupported claim rate",
            percent(
                metrics["unsupported_claim_rate"]
            )
        )}

    </div>

    <table class="faithfulness-table">
        <thead>
            <tr>
                <th>Claim</th>
                <th>Verdict</th>
                <th>Source evidence</th>
                <th>Reason</th>
            </tr>
        </thead>

        <tbody>
            {rows}
        </tbody>
    </table>
    """


# ============================================================
# Sample rendering
# ============================================================

def render_sample(
    dataset_sample,
    evaluation_sample,
    analysis_sample,
    faithfulness_sample,
):

    sample_id = dataset_sample["id"]

    input_text = dataset_sample["input"]
    prediction = evaluation_sample["prediction"]

    overall_metrics = analysis_sample["metrics"]["overall"]

    return f"""
    <section
        class="sample"
        id="sample-{sample_id}"
    >

        <div class="sample-header">
            <h2>
                Sample {sample_id}
            </h2>

            <a
                href="{esc(dataset_sample["source"])}"
                target="_blank"
                rel="noopener"
            >
                Source ↗
            </a>
        </div>

        <!-- ================================================= -->
        <!-- Text comparison -->
        <!-- ================================================= -->

        <div class="comparison">

            <div class="text-panel">
                <h3>Original sentence</h3>
                <p>{esc(input_text)}</p>
            </div>

            <div class="text-panel prediction">
                <h3>Generated explanation</h3>
                <p>{esc(prediction)}</p>
            </div>

        </div>

        <!-- ================================================= -->
        <!-- Overall sample metrics -->
        <!-- ================================================= -->

        <h3>Evaluation metrics</h3>

        <div class="metric-grid">

            {metric_card(
                "Requirements",
                overall_metrics["total_requirements"]
            )}

            {metric_card(
                "Information present",
                f'{overall_metrics["information_present"]} '
                f'/ {overall_metrics["total_requirements"]}',
                percent(
                    overall_metrics["information_presence"]
                )
            )}

            {metric_card(
                "Fully satisfied",
                overall_metrics["fully_satisfied"]
            )}

            {metric_card(
                "Partially satisfied",
                overall_metrics["partially_satisfied"]
            )}

            {metric_card(
                "Not satisfied",
                overall_metrics["not_satisfied"]
            )}

            {metric_card(
                "Satisfaction score",
                percent(
                    overall_metrics["satisfaction_score"]
                )
            )}

        </div>

        <!-- ================================================= -->
        <!-- Type metrics -->
        <!-- ================================================= -->

        <h3>Metrics by requirement type</h3>

        {render_metric_table(
            analysis_sample["metrics"]
        )}

        <!-- ================================================= -->
        <!-- Requirements -->
        <!-- ================================================= -->

        <details>
            <summary>
                <strong>
                    Requirement-level evaluation
                </strong>
            </summary>

            {render_requirements(
                evaluation_sample
            )}

        </details>

        <!-- ================================================= -->
        <!-- Faithfulness -->
        <!-- ================================================= -->

        <details open>
            <summary>
                <strong>
                    Factual faithfulness
                </strong>
            </summary>

            {render_faithfulness(
                faithfulness_sample
            )}

        </details>

    </section>
    """


# ============================================================
# Main HTML
# ============================================================

def generate_html(
    dataset,
    evaluation_results,
    analysis_report,
    faithfulness_results,
):

    evaluation_samples = {
        sample["id"]: sample
        for sample in evaluation_results["samples"]
    }

    analysis_samples = {
        sample["id"]: sample
        for sample in analysis_report["samples"]
    }

    faithfulness_samples = {
        sample["id"]: sample
        for sample in faithfulness_results["samples"]
    }

    overall = analysis_report[
        "overall_metrics"
    ]["overall"]

    overall_by_type = analysis_report[
        "overall_metrics"
    ]

    faithfulness_metrics = faithfulness_results[
        "metrics"
    ]

    samples_html = ""

    for sample in dataset:

        sample_id = sample["id"]

        samples_html += render_sample(
            sample,
            evaluation_samples[sample_id],
            analysis_samples[sample_id],
            faithfulness_samples[sample_id],
        )

    return f"""<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>Model Explanation Evaluation</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    background: #f5f7fa;
    color: #1f2937;
    line-height: 1.6;
}}

header {{
    background: #111827;
    color: white;
    padding: 40px;
}}

header h1 {{
    margin: 0 0 8px 0;
    font-size: 32px;
}}

header p {{
    margin: 0;
    opacity: 0.75;
}}

.container {{
    max-width: 1500px;
    margin: 0 auto;
    padding: 30px;
}}

.overview {{
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin-bottom: 35px;
}}

.metric-card {{
    background: white;
    border-radius: 12px;
    padding: 20px;
    border: 1px solid #e5e7eb;
    box-shadow:
        0 2px 5px rgba(0, 0, 0, 0.04);
}}

.metric-title {{
    font-size: 13px;
    color: #6b7280;
    margin-bottom: 6px;
}}

.metric-value {{
    font-size: 26px;
    font-weight: 700;
}}

.metric-subtitle {{
    font-size: 12px;
    color: #9ca3af;
    margin-top: 4px;
}}

.metric-grid {{
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
    margin-bottom: 25px;
}}

.faithfulness-summary {{
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(160px, 1fr));
    gap: 12px;
    margin: 20px 0;
}}

section {{
    background: white;
    border-radius: 14px;
    padding: 30px;
    margin-bottom: 30px;
    border: 1px solid #e5e7eb;
    box-shadow:
        0 3px 10px rgba(0, 0, 0, 0.04);
}}

.sample-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    margin-bottom: 20px;
}}

.sample-header h2 {{
    margin: 0;
}}

.sample-header a {{
    color: #2563eb;
    text-decoration: none;
}}

.comparison {{
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(350px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}}

.text-panel {{
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 20px;
}}

.text-panel h3 {{
    margin-top: 0;
    font-size: 15px;
}}

.text-panel p {{
    white-space: pre-wrap;
}}

.prediction {{
    background: #f8fafc;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
    font-size: 14px;
}}

th {{
    background: #f3f4f6;
    text-align: left;
    padding: 12px;
    border-bottom: 2px solid #e5e7eb;
}}

td {{
    padding: 12px;
    border-bottom: 1px solid #e5e7eb;
    vertical-align: top;
}}

tr:hover {{
    background: #fafafa;
}}

.badge {{
    display: inline-block;
    padding: 3px 9px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.3px;
}}

.badge.yes {{
    background: #dcfce7;
    color: #166534;
}}

.badge.partial {{
    background: #fef3c7;
    color: #92400e;
}}

.badge.no {{
    background: #fee2e2;
    color: #991b1b;
}}

.badge.contradiction {{
    background: #fce7f3;
    color: #9d174d;
}}

.badge.neutral {{
    background: #e5e7eb;
    color: #374151;
}}

.muted {{
    color: #6b7280;
}}

.reason {{
    color: #4b5563;
    max-width: 400px;
}}

.claim {{
    min-width: 250px;
}}

.evidence {{
    color: #374151;
    min-width: 200px;
}}

details {{
    margin-top: 25px;
    border-top: 1px solid #e5e7eb;
    padding-top: 20px;
}}

summary {{
    cursor: pointer;
    font-size: 16px;
    padding: 10px 0;
}}

.table-controls {{
    display: flex;
    gap: 10px;
    margin: 15px 0;
}}

select {{
    padding: 8px 12px;
    border: 1px solid #d1d5db;
    border-radius: 7px;
    background: white;
}}

@media (max-width: 800px) {{

    header {{
        padding: 25px;
    }}

    .container {{
        padding: 15px;
    }}

    section {{
        padding: 18px;
    }}

    table {{
        display: block;
        overflow-x: auto;
    }}

}}

</style>

</head>

<body>

<header>

<div class="container">

<h1>
Model Explanation Evaluation
</h1>

<p>
Checklist-based evaluation and factual faithfulness analysis
</p>

</div>

</header>


<div class="container">

<!-- ====================================================== -->
<!-- Overview -->
<!-- ====================================================== -->

<h2>Overall results</h2>

<div class="overview">

{metric_card(
    "Samples",
    len(dataset)
)}

{metric_card(
    "Requirements",
    overall["total_requirements"]
)}

{metric_card(
    "Information present",
    f'{overall["information_present"]} '
    f'/ {overall["total_requirements"]}',
    percent(
        overall["information_presence"]
    )
)}

{metric_card(
    "Fully satisfied",
    overall["fully_satisfied"]
)}

{metric_card(
    "Partially satisfied",
    overall["partially_satisfied"]
)}

{metric_card(
    "Not satisfied",
    overall["not_satisfied"]
)}

{metric_card(
    "Satisfaction score",
    percent(
        overall["satisfaction_score"]
    )
)}

{metric_card(
    "Total claims",
    faithfulness_metrics["total_claims"]
)}

{metric_card(
    "Factual faithfulness",
    percent(
        faithfulness_metrics[
            "factual_faithfulness"
        ]
    )
)}

{metric_card(
    "Unsupported claim rate",
    percent(
        faithfulness_metrics[
            "unsupported_claim_rate"
        ]
    )
)}

</div>


<!-- ====================================================== -->
<!-- Overall type metrics -->
<!-- ====================================================== -->

<h2>Metrics by requirement type</h2>

{render_metric_table(
    overall_by_type
)}


<!-- ====================================================== -->
<!-- Faithfulness overview -->
<!-- ====================================================== -->

<h2>Overall factual faithfulness</h2>

<div class="overview">

{metric_card(
    "Supported",
    faithfulness_metrics[
        "supported_claims"
    ]
)}

{metric_card(
    "Partial",
    faithfulness_metrics[
        "partial_claims"
    ]
)}

{metric_card(
    "Unsupported",
    faithfulness_metrics[
        "unsupported_claims"
    ]
)}

{metric_card(
    "Contradictions",
    faithfulness_metrics[
        "contradiction_claims"
    ]
)}

</div>


<!-- ====================================================== -->
<!-- Samples -->
<!-- ====================================================== -->

<h2>Detailed sample analysis</h2>

{samples_html}

</div>


<script>

function filterRequirements(select) {{

    const value = select.value;

    const table =
        select.closest("details")
        .querySelector(".requirements-table");

    const rows =
        table.querySelectorAll("tbody tr");

    rows.forEach(row => {{

        if (value === "all") {{
            row.style.display = "";
            return;
        }}

        row.style.display =
            row.dataset.type === value
                ? ""
                : "none";
    }});
}}


function filterSatisfaction(select) {{

    const value = select.value;

    const table =
        select.closest("details")
        .querySelector(".requirements-table");

    const rows =
        table.querySelectorAll("tbody tr");

    rows.forEach(row => {{

        if (value === "all") {{
            row.style.display = "";
            return;
        }}

        row.style.display =
            row.dataset.satisfaction === value
                ? ""
                : "none";
    }});
}}

</script>

</body>

</html>
"""


# ============================================================
# Main
# ============================================================

def main():

    print("Loading evaluation files...")

    dataset = load_json(DATASET_PATH)

    evaluation_results = load_json(
        EVALUATION_RESULTS_PATH
    )

    analysis_report = load_json(
        ANALYSIS_REPORT_PATH
    )

    faithfulness_results = load_json(
        FAITHFULNESS_RESULTS_PATH
    )

    print("Generating HTML report...")

    html_output = generate_html(
        dataset,
        evaluation_results,
        analysis_report,
        faithfulness_results,
    )

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html_output)

    print(
        f"Saved report to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()