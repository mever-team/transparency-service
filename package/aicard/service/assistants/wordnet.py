import threading
import nltk
import sys
import re
import requests
from .assistant import Assistant
from aicard.card import ModelCard
from nltk.corpus import wordnet as wn
from aicard.service.logger import Logger
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from ...card.fields import Field, LongText, Options


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
    stop_words = set()

    def __init__(self,
                 external_get_timeout_sec: float=1,
                 max_chars_for_semantic_synonyms: int=1000):
        super().__init__(
            alias="📚 Text copying",
            description=(
                "<h1>📚 Text copying</h1>"
                "Fast and deterministic copy-paster. Imports text by using a semantic dictionary from WordNet to organize paragraphs by meaning, and refines text by adding explanatory tooltips."
            )
        )
        self.scientific_defs = None
        self.field_synonyms = dict()
        self.external_get_timeout_sec = external_get_timeout_sec
        self.max_chars_for_semantic_synonyms = max_chars_for_semantic_synonyms


    def start(self, logger: Logger):
        with WordNet._loader_lock:
            if WordNet._started: return
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
                stop_words.add("b")
                stop_words.add("div")
                stop_words.add("a")
                stop_words.add("href")
                stop_words.add("i")
                stop_words.add("span")
                stop_words.add("p")
                stop_words.add("br")
                stop_words.add("ul")
                stop_words.add("li")
                stop_words.add("abbr")
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
                    field_synonyms[cat] = get_synonyms(cat, stop_words)
                    for field, value in values.items():
                        if isinstance(value, Options):
                            for option in value.options():
                                field_synonyms[option] = set(option.lower().split())#get_synonyms(option.lower(), stop_words)
                        field_synonyms[field] = get_synonyms(field+" "+value.description.split("?")[0], stop_words)

                logger.ok(f"loading complete" 
                        f"\n * {len(scientific_defs)} terms"
                        f"\n * {int(total/1024)} kB"
                        f"\n * {len(stop_words)} stopwords"
                        f"\n * {len(field_synonyms)} card field synonym lists", user="📚 WordNet")
                with WordNet._loader_lock:
                    self.scientific_defs = scientific_defs
                    self.field_synonyms = field_synonyms
                    WordNet.stop_words = stop_words
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

    def complete(self, card: ModelCard, url: str, logger: Logger, user_messages: list[str]):
        user_messages[-1] = (
            f"<h2>{self.alias} import</h2>"
            f"Matching by dictionary definitions."
        )
        self._wait_until_ready()
        logger.info("Submitted: " + str(url), user=self.alias)
        parsed = urlparse(url)
        if not parsed.scheme in ("http", "https") or not parsed.netloc: raise Exception("Invalid url format")
        response = requests.get(url, timeout=self.external_get_timeout_sec)

        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup.find_all(href=True): tag["href"] = urljoin(url, tag["href"])
        for tag in soup.find_all(src=True): tag["src"] = urljoin(url, tag["src"])
        first_header = soup.find(re.compile("^h[1-6]$"))
        title = first_header.get_text(separator=" ", strip=True) if first_header else ""
        # sections = []
        # for header in soup.find_all(re.compile("^h[1-6]$")):
        #     content = []
        #     for sibling in header.find_next_siblings():
        #         if sibling.name and re.match("^h[1-6]$", sibling.name):
        #             break
        #         content.append(str(sibling))
        #     sections.append(content)
        sections = []
        last_header = ""
        for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "table", "img", "pre"]):
            if tag.name.startswith("h"):
                # Store latest header text
                last_header = tag.get_text(strip=True)
            else:
                # Preserve previous header + image
                context = last_header if last_header else ""
                full_info = (context + "\n" + str(tag)) if context else str(tag)
                sections.append((full_info, str(tag)))

        for tag in soup.find_all(["table", "img", "pre"]):
            tag.decompose()  # remove from document
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            text = a.get_text(strip=True)
            # Combine text and URL
            if text:
                replacement = f"[{text}]({href})"
            else:
                replacement = href
            a.replace_with(replacement)
        for para in [p.strip() for p in soup.get_text(separator="\n").strip().split("\n\n") if p.strip()]:
            para = re.sub(r'\[([^\]]+)\]\((https?://[^\)]+)\)', r'<a href="\2" target="_blank">\1</a>', para) #
            para = re.sub(r'\[([^\]]+)\]\((mailto?://[^\)]+)\)', r'<a href="\2" target="_blank">\1</a>', para) # markdown link to link
            para = para.replace(" ,", ",").replace(" .", ".")
            if len(para)>20 and para.endswith("."):
                sections.append((para, para))
            elif para.startswith("https://"):
                para = f'<a href={para} target="_blank">{para}</a>'
                sections.append((para, para))

        not_used_fields = list()
        has_been_replaced = dict()
        best_option_matches = dict()
        existing = set(cat+"__"+field for cat, values in card.data.items()
                       if isinstance(values, dict)
                       for field, value in values.items() if value.get() and value.get().lower()!="unknown")
        for heading, content in sections:
            content = content.strip()
            if not content.strip():
                continue
            if not content: continue
            synonyms = get_synonyms(heading, WordNet.stop_words)
            secondary_synonyms = get_synonyms(heading, WordNet.stop_words)
            for value in re.sub(r"[^A-Za-z]", " ", content[:min(self.max_chars_for_semantic_synonyms, len(content))]).split(" "):
                secondary_synonyms |= get_synonyms(value, WordNet.stop_words)
            best_score = 0
            best_path = []
            for cat, values in card.data.items():
                if not isinstance(values, dict): continue
                for field, value in values.items():
                    if isinstance(value, Options):
                        if cat+"__"+field in existing: continue
                        field_score = (len(synonyms & self.field_synonyms[field])
                                 + len(synonyms & self.field_synonyms[cat])*0.5
                                 + len(secondary_synonyms & self.field_synonyms[field])*0.2
                                 + len(secondary_synonyms & self.field_synonyms[cat])*0.2
                                 )
                        for option in value.options():
                            normalized_option = cat+"__"+field+"__"+option
                            score = field_score + len(synonyms & self.field_synonyms[option])
                            if score>=field_score+len(self.field_synonyms[option])/2+1 and score > best_option_matches.get(normalized_option, 0):
                                best_option_matches[normalized_option] = score
                                value.set(option)
                        continue
                    if not isinstance(value, LongText) and (len(content)>120 or ' ' in content.strip()): continue
                    #if cat+"__"+field in has_been_replaced: continue
                    score = (len(synonyms & self.field_synonyms[field])
                             + len(synonyms & self.field_synonyms[cat])*0.5
                             + len(secondary_synonyms & self.field_synonyms[field])*0.2
                             + len(secondary_synonyms & self.field_synonyms[cat])*0.2
                             ) / (len(self.field_synonyms[cat])+len(self.field_synonyms[field])+1)
                    if score > best_score:
                        best_score = score
                        best_path = (cat, field)
            if best_path and best_path[0]+"__"+best_path[1] not in existing:
                prev_content = has_been_replaced.get(best_path[0]+"__"+best_path[1], "")
                if prev_content and (not prev_content.endswith(".") or not content.endswith(".")): prev_content = prev_content+"<br>"
                if prev_content: content = prev_content +  " " + content
                has_been_replaced[best_path[0] + "__" + best_path[1]] = content
                card.data[best_path[0]][best_path[1]].set(content)
            else: not_used_fields.append(heading)

        if not card.overview.name: card.overview.name = title
        if not card.overview.home: card.overview.home = url
        user_messages[-1] = (
            f"<h2>{self.alias} import</h2>"
            f"Saving..."
        )

    def refine(self, card: ModelCard, logger: Logger, user_messages: list[str]):
        user_messages[-1] = (
            f"<h2>{self.alias} refinement</h2>"
            f"Searching dictionary for word definitions"
        )
        self._wait_until_ready()
        for cat, vals in card.data.items():
            if not isinstance(vals, dict): continue
            for field, value in vals.items():
                assert isinstance(value, Field)
                vals[field].set(self._refine_field(value.get()))
        card.assign(card.to_html_card())
        user_messages[-1] = (
            f"<h2>{self.alias} refinement</h2>"
            f"Matching by dictionary definitions"
        )
