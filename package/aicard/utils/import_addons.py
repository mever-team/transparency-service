import requests
from aicard.card import ModelCard
from urllib.parse import urlparse
import markdown2

def huggingface_redirect(card: ModelCard, url: str, external_get_timeout_sec: float):
    def md(s): return markdown2.markdown(str(s), extras=["markdown-in-html", "code-friendly"]) if s else ""

    assert isinstance(url, str)
    assert isinstance(card, ModelCard)
    url = urlparse(url)
    parts = [x for x in url.path.split("/") if x]
    model_id = "/".join(parts[:2]) if url.netloc in ("huggingface.co", "www.huggingface.co") and len(parts) >= 2 else ""
    if not model_id: raise ValueError(f"Invalid Hugging Face model URL: {url}")
    r = requests.get(f"https://huggingface.co/api/models/{model_id}", timeout=external_get_timeout_sec)
    r.raise_for_status()
    meta = r.json()
    cd = meta.get("cardData") or {}

    o = card.data.overview
    o.name = meta.get("id", "")
    o.creator = meta.get("author") or model_id.split("/")[0]
    o.version = meta.get("sha", "")[:7]
    o.license = (", ".join(x[8:] for x in meta.get("tags", []) if x.startswith("license:")) or cd.get("license", ""))
    o.home = f"https://huggingface.co/{model_id}"
    o.contact = meta.get("author", "")

    pipelines = {
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
        "time-series-forecasting": "Time Series Forecasting"
    }
    pipeline = meta.get("pipeline_tag", "")
    lib = meta.get("library_name", "") or ""
    tags = set(meta.get("tags", []))
    o.task = pipelines.get(pipeline, "unknown")
    o.type = (
        "Transformer"
        if "transformer" in tags or "transformers" in lib
        else "Generative Adversarial Network"
        if "diffusers" in lib else "unknown"
    )
    udata = card.data.use
    udata.use_cases = str(cd.get("intended_uses") or pipeline)
    udata.out_of_scope_use = str(cd.get("out_of_scope_use", ""))
    langs = [x for x in tags if x.startswith("language:") or len(x) == 2]
    if langs: udata.inputs_outputs = ", ".join(langs)
    udata.software = lib
    udata.factors = md(cd.get("factors"))
    datasets = cd.get("datasets") or meta.get("datasets") or []
    card.data.training.datasets = (", ".join(datasets) if isinstance(datasets, list) else str(datasets))
    card.data.training.motivation = md(cd.get("training_data_motivation"))
    ev = cd.get("eval_results", [])
    if ev:
        card.data.evaluation.datasets = ", ".join(filter(None, {
            x.get("dataset", {}).get("name", "")
            for x in ev if isinstance(x, dict)
        }))
        lines = [
            f"- **{x.get('task', {}).get('name', '')}** / "
            f"{x.get('dataset', {}).get('name', '')}: "
            f"{x.get('metric', {}).get('name', '')} = "
            f"`{x.get('metric', {}).get('value', '')}`"
            for x in ev
            if isinstance(x, dict) and x.get("metric", {}).get("name")
        ]
        card.data.performance.metrics = "\n".join(lines)
        card.data.performance.analysis = md("\n".join(lines))
    card.data.evaluation.motivation = md(cd.get("evaluation_data_motivation"))
    card.data.safety.ethics = md(cd.get("bias_risks_limitations"))
    card.data.safety.risks = md(cd.get("risks"))
    card.data.safety.caveats = md(cd.get("caveats_and_recommendations"))
    return f"https://huggingface.co/{model_id}/resolve/main/README.md"


def github_redirect(card: ModelCard, url: str, external_get_timeout_sec: float):
    assert isinstance(url, str)
    assert isinstance(card, ModelCard)
    url = urlparse(url)
    parts = [x for x in url.path.split("/") if x]
    if url.netloc not in ("github.com", "www.github.com") or len(parts) != 2: return ""
    r = requests.get(f"https://github.com/{parts[0]}/{parts[1]}/blob/HEAD/README.md", timeout=external_get_timeout_sec)
    return r.url.replace("https://github.com/", "https://raw.githubusercontent.com/").replace("/blob/", "/") if r.ok else ""
