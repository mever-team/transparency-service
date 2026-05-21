import threading
import re
import torch
import json
import requests
import numpy as np
from .assistant import Assistant
from aicard.card import ModelCard
from aicard.service.logger import Logger
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup, NavigableString, Comment
from ...card.fields import Field, LongText, Options
from datetime import date
from transformers import AutoTokenizer, AutoModel
from codecarbon import EmissionsTracker
from aicard.service.jobs_tracker import CardJobsTracker, Job



class SemanticMatcher(Assistant):
    _loader_thread: threading.Thread | None = None
    _loader_lock = threading.Lock()
    _started = False

    def get_embeddings(self, text: str):
        with SemanticMatcher._loader_lock:
            if self.field_embeddings is None:
                raise Exception("Semantic Matcher is still starting")
            return self._get_embeddings(text) # within the lock so that we can compute one embedding at a time

    def _get_embeddings(self, text: str):
        def mean_pooling(model_output, attention_mask):
            token_embeddings = model_output.last_hidden_state
            mask = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
            return (token_embeddings * mask).sum(1) / mask.sum(1)

        encoded = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            return_tensors="pt"
        )

        with torch.no_grad():
            model_output = self.model(**encoded)
        token_embeddings = model_output.last_hidden_state
        input_mask_expanded = encoded["attention_mask"].unsqueeze(-1).expand(token_embeddings.size()).float()
        embeddings = torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
        return embeddings[0]

    def embedding_similarity(self, e1, e2) -> float:
        return float((e1*e2).sum())

    def __init__(self,
                 model_name: str="BAAI/bge-small-en-v1.5", #"BAAI/bge-m3",
                 external_get_timeout_sec: float=1,
                 matching_strictness: float=1,
                 max_special_character_density: float=0.05):
        super().__init__(
            alias="📚 Semantic organizer",
            description=(
                "<h1>📚 Semantic organizer</h1>"
                f"Fast and deterministic copy-paster powered by {model_name}. Re-organizes imported text by using semantic analysis of sentences, and refines text by adding explanatory tooltips."
            )
        )
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.field_embeddings = None
        self.average_field_embeddings = 0
        self.max_noise_similarity = 0
        self.max_special_character_density = max_special_character_density
        self.external_get_timeout_sec = external_get_timeout_sec
        self.matching_strictness = matching_strictness


    def start(self, logger: Logger):
        with SemanticMatcher._loader_lock:
            if SemanticMatcher._started: return
            SemanticMatcher._started = True
        def _load():
            try:
                with SemanticMatcher._loader_lock:
                    logger.warn("preparing semantic matcher\n * will proceed asynchronously\n * may take a while the first time\n * agent tasks will wait on this", user="📚 Semantic Matcher")
                    device = "cpu"# "cuda" if torch.cuda.is_available() else "cpu"
                    self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                    self.model = AutoModel.from_pretrained(self.model_name).to(device)
                    logger.ok(f"Loaded {self.model_name} on torch device: {device}", user="📚 Semantic Matcher")
                    self.model.eval()
                    field_embeddings = dict()
                    for cat, values in ModelCard().data.items():
                        if not isinstance(values, dict): continue
                        field_embeddings[cat] = self._get_embeddings("AI model card "+cat)
                        for field, value in values.items():
                            if isinstance(value, Options):
                                for option in value.options():
                                    field_embeddings[cat+"__"+field+"__"+option] = self._get_embeddings("question: # AI model card "+cat+" "+field+" "+option+"\n"+value.description)
                            field_embeddings[cat+"__"+field] = self._get_embeddings("question: # AI model card "+cat+" "+field+"\n"+value.description)
                    vals = list(field_embeddings.values())
                    sims = [self.embedding_similarity(vals[s1], vals[s2]) for s1 in range(len(vals)) for s2 in range(s1+1, len(vals))]
                    max_noise_similarity = min(sims)
                    logger.ok(f"loading complete" 
                            f"\n * {len(field_embeddings)} card field semantic embeddings"
                            f"\n * {max_noise_similarity:.3f} minimum matching (semantic similarity lesser than this is considered irrelevant)", user="📚 Semantic Matcher")

                    self.field_embeddings = field_embeddings
                    self.max_noise_similarity = max_noise_similarity
            except Exception as e:
                logger.error(f"failed to start: {e}", user="📚 Semantic Matcher")
                self.field_embeddings = dict()

        SemanticMatcher._loader_thread = threading.Thread(target=_load, daemon=True)
        SemanticMatcher._loader_thread.start()

    def _wait_until_ready(self):
        with SemanticMatcher._loader_lock:
            if self.field_embeddings is None:
                raise Exception("Semantic Matcher is still starting")

    def complete_from_text(self, card: ModelCard, url:str, text:str, user_messages=["dummy message list"]):
        soup = BeautifulSoup(text, "html.parser")
        for comment in soup.findAll(string=lambda text: isinstance(text, Comment)): comment.extract() # remove comments
        for tag in soup.find_all(href=True): tag["href"] = urljoin(url, tag["href"])
        for tag in soup.find_all(src=True): tag["src"] = urljoin(url, tag["src"])
        first_header = soup.find(re.compile("^h[1-6]$"))
        creator = ""
        title = ""
        if first_header: title = next((child.strip() for child in first_header.children if isinstance(child, NavigableString) and child.strip()), "")
        if not title: title = first_header.get_text(separator=" ", strip=True) if first_header else ""
        if "/" in title:
            title = title.split("/")
            creator = title[0].strip()
            title = title[1].strip()
        if " " in title and "-" in title:
            title_parts = title.split(" ")
            if title_parts[0].strip() and "-" in title_parts[0]:
                title = title_parts[0]
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
            if tag.name.startswith("h"): last_header = tag.get_text(strip=True)
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
            replacement = f"[{text}]({href})" if text else href
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
        existing = set(
            cat+"__"+field for cat, values in card.data.items()
           if isinstance(values, dict)
           for field, value in values.items() if value.get() and value.get().lower()!="unknown")
        count_sections = 0
        for heading, content in sections:
            content = content.strip()
            if not content: continue
            count_sections += 1
        progress = 0
        for heading, content in sections:
            content = content.strip()
            if not content: continue
            progress_html = (
                f"<progress value='{int(progress / count_sections * 100)}' max='100' "
                f"style='width: 300px; height: 20px; "
                f"accent-color: #79CFDC; border: 2px solid #1F1F1F;'></progress>"
            )
            user_messages[-1] = (
                f"<h2>{self.alias} import</h2>"
                f"{progress_html}<br>"
                f"<b>Organizing information.</b>"
            )
            progress += 1
            with SemanticMatcher._loader_lock: # TODO: more advanced scheduling in the future
                embedding = self._get_embeddings("passage: #"+(heading if heading else "")+"\n"+(content if content else ""))
            best_path = []
            # find where to place new content:
            # - short-circuit option selection
            # - place short content in short fields only
            # - place technical content only when on LongText.technical_nature (also that content cannot have the textual-derived threshold)
            is_technical = "<pre>" in content or "<math" in content or "<table" in content or "<image" in content or "<li" in content
            special_character_density = sum(1 for c in content if c in "_{}.,+/*^%#$=-0123456789")/len(content)
            if ("_" in content or "{" in content) and not is_technical: continue
            if not is_technical and special_character_density>self.max_special_character_density: continue
            best_score = 0 if is_technical else self.max_noise_similarity*self.matching_strictness
            for cat, values in card.data.items():
                if not isinstance(values, dict): continue
                for field, value in values.items():
                    if isinstance(value, Options):
                        if cat+"__"+field in existing: continue
                        for option in value.options():
                            normalized_option = cat+"__"+field+"__"+option
                            score = self.embedding_similarity(embedding, self.field_embeddings[normalized_option])
                            if score > best_option_matches.get(normalized_option, 0):
                                best_option_matches[normalized_option] = score
                                value.set(option)
                        continue
                    if not isinstance(value, LongText) and (len(content)>120 or ' ' in content.strip()): continue
                    if isinstance(value, LongText) and is_technical and not value.technical_nature: continue
                    idx = cat+"__"+field
                    score = self.embedding_similarity(embedding, self.field_embeddings[idx])
                    if score > best_score:
                        best_score = score
                        best_path = (cat, field)
            # actually place the new content (some minor formatting for paragraphs too)
            if best_path and best_path[0]+"__"+best_path[1] not in existing:
                prev_content = has_been_replaced.get(best_path[0]+"__"+best_path[1], "")
                if prev_content and (not prev_content.endswith(".") or not content.endswith(".")): prev_content = prev_content+"<br>"
                if prev_content: content = prev_content +  " " + content
                has_been_replaced[best_path[0] + "__" + best_path[1]] = content
                card.data[best_path[0]][best_path[1]].set(content)
            else: not_used_fields.append(heading)
        if not card.overview.name: card.overview.name = title
        if not card.overview.creator: card.overview.creator = creator
        if not card.overview.date: card.overview.date = date.today().strftime("%Y-%m-%d")
        if not card.overview.home: card.overview.home = url

    def complete(self, card: ModelCard, card_id: int, data: dict, logger: Logger, user_messages: list[str], job_tracker: CardJobsTracker):
        user_messages[-1] = (
            f"<h2>{self.alias} import</h2>"
            f"Retrieving document."
        )
        self._wait_until_ready()
        job = Job(
            worker = 'matcher',
            operation = 'complete',
            data={})
        job_tracker.set(card_id, job)
        job_id = job_tracker.get(card_id).id
        tracker = EmissionsTracker( project_name=job_id, save_to_file=False, log_level="WARNING", tracking_mode="process")
        tracker.start()
        
        url = data['url']
        logger.info("Submitted: " + str(url), user=self.alias)
        parsed = urlparse(url)
        if not parsed.scheme in ("http", "https") or not parsed.netloc: raise Exception("Invalid url format")
        response = requests.get(url, timeout=self.external_get_timeout_sec)
        self.complete_from_text(card, url, response.text)
        user_messages[-1] =  f"<h2>{self.alias} import</h2> Saving..."
        emissions = tracker.stop()
        emissions_data = json.loads(tracker.final_emissions_data.toJSON())
        job_tracker.delete(card_id, emissions_data)

    def refine(self, card: ModelCard, logger: Logger, user_messages: list[str]):
        raise Exception("Semantic matcher cannot perform refinement - consider combining it with an LLM")
