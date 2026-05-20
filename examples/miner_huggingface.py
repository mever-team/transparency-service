import requests
import markdown2
import aicard as aic
from aicard.service.assistants import SemanticMatcher
from tqdm import tqdm

logger = aic.service.logger.Logger()
matcher = SemanticMatcher(
    "sentence-transformers/all-mpnet-base-v2",
    external_get_timeout_sec=3,
    matching_strictness=0.5)
matcher.start(logger=logger)
#matcher._wait_until_ready()

def _md(text: str) -> str:
    if not text: return ""
    return markdown2.markdown(text, extras=["markdown-in-html", "code-friendly"])

def hf_to_card(model_id: str, card):
    meta = requests.get(f"https://huggingface.co/api/models/{model_id}").json()
    card_data = meta.get("cardData") or {}
    card.data.overview.name=(meta.get("id", ""))
    card.data.overview.creator=(meta.get("author") or model_id.split("/")[0])
    card.data.overview.version=(meta.get("sha", "")[:7])
    card.data.overview.license=(
        ", ".join(t[len("license:"):] for t in meta.get("tags", []) if t.startswith("license:"))
        or card_data.get("license", "")
    )
    card.data.overview.home=(f"https://huggingface.co/{model_id}")
    card.data.overview.contact=(meta.get("author", ""))

    pipeline_map = {
        "text-generation": "Text Generation",
        "text2text-generation": "Text Generation",
        "text-classification": "Text Classification",
        "token-classification": "Token Classification",
        "question-answering": "Question Answering",
        "summarization": "Summarization",
        "translation": "Translation",
        "fill-mask": "Fill-Mask",
        "sentence-similarity": "Sentence Similarity",
        "feature-extraction": "Feature Extraction",
        "automatic-speech-recognition": "Automatic Speech Recognition",
        "text-to-speech": "Text-to-Speech",
        "image-classification": "Image Classification",
        "object-detection": "Object Detection",
        "image-segmentation": "Image Segmentation",
        "image-to-text": "Image-to-Text",
        "text-to-image": "Text-to-Image",
        "visual-question-answering": "Visual Question Answering",
        "document-question-answering": "Document Question Answering",
        "zero-shot-classification": "Zero-Shot Classification",
        "zero-shot-image-classification": "Zero-Shot Image Classification",
        "reinforcement-learning": "Reinforcement Learning",
        "tabular-classification": "Tabular Classification",
        "tabular-regression": "Tabular Regression",
        "time-series-forecasting": "Time Series Forecasting",
    }
    pipeline = meta.get("pipeline_tag", "")
    card.data.overview.task=(pipeline_map.get(pipeline, "unknown"))
    tags = set(meta.get("tags", []))
    if "transformer" in tags or "transformers" in meta.get("library_name", ""): card.data.overview.type=("Transformer")
    elif "diffusers" in meta.get("library_name", ""):  card.data.overview.type=("Generative Adversarial Network")
    else: card.data.overview.type=("unknown")
    description = card_data.get("description", "")
    if not description:
        url = f"https://huggingface.co/{model_id}/resolve/main/README.md"
        readme = requests.get(url)
        if readme.ok: description = readme.text
    intended = card_data.get("intended_uses", "")
    card.data.use.use_cases=(str(intended) if intended else pipeline)
    out_of_scope = card_data.get("out_of_scope_use", "")
    card.data.use.out_of_scope_use=(str(out_of_scope))
    lang_tags = [t for t in meta.get("tags", []) if t.startswith("language:") or len(t) == 2]
    if lang_tags:
        card.data.use.inputs_outputs=(", ".join(lang_tags))
    card.data.use.software=(meta.get("library_name", ""))
    factors = card_data.get("factors", "")
    card.data.use.factors=(_md(str(factors)) if factors else "")  # LongText
    datasets = card_data.get("datasets") or meta.get("datasets") or []
    card.data.training.datasets=(", ".join(datasets) if isinstance(datasets, list) else str(datasets))
    motivation = card_data.get("training_data_motivation", "")
    card.data.training.motivation=(_md(str(motivation)) if motivation else "")  # LongText
    eval_datasets = card_data.get("eval_results", [])
    if eval_datasets:
        names = list({r.get("dataset", {}).get("name", "") for r in eval_datasets if isinstance(r, dict)})
        card.data.evaluation.datasets=(", ".join(filter(None, names)))
    eval_motivation = card_data.get("evaluation_data_motivation", "")
    card.data.evaluation.motivation=(_md(str(eval_motivation)) if eval_motivation else "")  # LongText
    if eval_datasets:
        metrics_lines = []
        for r in eval_datasets:
            if not isinstance(r, dict):
                continue
            task  = r.get("task", {}).get("name", "")
            mname = r.get("metric", {}).get("name", "")
            mval  = r.get("metric", {}).get("value", "")
            dset  = r.get("dataset", {}).get("name", "")
            if mname and mval != "":
                metrics_lines.append(f"- **{task}** / {dset}: {mname} = `{mval}`")
        card.data.performance.metrics=("\n".join(metrics_lines))
        card.data.performance.analysis=(_md("\n".join(metrics_lines)))
    bias = card_data.get("bias_risks_limitations", "")
    card.data.safety.ethics=(_md(str(bias)) if bias else "")
    risks = card_data.get("risks", "")
    card.data.safety.risks=(_md(str(risks)) if risks else "")
    caveats = card_data.get("caveats_and_recommendations", "")
    card.data.safety.caveats=(_md(str(caveats)) if caveats else "")

    matcher.complete_from_text(card, url, _md(description))


def fetch_recent_hf_models(limit: int) -> list[str]:
    resp = requests.get(
        "https://huggingface.co/api/models",
        params={
            "sort": "downloads",
            "direction": -1, # descending
            "limit": limit,
        }
    )
    resp.raise_for_status()
    return [m["id"] for m in resp.json()]

# model_id = "google-bert/bert-base-uncased" # this is an example model id

conn = aic.connect("http://127.0.0.1:5000", username="admin", password="admin")
card_names = {card["name"] for card in conn.status()["cards"]}
logger.info(f"bot has already registered {len(card_names)} cards")
missing_models = [model for model in fetch_recent_hf_models(5000) if model.split("/")[-1] not in card_names]
logger.info(f"bot found {len(missing_models)} new cards to import")

for model_id in tqdm(missing_models):
    local_card = aic.ModelCard()
    hf_to_card(model_id, local_card)
    quality = local_card.quality()
    if quality<0.3:
        logger.warn(f"Created by not published {model_id} due to low quality {local_card.quality():.3f}")
        local_card.overview.version = ""
    with conn.create() as card: card.merge(local_card)