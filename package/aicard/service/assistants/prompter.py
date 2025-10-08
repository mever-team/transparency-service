from .assistant import Assistant
from ..logger import Logger
from aicard.card import ModelCard
from aicard.agents import Agent
from urllib.parse import urlparse, urljoin
import requests
import json
import markdown2
from bs4 import BeautifulSoup
import time
import datetime


from ...card.fields import LongText


class Prompter(Assistant):
    def __init__(self,
                 agent: Agent,
                 external_get_timeout_sec=1):
        super().__init__(
            alias=agent.name(),
            description="<h1>"+agent.name()+"</h1>Slow thinker. Powered by the namesake LLM.")
        self.agent = agent
        self.external_get_timeout_sec = external_get_timeout_sec

    def complete(self, card: ModelCard, url: str, logger: Logger, user_messages: list[str]):
        logger.info("Submitted: " + str(url), user=self.alias)
        user_messages.clear()
        user_messages.append(f"<h2>{self.alias} import</h2>")

        parsed = urlparse(url)
        if not parsed.scheme in ("http", "https") or not parsed.netloc: raise Exception("Invalid url format")
        response = requests.get(url, timeout=self.external_get_timeout_sec)
        text = response.text

        soup = BeautifulSoup(text, "html.parser")
        for tag in soup.find_all(href=True): tag["href"] = urljoin(url, tag["href"])
        for tag in soup.find_all(src=True): tag["src"] = urljoin(url, tag["src"])
        text = soup.get_text(strip=True)

        output_formats = card.json_schema_per_category()
        # Extra parameterization
        output_formats['model']['required'] = ['name', 'overview','author', 'use_case']
        output_formats['considerations']['required'] = ['use_case']
        output_formats['model']['properties']['overview']['minLength'] = 500
        output_formats['considerations']['properties']['use_case']['minLength'] = 10
        for category, values in output_formats.items():
            if 'more' in values['properties']:
                values['properties'].pop('more')

        count_categories = 0
        for category, values in card.data.items():
            if not isinstance(values, dict): continue
            count_categories += 1

        progress = 0
        for category, values in card.data.items():
            if not isinstance(values, dict): continue

            progress_html = (
                f"<progress value='{int(progress / count_categories * 100)}' max='100' "
                f"style='width: 300px; height: 20px; "
                f"accent-color: #79CFDC; border: 2px solid #1F1F1F;'></progress>"
            )
            user_messages[-1] = (
                f"<h2>{self.alias} import</h2>"
                f"{progress_html}<br>"
                f"<b>Working on {category.replace('_', ' ')}</b>"
            )
            progress += 1

            prompt = f"Output in plain text, no braces, no quotes, no JSON. Provide information about: {text}"
            category_format = output_formats[category]
            params = {"format": category_format}

            # Ollama bug workaround: invalid json
            while True:
                completion = self.agent.completion(prompt, **params)
                # Ollama bug workaround: https://github.com/ollama/ollama/issues/1910
                time.sleep(1)
                try:
                    completion = json.loads(completion)
                    break
                except (json.JSONDecodeError, TypeError): logger.warn("agent.completion produced an invalid json. Requesting completion again")
            for field, value in values.items():
                if field not in completion: continue
                value.set(
                    f"<details>\n<summary><h2>{datetime.datetime.now().strftime("%Y %B %d, %I:%M%p")}</h2></summary>\n\n<div class=\"card-details-content\">\n{completion[field]}\n</div>\n</details>\n\n"
                    f"{value.get()}"
                )
        if not card.model.home: card.model.home = url
        user_messages[-1] = (
            f"<h2>{self.alias} refinement</h2>"
            f"Saving..."
        )

    def refine(self, card: ModelCard, logger: Logger, user_messages: list[str]):
        user_messages.clear()
        user_messages.append(f"<h2>{self.alias} refinement</h2>")
        count_categories = 0
        for category, values in card.data.items():
            if not isinstance(values, dict): continue
            for field, value in values.items():
                if not isinstance(value, LongText): continue
                if len(value.get().split(' '))<2: continue
                count_categories += 2
        progress = 0
        for category, values in card.data.items():
            if not isinstance(values, dict): continue
            for field, value in values.items():
                if not isinstance(value, LongText): continue
                value_text = value.get()
                if len(value_text.split(' '))<2: continue
                if ("<summary><h2>Simplified</h2></summary>" in value_text or
                    "<summary><h2>Original</h2></summary>" in value_text): continue

                def update_progress(progress):
                    progress_html = (
                        f"<progress value='{int(progress / count_categories * 100)}' max='100' "
                        f"style='width: 300px; height: 20px; "
                        f"accent-color: #79CFDC; border: 2px solid #1F1F1F;'></progress>"
                    )
                    user_messages[-1] = (
                        f"<h2>{self.alias} refinement</h2>"
                        f"{progress_html}<br>"
                        f"<b>Working on {category.replace('_', ' ')} {field.replace('_', ' ')}</b>"
                    )

                update_progress(progress)
                progress += 1
                summarization = self.agent.summarization(value_text)

                update_progress(progress)
                progress += 1
                simplification = self.agent.simplification(value_text)

                summarization = markdown2.markdown(summarization, extras=["markdown-in-html", "code-friendly"])
                simplification = markdown2.markdown(simplification, extras=["markdown-in-html", "code-friendly"])
                value.set(
                    f"{summarization}\n\n"
                    f"<details>\n<summary><h2>Simplified</h2></summary>\n\n<div class=\"card-details-content\">\n{simplification}\n</div>\n</details>\n\n"
                    f"<details>\n<summary><h2>Original</h2></summary>\n\n<div class=\"card-details-content\">\n{value_text}\n</div>\n</details>"
                )
        user_messages[-1] = (
            f"<h2>{self.alias} refinement</h2>"
            f"Saving..."
        )
        #card.assign(card.to_html_card()) # this creates some errors - under investigation

def assist(agent):
    if isinstance(agent, Agent): return Prompter(agent)
    raise Exception("Invalid agent type to assist with: "+str(type(agent)))