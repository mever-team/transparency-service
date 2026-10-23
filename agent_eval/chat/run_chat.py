# run_chat.py
import json
import time
from pathlib import Path
from datetime import datetime, timezone

from aicard.card.model_card import ModelCard
from aicard.service.server_card_entry import ModelCardEntry
from aicard.service.assistants import SemanticMatcher
from aicard.service.logger import Logger
from aicard.service.jobs_tracker import CardJobsTracker


logger = Logger()
dataset = Path("dataset")
predictions_dir = Path("predictions")
predictions_dir.mkdir(exist_ok=True)
job_tracker = CardJobsTracker()

QUESTION_TIMEOUT_SEC = 300  # 5 minutes per question
POLL_INTERVAL_SEC = 0.5

# Shared ground-truth file: one file for all cards
GT_FILE = dataset / "gt.json"


def convert_structure(source: dict, template: dict) -> dict:
    result = {}
    for key, value in template.items():
        if key == "title":
            result[key] = value
            continue
        if isinstance(value, dict):
            section = next(
                (item["value"] for item in source["data"] if item["name"] == key), []
            )
            source_fields = {item["name"]: item["value"] for item in section}
            result[key] = {
                field_name: (
                    source_fields[field_name]
                    if field_name in source_fields
                    else field_template
                )
                for field_name, field_template in value.items()
            }
    return result


def ask_question(md_entry, question: str) -> str:
    question_id = md_entry.chat_ask(question, matcher, logger, job_tracker)
    started = time.time()
    while True:
        if time.time() - started > QUESTION_TIMEOUT_SEC:
            raise TimeoutError(
                f"Question timed out after {QUESTION_TIMEOUT_SEC}s: {question}"
            )
        if md_entry.check_completion():
            time.sleep(POLL_INTERVAL_SEC)
            continue
        with md_entry:
            isdone, answer = md_entry.chat_reply(question_id)
        return answer


# ── Load questions from the shared gt.json ────────────────────────────
with GT_FILE.open(encoding="utf-8") as f:
    gt = json.load(f)

# gt.json structure:
# {
#   "overview":   [{"question": "...", "target_fields": [...]}, ...],
#   "use":        [{"question": "...", "target_fields": [...]}, ...],
#   ...
# }
# We only need the question strings for prediction generation.
QUESTIONS = {
    category: [entry["question"] for entry in entries]
    for category, entries in gt.items()
}


matcher = SemanticMatcher(
    "sentence-transformers/all-mpnet-base-v2",
    external_get_timeout_sec=3,
    matching_strictness=0.5,
)
matcher.start(logger)


def numeric_key(p: Path):
    return int(p.name) if p.name.isdigit() else -1


for folder in sorted(dataset.iterdir(), key=numeric_key):
    if not folder.is_dir() or not folder.name.isdigit():
        continue

    json_file = next(folder.glob("*.json"))
    with json_file.open(encoding="utf-8") as f:
        md_json = json.load(f)

    md = ModelCard()
    converted = convert_structure(source=md_json, template=md.data)
    md.data.assign(converted)
    md_entry = ModelCardEntry(md, "user", None)

    model_predictions = {
        "_meta": {
            "model_card": str(json_file),
            "started_at": datetime.now(timezone.utc).isoformat(),
            "matcher": "sentence-transformers/all-mpnet-base-v2",
            "matching_strictness": 0.5,
            "questions_source": str(GT_FILE),
        }
    }

    for category, questions in QUESTIONS.items():
        category_predictions = []
        for question in questions:
            entry = {"question": question}
            try:
                answer = ask_question(md_entry, question)
                entry["answer"] = answer
            except Exception as exc:
                entry["error"] = f"{type(exc).__name__}: {exc}"
                logger.error(f"[{folder.name}][{category}] {question} failed: {exc}")
            category_predictions.append(entry)
            print(
                f"[{folder.name}][{category}] {question} "
                f"-> {(entry.get('answer') or entry.get('error') or '')[:100]}"
            )
        model_predictions[category] = category_predictions

    model_predictions["_meta"]["finished_at"] = datetime.now(timezone.utc).isoformat()

    out_file = predictions_dir / f"{folder.name}.json"
    with out_file.open("w", encoding="utf-8") as f:
        json.dump(model_predictions, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved predictions to {out_file}")