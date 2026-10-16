import requests
import aicard as aic
import trafilatura
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urlparse
from aicard.service.assistants import SemanticMatcher
from aicard.utils.import_addons import huggingface_redirect, github_redirect, ollama_redirect

logger = aic.service.logger.Logger()
matcher = SemanticMatcher(
    "sentence-transformers/all-mpnet-base-v2",
    external_get_timeout_sec=3,
    matching_strictness=0,
    fuzzer_weight=0.25,
    promote_filling_simple_fields=0.1)
matcher.start(logger=logger)

def fetch_ollama_models(limit: int) -> list[str]:
    models = []
    for page in range(20):
        while len(models) < limit:
            resp = requests.get(
                "https://ollama.com/search",
                params={"o": "popular", "p": page},
                timeout=15
            )
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            found = []
            for a in soup.select("a[href]"):
                path = urlparse(a["href"]).path
                if path.startswith("/library/"):
                    model = path.removeprefix("/library/").strip("/")
                    if model and "/" not in model: found.append(model)
            new_models = [m for m in dict.fromkeys(found) if m not in models]
            if not new_models: break
            models.extend(new_models)
            page += 1
    return models[:limit]


def technical_assessment(card, model_name):
    card.performance.energy_consumption = "100cll"

conn = aic.connect("http://127.0.0.1:5000", username="admin", password="admin")
card_names = {card["name"] for card in conn.status()["cards"]}
logger.info(f"bot has already registered {len(card_names)} cards")
ollama_models = fetch_ollama_models(5000)
logger.info(f"bot found {len(ollama_models)} Ollama models")
missing_models = [model for model in ollama_models if model.split("/")[-1] not in card_names]
logger.info(f"bot found {len(missing_models)} new cards to import")

matcher._wait_until_ready()
for model_id in tqdm(missing_models):
    try:
        local_card = aic.ModelCard()
        url = f"https://ollama.com/library/{model_id}"
        url = ollama_redirect(local_card, url, external_get_timeout_sec=matcher.external_get_timeout_sec, callback=technical_assessment) or url
        url = huggingface_redirect(local_card, url, external_get_timeout_sec=matcher.external_get_timeout_sec) or url
        url = github_redirect(local_card, url, external_get_timeout_sec=matcher.external_get_timeout_sec) or url
        p = urlparse(url)
        if p.scheme not in ("http", "https") or not p.netloc: raise Exception("Invalid url format")
        r = requests.get(url, timeout=matcher.external_get_timeout_sec)
        r.raise_for_status()
        url = r.url
        text = r.text
        if not urlparse(url).path.lower().endswith((".md", ".markdown")):
            text = trafilatura.extract(text, output_format="markdown", include_formatting=True, include_links=True)
        if not text: continue
        matcher.complete_from_markdown(local_card, url, text, ["",""])
        quality = local_card.quality()
        if any(existing_name in local_card.overview.name for existing_name in card_names):
            logger.warn(f"It was not immediately obvious but after parsing {model_id} was already found")
            continue
        if quality < 0.3 or not local_card.overview.name:
            logger.warn(f"Created but not submitted {model_id} due to low quality {quality:.3f}")
            local_card.overview.version = ""
            continue
        logger.info(local_card.overview.name)
        with conn.create() as card: card.merge(local_card)
    except Exception as e:
        logger.warn(f"Failed to import {model_id}: {e}")