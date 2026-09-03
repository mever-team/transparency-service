from .assistant import Assistant
from ..logger import Logger
from aicard.card import ModelCard
from aicard.agents import Agent
from aicard.service.jobs_tracker import CardJobsTracker, Job

from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests
import json
import markdown2
import time
from codecarbon import EmissionsTracker
from json_repair import repair_json

from ...agents.extensions.embeddings import ImageClassifier
from ...card.fields import LongText, Pattern
from ...utils.pdf_split import pdf_to_chunks
from ..converters import dynamic2dict



class Prompter(Assistant):
    def __init__(self,
                 agent: Agent,
                 image_classifier: ImageClassifier|None=None,
                 external_get_timeout_sec:int=3,
                 max_retries:int=3,
                 deep:bool=False,
                 description:str = None,
                 text_preprocessor = None):
        if not description:
            self.description = "<h1>"+agent.name()+("</h1>Slow but deep thinker, especially for refinement. "if not deep else "</h1>Thinks for a little bit. ")+agent.description()
        else:
            self.description = "<h1>" + agent.name() + "</h1>" + description + ' ' + agent.description()
        super().__init__(
            alias=agent.name()+("-deep" if deep else ""),
            description=self.description
        )
        self.agent = agent
        self.external_get_timeout_sec = external_get_timeout_sec
        self.max_retries = max_retries
        self.deep = deep
        self.image_classifier = image_classifier
        self.text_preprocessor = text_preprocessor

    def complete(self, card: ModelCard, card_id: int, data: dict, logger: Logger, user_messages: list[str], job_tracker: CardJobsTracker):
        if data['data_type'] == 'url':
            # url = data['url']
            # logger.info("Submitted: " + str(url), user=self.alias)
            # user_messages.clear()
            # user_messages.append(f"<h2>{self.alias} import</h2>Retrieving data")

            # parsed = urlparse(url)
            # if not parsed.scheme in ("http", "https") or not parsed.netloc: raise Exception("Invalid url format")
            # response = requests.get(url, timeout=self.external_get_timeout_sec)
            # text = response.text

            # soup = BeautifulSoup(text, "html.parser")
            # for tag in soup.find_all(href=True): tag["href"] = urljoin(url, tag["href"])
            # for tag in soup.find_all(src=True): tag["src"] = urljoin(url, tag["src"])

            # text = soup.get_text(strip=True)
            url = data['url']
            text = url
        elif data['data_type'] == '.pdf':
            pdf_bytes = data['bytes']
            text = pdf_to_chunks(pdf_bytes = pdf_bytes)
            
        self._complete(text, "completion", card, logger, user_messages)
        progress_html = (
            f"<progress value='{100}' max='100' "
            f"style='width: 300px; height: 20px; "
            f"accent-color: #79CFDC; border: 2px solid #1F1F1F;'></progress>"
        )
        user_messages[-1] = (
            f"<h2>{self.alias} import</h2>"
            f"{progress_html}<br>"
            f"<b>Importing images</b>"
        )
        if self.image_classifier and data['data_type'] == 'url':
            images = []
            img_tags = soup.find_all('img')
            for tag in img_tags:
                images.append(tag["src"])
                tag['style'] = 'max-height:600px; display:block; margin:0 auto;'
            results = self.image_classifier.classify_images(images)
            for i, (label, score) in enumerate(results):
                if label is None: continue
                (cat, field), = label.items()
                if cat not in card.data: continue
                card.data[cat][field].set(card.data[cat][field].get()+"<br><br>"+str(img_tags[i]))
        if not card.overview.home and data['data_type'] == 'url': card.overview.home = url
        user_messages[-1] = (
            f"<h2>{self.alias} import</h2>"
            f"Saving..."
        )

    def refine_field(self, text: str, logger: Logger):
        params = {}
        refined_stream = self.agent.simplificationStream(text, **params)
        return refined_stream
    
    def refine(self, card: ModelCard, card_id: int, logger: Logger, user_messages: list[str], job_tracker: CardJobsTracker):
        job = Job(
            worker = 'prompter',
            operation = 'refine',
            data={})
        job_tracker.set(card_id, job)
        job_id = job_tracker.get(card_id).id
        tracker = EmissionsTracker( project_name=job_id, save_to_file=False, log_level="WARNING", tracking_mode="process")
        tracker.start()
        for category, values in card.data.items():
            if not isinstance(values, dict): continue
            job.data[category] = {}
            for field, value in values.items():
                if not value.is_refinable: 
                    text = value.get()
                else:
                    text = ''
                    for chunks in self.refine_field(value.get(), logger):
                        chunks = json.loads(chunks)
                        text += chunks['message']['content']
                    card.data[category][field].set(text)
                job.data[category][field] = text
                job_tracker.update(card_id, job)
        emissions = tracker.stop()
        emissions_data = json.loads(tracker.final_emissions_data.toJSON())
        job_tracker.delete(card_id, emissions_data)
        
        
    def _complete(self, text: str|list[str], task: str, card: ModelCard, logger: Logger, user_messages: list[str]):
        user_messages[-1] = (
            "<h2>Importing Information</h2>"
            "An AI assistant is working on the model card<br>"
        )
        md_claude_schema = card.to_claude_schema()
        params = {"format":{"type": "json_schema", "schema": md_claude_schema}}
        answer = self.agent.completion(text, **params)
        new_md = repair_json(answer, return_objects=True)
        for categoty_name, fields in new_md.items():
            if not isinstance(fields, dict): continue
            for field_name, field_value in fields.items():
                if field_name not in card.data.get(categoty_name, {}): continue
                card.data[categoty_name][field_name].set(field_value)
        card.data['overview']['version'].set('')
        


def assist(agent):
    if isinstance(agent, Agent): return Prompter(agent)
    raise Exception("Invalid agent type to assist with: "+str(type(agent)))