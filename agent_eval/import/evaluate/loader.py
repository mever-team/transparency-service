import json
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def find_file_pairs(gt_dir: Path, pred_dir: Path):
    """
    Pair GT and prediction files by filename.

    Example:
        gpt_reorganize/foo.json
        matcher_output/foo.json
    """
    gt_files = sorted(gt_dir.glob("*.json"))

    if not gt_files:
        raise FileNotFoundError(
            f"No JSON files found in {gt_dir}"
        )

    pairs = []

    for gt_path in gt_files:
        pred_path = pred_dir / gt_path.name

        pairs.append({
            "name": gt_path.name,
            "gt_path": gt_path,
            "pred_path": pred_path if pred_path.exists() else None,
        })

    return pairs