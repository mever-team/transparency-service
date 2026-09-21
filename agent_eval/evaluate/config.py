from pathlib import Path


GT_DIR = Path("gpt_reorganize")
PRED_DIR = Path("matcher_output")
REPORT_DIR = Path("evaluation_results")

MATCH_THRESHOLD = 80.0
MIN_PREDICTION_LENGTH = 20
REPORT_FILE = REPORT_DIR / "evaluation.log"
HTML_REPORT = REPORT_DIR / "evaluation.html"

EXCLUDED_FIELDS = {
    "title",
    # "overview.name",
    "overview.date",
    # "overview.type",
    # "overview.task",
    "overview.home",
    "overview.version",
    # "use.oversight",
    # "training.standards",
    # "training.update",
    # "evaluation.standards",
    # "evaluation.update",
}