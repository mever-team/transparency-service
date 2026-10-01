from aicard.card import ModelCard
from aicard.service.assistants import SemanticMatcher
from aicard.service.logger import Logger
from urllib.parse import urlparse
import markdown2
import requests
import tempfile
import webbrowser

logger = Logger()
matcher = SemanticMatcher(
    "sentence-transformers/all-mpnet-base-v2",
    external_get_timeout_sec=3,
    matching_strictness=0.0,
    fuzzer_weight=0.25
).start(logger)

def _md(text: str) -> str: return markdown2.markdown(text, extras=["markdown-in-html", "code-friendly"]) if text else ""
def _is_markdown_url(url: str) -> bool: return urlparse(url).path.lower().endswith((".md", ".markdown"))
def _hf_model_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc not in ("huggingface.co", "www.huggingface.co"): return ""
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts)<2: return ""
    return "/".join(parts[:2])

def complete_from_huggingface(card: ModelCard, url: str):
    model_id = _hf_model_id(url)
    if not model_id: raise ValueError(f"Invalid Hugging Face model URL: {url}")

    response = requests.get(f"https://huggingface.co/api/models/{model_id}", timeout=10)
    response.raise_for_status()
    meta = response.json()
    card_data = meta.get("cardData") or {}

    card.data.overview.name = meta.get("id", "")
    card.data.overview.creator = meta.get("author") or model_id.split("/")[0]
    card.data.overview.version = meta.get("sha", "")[:7]
    card.data.overview.license = (
        ", ".join(t[len("license:"):] for t in meta.get("tags", []) if t.startswith("license:"))
        or card_data.get("license", "")
    )
    card.data.overview.home = f"https://huggingface.co/{model_id}"
    card.data.overview.contact = meta.get("author", "")

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
    card.data.overview.task = pipeline_map.get(pipeline, "unknown")

    tags = set(meta.get("tags", []))
    if "transformer" in tags or "transformers" in meta.get("library_name", ""): card.data.overview.type = "Transformer"
    elif "diffusers" in meta.get("library_name", ""): card.data.overview.type = "Generative Adversarial Network"
    else: card.data.overview.type = "unknown"

    intended = card_data.get("intended_uses", "")
    card.data.use.use_cases = str(intended) if intended else pipeline
    out_of_scope = card_data.get("out_of_scope_use", "")
    card.data.use.out_of_scope_use = str(out_of_scope)

    lang_tags = [t for t in meta.get("tags", []) if t.startswith("language:") or len(t)==2]
    if lang_tags: card.data.use.inputs_outputs = ", ".join(lang_tags)
    card.data.use.software = meta.get("library_name", "")

    factors = card_data.get("factors", "")
    card.data.use.factors = _md(str(factors)) if factors else ""

    datasets = card_data.get("datasets") or meta.get("datasets") or []
    card.data.training.datasets = ", ".join(datasets) if isinstance(datasets, list) else str(datasets)
    motivation = card_data.get("training_data_motivation", "")
    card.data.training.motivation = _md(str(motivation)) if motivation else ""

    eval_datasets = card_data.get("eval_results", [])
    if eval_datasets:
        names = list({r.get("dataset", {}).get("name", "") for r in eval_datasets if isinstance(r, dict)})
        card.data.evaluation.datasets = ", ".join(filter(None, names))

    eval_motivation = card_data.get("evaluation_data_motivation", "")
    card.data.evaluation.motivation = _md(str(eval_motivation)) if eval_motivation else ""

    if eval_datasets:
        metrics_lines = []
        for r in eval_datasets:
            if not isinstance(r, dict): continue
            task = r.get("task", {}).get("name", "")
            mname = r.get("metric", {}).get("name", "")
            mval = r.get("metric", {}).get("value", "")
            dset = r.get("dataset", {}).get("name", "")
            if mname and mval!="": metrics_lines.append(f"- **{task}** / {dset}: {mname} = `{mval}`")
        card.data.performance.metrics = "\n".join(metrics_lines)
        card.data.performance.analysis = _md("\n".join(metrics_lines))

    bias = card_data.get("bias_risks_limitations", "")
    card.data.safety.ethics = _md(str(bias)) if bias else ""
    risks = card_data.get("risks", "")
    card.data.safety.risks = _md(str(risks)) if risks else ""
    caveats = card_data.get("caveats_and_recommendations", "")
    card.data.safety.caveats = _md(str(caveats)) if caveats else ""

    readme_url = f"https://huggingface.co/{model_id}/resolve/main/README.md"
    logger.info(f"Readme: {readme_url}")
    readme = requests.get(readme_url, timeout=10)
    if not readme.ok: return []
    return matcher.complete_from_markdown(card, readme_url, readme.text)


def _github_readme_url(url: str) -> str:
    p = urlparse(url)
    if p.netloc not in ("github.com", "www.github.com"): return ""
    parts = [x for x in p.path.split("/") if x]
    if len(parts) != 2: return ""

    repo = f"https://github.com/{parts[0]}/{parts[1]}"
    r = requests.get(f"{repo}/blob/HEAD/README.md", timeout=10)
    if not r.ok: return ""

    return r.url.replace("https://github.com/", "https://raw.githubusercontent.com/").replace("/blob/", "/")

def complete_from_url(card: ModelCard, url: str, levels=1, visited=None):
    visited = visited or set()
    if url in visited: return
    visited.add(url)

    github_readme = _github_readme_url(url)
    if github_readme:
        logger.info(f"GitHub repository detected: {url} -> {github_readme}")
        url = github_readme

    model_id = _hf_model_id(url)
    if model_id:
        logger.info(f"Hugging Face model detected: {model_id}")
        urls = complete_from_huggingface(card, url) or []
    else:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        if _is_markdown_url(url):
            logger.info(f"Markdown detected: {url}")
            urls = matcher.complete_from_markdown(card, url, response.text) or []
        else:
            logger.info(f"HTML/text detected: {url}")
            urls = matcher.complete_from_text(card, url, response.text) or []

    if levels:
        for u in urls:
            print(u)
            if u.startswith(("http://", "https://")):
                complete_from_url(card, u, levels - 1, visited)


# url = "https://raw.githubusercontent.com/QwenLM/Qwen-Image-2.1/refs/heads/main/README.md"
url = "https://huggingface.co/Qwen/Qwen-Image-2.1"

card = ModelCard()
complete_from_url(card, url)

html = card.to_html_card().to_html()
with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html)
    path = f.name
webbrowser.open("file://" + path)