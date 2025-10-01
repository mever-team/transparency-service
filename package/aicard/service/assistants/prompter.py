from .assistant import Assistant
from ..logger import Logger
from aicard.card import ModelCard
from aicard.agents import Agent
from urllib.parse import urlparse
import requests
import json
import markdown2
from bs4 import BeautifulSoup


class Prompter(Assistant):
    def __init__(self,
                 agent: Agent,
                 external_get_timeout_sec=1):
        super().__init__(
            alias="🤖 "+agent.__class__.__name__,
            description="<h1>🤖 "+agent.__class__.__name__+"</h1>Powered by the namesake LLM.")
        self.agent = agent
        self.external_get_timeout_sec = external_get_timeout_sec

    def complete(self, card: ModelCard, url: str, logger: Logger):
        logger.info("Submitted: " + str(url), user=self.alias)
        parsed = urlparse(url)
        if not parsed.scheme in ("http", "https") or not parsed.netloc: raise Exception("Invalid url format")
        response = requests.get(url, timeout=self.external_get_timeout_sec)
        text = response.text

        last_output = card.json_dumps()
        prompt = f"{last_output}\n\n{text}"
        completion = self.agent.completion(prompt)

        start = completion.find("{")
        brace_count = 0
        for i, ch in enumerate(completion[start:], start=start):
            if ch == "{":
                brace_count += 1
            elif ch == "}":
                brace_count -= 1
                if brace_count == 0:
                    striped_json = json.loads(completion[start:i + 1])

        for category, values in card.data.items():
            if category not in striped_json: continue
            if not isinstance(values, dict): continue
            for field, value in values.items():
                if field not in striped_json[category]: continue
                if not isinstance(value, str): continue
                values[field] = striped_json[category][field]

    def refine(self, card: ModelCard, logger: Logger):
        print(f'def refine(self, card: ModelCard, logger: Logger):{self.agent.__class__.__name__}')
        for category, values in card.data.items():
            if not isinstance(values, dict): continue
            for field, value in values.items():
                if not isinstance(value, str): continue
                if len(value.split(' '))<2: continue
                if ("<summary><h2>Simplified</h2></summary>" in value or
                    "<summary><h2>Original</h2></summary>" in value): continue
                summarization = self.agent.summarization(value)
                simplification = self.agent.simplification(value)
                summarization = markdown2.markdown(summarization, extras=["markdown-in-html", "code-friendly"])
                simplification = markdown2.markdown(simplification, extras=["markdown-in-html", "code-friendly"])
                values[field] = (
                    f"{summarization}\n\n"
                    f"<details>\n<summary><h2>Simplified</h2></summary>\n\n<div class=\"card-details-content\">\n{simplification}\n</div>\n</details>\n\n"
                    f"<details>\n<summary><h2>Original</h2></summary>\n\n<div class=\"card-details-content\">\n{value}\n</div>\n</details>"
                )
        #card.assign(card.to_html_card()) # this creates some errors - under investigation

def assist(agent):
    if isinstance(agent, Agent): return Prompter(agent)
    raise Exception("Invalid agent type to assist with: "+str(type(agent)))