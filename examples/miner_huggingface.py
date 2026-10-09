import requests
import aicard as aic
import trafilatura
from tqdm import tqdm
from urllib.parse import urlparse, urljoin
from aicard.service.assistants import SemanticMatcher
from aicard.utils.import_addons import huggingface_redirect, github_redirect

logger = aic.service.logger.Logger()
matcher = SemanticMatcher(
    "sentence-transformers/all-mpnet-base-v2",
    external_get_timeout_sec=3,
    matching_strictness=0,
    fuzzer_weight=0.25,
    promote_filling_simple_fields=0.1)
matcher.start(logger=logger)

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

conn = aic.connect("http://127.0.0.1:5000", username="admin", password="admin")
card_names = {card["name"] for card in conn.status()["cards"]}
logger.info(f"bot has already registered {len(card_names)} cards")
missing_models = [model for model in fetch_recent_hf_models(5000) if model.split("/")[-1] not in card_names]
logger.info(f"bot found {len(missing_models)} new cards to import")

matcher._wait_until_ready()
for model_id in tqdm(missing_models):
    #try:
    local_card = aic.ModelCard()
    url = f"https://huggingface.co/{model_id}"
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
    matcher.complete_from_markdown(local_card, url, text, ["",""])
    print(local_card.overview.name)
    #except: continue
    quality = local_card.quality()
    #if not local_card.overview.name: local_card.overview.name = local_card.overview.description.get()[:120].split(" ")[0]#local_card.overview.name = f"huggingface-{model_id}"
    if quality<0.3 or not local_card.overview.name:
        logger.warn(f"Created by not published {model_id} due to low quality {local_card.quality():.3f}")
        local_card.overview.version = ""
    with conn.create() as card: card.merge(local_card)