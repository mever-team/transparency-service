import aicard as aic
import requests
import trafilatura
from tqdm import tqdm

from aicard.service.logger import Logger
from aicard.utils.import_addons import huggingface_redirect, github_redirect, ollama_redirect
from aicard.service.assistants import SemanticMatcher
from urllib.parse import urlparse

conn = aic.connect("https://trai.mever.gr", username="admin", password="admin")
card_names = {card["name"] for card in conn.status()["cards"]}

logger = aic.service.logger.Logger()
matcher = SemanticMatcher(
    "sentence-transformers/all-mpnet-base-v2",
    external_get_timeout_sec=3,
    matching_strictness=0,
    fuzzer_weight=0.25,
    promote_filling_simple_fields=0.1)
matcher.start(logger=logger)

cards = conn.owned_cards()
for _card in tqdm(cards):
    card = conn.attach(_card["id"])
    local_card = aic.ModelCard()
    url = card.overview.home
    if not url: continue
    try:
        url = ollama_redirect(local_card, url, external_get_timeout_sec=matcher.external_get_timeout_sec, callback=None) or url
        url = huggingface_redirect(local_card, url, external_get_timeout_sec=matcher.external_get_timeout_sec) or url
        url = github_redirect(local_card, url, external_get_timeout_sec=matcher.external_get_timeout_sec) or url
        p = urlparse(url)
        if p.scheme not in ("http", "https") or not p.netloc: raise Exception("Invalid url format")
        r = requests.get(url, timeout=matcher.external_get_timeout_sec)
        r.raise_for_status()
    except Exception as e:
        logger.warn("Home page retrieval error "+str(p))
    url = r.url
    text = r.text
    if not urlparse(url).path.lower().endswith((".md", ".markdown")):
        text = trafilatura.extract(text, output_format="markdown", include_formatting=True, include_links=True)
    if not text: continue
    matcher.complete_from_markdown(local_card, url, text, ["", ""])

    card.assign(local_card)
    card.commit()
    logger.info("Updated card "+card.overview.name+" with id "+str(_card["id"]))
