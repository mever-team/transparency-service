import threading
import nltk
import sys
import re
import requests
from .assistant import Assistant
from aicard.card import ModelCard
from nltk.corpus import wordnet as wn
from aicard.service.logger import Logger
from urllib.parse import urlparse
from bs4 import BeautifulSoup

class WordNet(Assistant):
    _loader_thread: threading.Thread | None = None
    _loader_lock = threading.Lock()
    _started = False

    def __init__(self, external_get_timeout_sec=1):
        super().__init__(
            alias="📚 WordNet",
            description=(
                "<h1>📚 WordNet</h1>"
                "Highlights scientific terms from WordNet domain tags "
                "and adds tooltips with their definitions."
            )
        )
        self.scientific_defs = None
        self.external_get_timeout_sec = external_get_timeout_sec


    def start(self, logger: Logger):
        with WordNet._loader_lock:
            if WordNet._started:
                return
            WordNet._started = True
        def _load():
            try:
                logger.warn("loading datasets\n * will proceed asynchronously\n * may take a while the first time\n * agent tasks will wait on this", user="📚 WordNet")
                nltk.download("wordnet", quiet=True)
                nltk.download("omw-1.4", quiet=True)
                sci_lexnames = {
                    "noun.cognition", "noun.artifact", "noun.process",
                    "noun.substance", "noun.attribute",
                }
                from nltk.corpus import stopwords
                stop_words = set(stopwords.words("english"))
                scientific_defs = {}
                for syn in wn.all_synsets():
                    if syn.lexname() in sci_lexnames:
                        gloss = syn.definition()
                        for lemma in syn.lemmas():
                            word = lemma.name().replace("_", " ").lower()
                            if word in stop_words: continue
                            scientific_defs.setdefault(str(word), str(gloss))
                total = sys.getsizeof(scientific_defs)  # base dict structure
                for k, v in scientific_defs.items():
                    total += sys.getsizeof(k)
                    total += sys.getsizeof(v)
                logger.ok(f"loaded {len(scientific_defs)} terms in {int(total/1024)} kb", user="📚 WordNet")
                with WordNet._loader_lock:
                    self.scientific_defs = scientific_defs
            except Exception as e:
                logger.error(f"failed to start: {e}", user="📚 WordNet")
                self.scientific_defs = dict()

        WordNet._loader_thread = threading.Thread(target=_load, daemon=True)
        WordNet._loader_thread.start()

    def _wait_until_ready(self):
        with WordNet._loader_lock:
            if self.scientific_defs is None or len(self.scientific_defs)==0:
                raise Exception(self.alias+" failed to start or has not yet finished setting up")

    def _refine_field(self, value):
        toks = re.findall(r"[A-Za-z0-9_]+|[<>.,()\"']|\s+", value)
        bal = 0
        for t in toks:
            if t == "<": bal += 1
            elif t == ">":bal -= 1
            if bal < 0: raise Exception("Imbalanced <>")
        if bal: raise Exception("Imbalanced <>")
        out, i, inside = [], 0, False
        in_abbr = False
        while i < len(toks):
            t = toks[i]
            if t == "<": inside = True; out.append(t)
            elif t == ">": inside = False; out.append(t)
            elif inside and t=="abbr": out.append(t); in_abbr = not in_abbr
            elif inside or in_abbr or len(t)<=1 or t.isspace(): out.append(t)
            else:
                bi = f"{t} {toks[i+2]}" if i+2<len(toks) and len(toks[i+2])>1 and toks[i+1].isspace() else None
                if bi and bi in self.scientific_defs:
                    out.append(f"<abbr title='{self.scientific_defs[bi]}'>{bi}</abbr>");
                    i += 2
                elif t in self.scientific_defs: out.append(f"<abbr title='{self.scientific_defs[t]}'>{t}</abbr>")
                else: out.append(t)
            i += 1
        return "".join(out)

    def complete(self, card: ModelCard, url: str, logger: Logger):
        self._wait_until_ready()
        logger.info("Submitted: " + str(url), user=self.alias)
        parsed = urlparse(url)
        if not parsed.scheme in ("http", "https") or not parsed.netloc: raise Exception("Invalid url format")
        response = requests.get(url, timeout=self.external_get_timeout_sec)

        soup = BeautifulSoup(response.text, "html.parser")
        first_header = soup.find(re.compile("^h[1-6]$"))
        title = first_header.get_text(strip=True) if first_header else None
        sections = []
        for header in soup.find_all(re.compile("^h[1-6]$")):
            content = []
            for sibling in header.find_next_siblings():
                if sibling.name and re.match("^h[1-6]$", sibling.name):
                    break
                content.append(sibling.get_text(" ", strip=True))
            sections.append((header.get_text(strip=True), " ".join(content).strip()))

        card.model.name = title
        print("Title:", title)
        print("Sections:", [sec[0] for sec in sections])


    def refine(self, card: ModelCard, logger: Logger):
        self._wait_until_ready()
        for cat, vals in card.data.items():
            if not isinstance(vals, dict):
                continue
            for field, value in vals.items():
                if not isinstance(value, str):
                    continue
                vals[field] = self._refine_field(value)
        card.assign(card.to_html_card())
