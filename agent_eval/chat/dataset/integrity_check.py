"""
integrity_check.py

Walks every numbered subfolder (1/, 2/, 3/, ...) next to this script, loads
the model card (*.json — any filename) and ground_truth.py in each, and
verifies that every sentence listed in GROUND_TRUTH exists verbatim in the
model card.

For each ground-truth sentence, two checks run:

  1. EXISTENCE    — the sentence appears (verbatim, as a substring) inside
                    the value of at least one field in the model card.
  2. FIELD MATCH  — the sentence appears inside the *specific* section/field
                    it was tagged with. This catches cases where a sentence
                    is real but was attributed to the wrong field.

Both checks are fatal by default. Exit code is 0 only if every sentence in
every folder passes both checks.

Usage:
    python integrity_check.py            # scans the script's own directory
    python integrity_check.py /some/dir  # scans a custom directory
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Iterable


# ── Loading helpers ──────────────────────────────────────────────────────


def find_model_card(folder: Path) -> Path:
    candidates = sorted(folder.glob("*.json"), key=lambda p: p.name)
    if not candidates:
        raise FileNotFoundError(f"No .json model card found in {folder}")
    if len(candidates) > 1:
        names = ", ".join(p.name for p in candidates)
        raise RuntimeError(f"Multiple .json files in {folder}: {names}")
    return candidates[0]


def find_ground_truth(folder: Path) -> Path:
    path = folder / "ground_truth.py"
    if not path.exists():
        raise FileNotFoundError(f"No ground_truth.py in {folder}")
    return path


def load_ground_truth(path: Path) -> dict:
    module_name = f"_gt_{path.parent.name}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "GROUND_TRUTH"):
        raise RuntimeError(f"{path} does not define GROUND_TRUTH")
    return module.GROUND_TRUTH


# ── Indexing the model card ──────────────────────────────────────────────


def index_card(model_card: dict) -> dict[str, dict[str, str]]:
    """Return {section_name: {field_name: field_value_as_string}}."""
    index: dict[str, dict[str, str]] = {}
    for section in model_card.get("data", []):
        section_name = section.get("name", "")
        index[section_name] = {}
        for field in section.get("value", []):
            field_name = field.get("name", "")
            value = field.get("value", "")
            # Guard against null values
            index[section_name][field_name] = value if isinstance(value, str) else str(value)
    return index


def sentence_exists_anywhere(sentence: str, index: dict[str, dict[str, str]]) -> bool:
    for fields in index.values():
        for value in fields.values():
            if sentence in value:
                return True
    return False


# ── Iterating ground truth ───────────────────────────────────────────────


def iter_sentences(ground_truth: dict) -> Iterable[tuple]:
    """Yield (category, question, section, field, sentence) for every entry."""
    for category, items in ground_truth.items():
        for item in items:
            question = item["question"]
            for gt in item["ground_truth"]:
                yield category, question, gt["section"], gt["field"], gt["sentence"]


# ── Per-folder check ─────────────────────────────────────────────────────


def check_folder(folder: Path) -> dict:
    report = {
        "folder": folder.name,
        "model_card": None,
        "sentences": 0,
        "existence_errors": [],
        "field_mismatches": [],
        "load_error": None,
    }

    try:
        card_path = find_model_card(folder)
        gt_path = find_ground_truth(folder)
        model_card = json.loads(card_path.read_text(encoding="utf-8"))
        ground_truth = load_ground_truth(gt_path)
    except Exception as exc:
        report["load_error"] = str(exc)
        return report

    report["model_card"] = card_path.name
    index = index_card(model_card)

    for category, question, section, field, sentence in iter_sentences(ground_truth):
        report["sentences"] += 1

        # 1. Existence check
        if not sentence_exists_anywhere(sentence, index):
            report["existence_errors"].append(
                {
                    "category": category,
                    "question": question,
                    "section": section,
                    "field": field,
                    "sentence": sentence,
                }
            )
            continue

        # 2. Field-match check
        field_value = index.get(section, {}).get(field)
        if field_value is None:
            report["field_mismatches"].append(
                {
                    "category": category,
                    "question": question,
                    "section": section,
                    "field": field,
                    "sentence": sentence,
                    "reason": "section/field does not exist in model card",
                }
            )
        elif sentence not in field_value:
            report["field_mismatches"].append(
                {
                    "category": category,
                    "question": question,
                    "section": section,
                    "field": field,
                    "sentence": sentence,
                    "reason": "sentence exists elsewhere but not in the tagged field",
                }
            )

    return report


def report_is_ok(report: dict) -> bool:
    if report["load_error"]:
        return False
    return not report["existence_errors"] and not report["field_mismatches"]


# ── Reporting ────────────────────────────────────────────────────────────


def print_report(report: dict) -> None:
    name = report["folder"]

    if report["load_error"]:
        print(f"\n[{name}] LOAD ERROR")
        print(f"  {report['load_error']}")
        return

    status = "OK" if report_is_ok(report) else "FAIL"
    print(
        f"\n[{name}] {status}  "
        f"(model card: {report['model_card']}, {report['sentences']} sentences)"
    )

    if report["existence_errors"]:
        print(f"  ✗ {len(report['existence_errors'])} sentence(s) not found in the model card:")
        for err in report["existence_errors"]:
            print(f"    - [{err['category']}] {err['question']}")
            print(f"      section={err['section']!r}  field={err['field']!r}")
            print(f"      sentence={err['sentence']!r}")

    if report["field_mismatches"]:
        print(f"  ✗ {len(report['field_mismatches'])} sentence(s) in the wrong field:")
        for mm in report["field_mismatches"]:
            print(f"    - [{mm['category']}] {mm['question']}")
            print(f"      section={mm['section']!r}  field={mm['field']!r}")
            print(f"      reason: {mm['reason']}")
            print(f"      sentence={mm['sentence']!r}")


# ── Main ─────────────────────────────────────────────────────────────────


def discover_folders(root: Path) -> list[Path]:
    folders = [p for p in root.iterdir() if p.is_dir() and p.name.isdigit()]
    return sorted(folders, key=lambda p: int(p.name))


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    root = Path(argv[0]).resolve() if argv else Path(__file__).resolve().parent

    folders = discover_folders(root)
    if not folders:
        print(f"No numbered folders (1/, 2/, ...) found in {root}")
        return 1

    reports = []
    for folder in folders:
        report = check_folder(folder)
        print_report(report)
        reports.append(report)

    print("\n=== Summary ===")
    all_ok = True
    for report in reports:
        ok = report_is_ok(report)
        all_ok = all_ok and ok
        mark = "OK  " if ok else "FAIL"
        extra = ""
        if report["load_error"]:
            extra = f"  ({report['load_error']})"
        elif not ok:
            extra = (
                f"  ({len(report['existence_errors'])} missing, "
                f"{len(report['field_mismatches'])} misplaced)"
            )
        print(f"  {mark} {report['folder']}{extra}")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())