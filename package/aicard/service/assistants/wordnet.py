import threading
import time

from .assistant import Assistant
from aicard.card import ModelCard
from nltk.corpus import wordnet as wn
import nltk
import sys
from aicard.service.logger import Logger

class WordNet(Assistant):
    _loader_thread: threading.Thread | None = None
    _loader_lock = threading.Lock()
    _started = False

    def __init__(self):
        super().__init__(
            alias="📚 WordNet",
            description=(
                "<h1>📚 WordNet</h1>"
                "Highlights scientific terms from WordNet domain tags "
                "and adds tooltips with their definitions."
            )
        )
        self.scientific_defs = None

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
                scientific_defs = {}
                for syn in wn.all_synsets():
                    if syn.lexname() in sci_lexnames:
                        gloss = syn.definition()
                        for lemma in syn.lemmas():
                            word = lemma.name().replace("_", " ").lower()
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
        for _ in range(2): # wait for 2 & 5 = 1 sec at most
            with WordNet._loader_lock:
                if self.scientific_defs is not None: return
            time.sleep(0.5)
        with WordNet._loader_lock:
            if self.scientific_defs is None or len(self.scientific_defs)==0:
                raise Exception("Wordnet failed to start")


    def complete(self, card: ModelCard, url: str, logger: Logger):
        self._wait_until_ready()

    def refine(self, card: ModelCard, logger: Logger):
        self._wait_until_ready()
        for cat, vals in card.data.items():
            if not isinstance(vals, dict):
                continue
            for field, value in vals.items():
                if not isinstance(value, str):
                    continue
                for def_name, def_value in self.scientific_defs.items():
                    value = value.replace(def_name, f"{def_name} ({def_value})")
                vals[field] = value
        print(card.to_markdown())
        card.assign(card.to_html_card())
