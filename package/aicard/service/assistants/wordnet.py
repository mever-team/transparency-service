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

def get_synonyms(heading, stopwords):
    synonyms = set()
    for heading_part in heading.lower().replace("_", " ").strip().split(" "):
        if not heading_part: continue
        if heading_part in stopwords: continue
        synsets = wn.synsets(heading_part)
        synonyms |= {part for syn in synsets for lemma in syn.lemmas() for part in lemma.name().lower().replace("_"," ").split(" ")}
        synonyms |= {part for syn in synsets for lemma in syn.hypernyms() for part in lemma.name().lower().replace("_"," ").split(" ")}
        synonyms |= {part for syn in synsets for lemma in syn.hyponyms() for part in lemma.name().lower().replace("_"," ").split(" ")}
        synonyms |= {part for syn in synsets for lemma in syn.similar_tos() for part in lemma.name().lower().replace("_"," ").split(" ")}
        synonyms.add(heading_part)
    return synonyms

class WordNet(Assistant):
    _loader_thread: threading.Thread | None = None
    _loader_lock = threading.Lock()
    _started = False

    def __init__(self,
                 external_get_timeout_sec: float=1,
                 max_chars_for_semantic_synonyms: int=1000):
        super().__init__(
            alias="📚 WordNet",
            description=(
                "<h1>📚 WordNet</h1>"
                "Dictionary-based semantics. Runs fastly."
            )
        )
        self.scientific_defs = None
        self.field_synonyms = dict()
        self.external_get_timeout_sec = external_get_timeout_sec
        self.max_chars_for_semantic_synonyms = max_chars_for_semantic_synonyms


    def start(self, logger: Logger):
        with WordNet._loader_lock:
            if WordNet._started:
                return
            WordNet._started = True
        def _load():
            try:
                logger.warn("loading datasets\n * will proceed asynchronously\n * may take a while the first time\n * agent tasks will wait on this", user="📚 WordNet")
                nltk.download('stopwords', quiet=True)
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

                field_synonyms = dict()
                for cat, values in ModelCard().data.items():
                    if not isinstance(values, dict): continue
                    for field, value in values.items():
                        if not isinstance(value, str): continue
                        field_synonyms[field] = get_synonyms(field, stop_words)
                        field_synonyms[cat] = get_synonyms(cat, stop_words)

                logger.ok(f"loaded {len(scientific_defs)} terms in {int(total/1024)} kΒ", user="📚 WordNet")
                with WordNet._loader_lock:
                    self.scientific_defs = scientific_defs
                    self.field_synonyms = field_synonyms
                    self.stop_words = stop_words
            except Exception as e:
                logger.error(f"failed to start: {e}", user="📚 WordNet")
                self.scientific_defs = dict()

        WordNet._loader_thread = threading.Thread(target=_load, daemon=True)
        WordNet._loader_thread.start()

    def _wait_until_ready(self):
        with WordNet._loader_lock:
            if len(self.scientific_defs)==0:
                raise Exception("WordNet failed to start - please contact the server's administrator")
            if self.scientific_defs is None:
                raise Exception("WordNet is still starting")

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
                if sibling.name and re.match("^h[1-6]$", sibling.name): break
                #content.append(sibling.get_text(" ", strip=True))
                content.append(str(sibling))
            sections.append((header
                                .get_text(strip=True)
                                .encode("ascii", errors="ignore")
                                .decode(),
                             " ".join(content).strip()))
        not_used_fields = list()
        has_been_replaced = dict()
        for heading, content in sections:
            if not content.strip(): continue
            synonyms = get_synonyms(heading, self.stop_words)
            secondary_synonyms = get_synonyms(heading, self.stop_words)
            for value in re.sub(r"[^A-Za-z]", " ", content[:min(self.max_chars_for_semantic_synonyms, len(content))]).split(" "):
                secondary_synonyms |= get_synonyms(value, self.stop_words)
            best_score = 1
            best_path = []
            for cat, values in card.data.items():
                if not isinstance(values, dict): continue
                for field, value in values.items():
                    if not isinstance(value, str): continue
                    #if cat+"__"+field in has_been_replaced: continue
                    score = (len(synonyms & self.field_synonyms[field])
                             + len(synonyms & self.field_synonyms[cat])*0.5
                             + len(secondary_synonyms & self.field_synonyms[field])*0.2
                             + len(secondary_synonyms & self.field_synonyms[cat])*0.2
                             )
                    if score > best_score:
                        best_score = score
                        best_path = (cat, field)
            if best_path:
                prev_content = has_been_replaced.get(best_path[0]+"__"+best_path[1], "")
                if prev_content: content = prev_content +  "\n<br><br>\n" + content
                has_been_replaced[best_path[0] + "__" + best_path[1]] = content
                card.data[best_path[0]][best_path[1]] = content
            else: not_used_fields.append(heading)

        # fix name field, because it's kind of important
        card.model.overview = card.model.name + "<br>" + card.model.overview
        card.model.name = title
        if not_used_fields:
            logger.warn("the following headings could not be matched to a model card based on synonyms" + ", ".join(not_used_fields), user=self.alias)


    def refine(self, card: ModelCard, logger: Logger):
        self._wait_until_ready()
        for cat, vals in card.data.items():
            if not isinstance(vals, dict): continue
            for field, value in vals.items():
                if not isinstance(value, str): continue
                vals[field] = self._refine_field(value)
        card.assign(card.to_html_card())
