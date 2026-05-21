import aiod
import requests
import markdown2
import aicard as aic
from aicard.service.assistants import SemanticMatcher
from tqdm import tqdm

logger = aic.service.logger.Logger()
matcher = SemanticMatcher(
    "sentence-transformers/all-mpnet-base-v2",
    external_get_timeout_sec=3,
    matching_strictness=0)
matcher.start(logger=logger)
matcher._wait_until_ready()

def _md(text: str) -> str:
    if not text: return ""
    return markdown2.markdown(str(text), extras=["markdown-in-html", "code-friendly"])
def _str(val) -> str:
    if val is None: return ""
    if isinstance(val, list): return ", ".join(str(v) for v in val if v)
    return str(val)

def aiod_to_card(model, card: aic.ModelCard) -> None:
    url = _str(model.get("same_as"))
    card.data.overview.name    = _str(model.get("name"))
    card.data.overview.creator = _str(model.get("creator"))
    card.data.overview.version = _str(model.get("date_published"))
    card.data.overview.date    = _str(model.get("date_published"))
    card.data.overview.license = _str(model.get("license"))
    card.data.overview.home    = url
    card.data.overview.contact = _str(model.get("creator"))
    app_area = model.get("application_area")
    if app_area: card.data.overview.task = _str(app_area)

    use_parts = []
    if app_area: use_parts.append(f"Application area: {_str(app_area)}")
    sector = model.get("industrial_sector")
    if sector: use_parts.append(f"Industrial sector: {_str(sector)}")
    card.data.use.use_cases     = "\n".join(use_parts) or _str(app_area)
    card.data.use.factors        = _str(model.get("keyword"))

    description = ""
    try: description = model.get("description", {}).get("plain", "") or ""
    except Exception: pass
    matcher.complete_from_text(card, url, _md(description))

conn = aic.connect("http://127.0.0.1:5000", username="admin", password="admin")
card_names = {card["name"] for card in conn.status()["cards"]}
logger.info(f"bot has already registered {len(card_names)} cards")

models = aiod.ml_models.get_list(limit=1000, platform="ai4europe_cms")
missing_models = models[~models["name"].isin(card_names)]
logger.info(f"bot found {len(missing_models)} new cards to import")

for _, model in tqdm(missing_models.iterrows(), total=len(missing_models)):
    local_card = aic.ModelCard()
    aiod_to_card(model, local_card)
    quality = local_card.quality()
    if quality < 0.3:
        logger.warn(f"Not published '{model['name']}' due to low quality {quality:.3f}")
        continue
    with conn.create() as card: card.merge(local_card)