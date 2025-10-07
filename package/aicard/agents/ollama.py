import requests
import json
from aicard.agents.agent import Agent


class Ollama(Agent):
    tasks = {
        "completion": """You are a helpful assistant that provide information about an AI model based on a given text. 
        Output in plain text, no braces, no quotes, no JSON.""",# return as JSON.""",
        "hint": "You will be given text. Your goal is to provide explanation for all technical words so a non expert can understand its content. "
                "Your output should be a JSON where the keys will be the word to be explained and the values will be the explanation of this word.",
        "summarization" : """You are an AI specialized in simplifying and summarizing technical texts. You will be given html, markdown, or other text, and will produce a very short summary.
Instructions:
- Avoid technical jargon—instead, explain concepts in a way that an educated reader can understand without specialized knowledge.
- Maintain an academic tone—the text should still feel like it belongs in a research paper.
- Rephrase rather than omit—if a concept is difficult to explain simply, break it down into intuitive phrases.
- Use precise language—do not oversimplify to the point of losing meaning.
- Make sure that the output contains at most a few sentences and reads tersely.
- Make sure that the output is considerably shorter than the input.
- The output should be in pure text format, with no lists, line breaks, or paragraphs.
""",
        "simplification": """You are an AI specialized in simplifying technical texts while maintaining a professional, academic tone. 
Your goal is to rewrite technical content in a way that preserves all information but replaces complex terminology with clear, accessible language.
Instructions:
- Do not shorten the text—keep all details intact.
- Avoid technical jargon—instead, explain concepts in a way that an educated reader can understand without specialized knowledge.
- Maintain an academic tone—the text should still feel like it belongs in a research paper.
- Rephrase rather than omit—if a concept is difficult to explain simply, break it down into intuitive steps.
- Use precise language—do not oversimplify to the point of losing meaning. 
- Keep the same content length as the original."""
    }

    def __init__(self, model: str='mistral:latest', base_url: str="http://localhost:11434"):
        self._base_url = base_url
        self._url = f"{base_url}/api/chat"
        self._model = model
        test = requests.post(self._url, json={
            "model": model,
            "stream": False,
            "messages": [{"role": "user", "content": "Request test"}]
        })
        assert test.status_code == 200, f"Failed to initialize model '{model}'\nResponse: {test.text}"

    def _run(self, content: str, task: str, params: dict | None):
        assert isinstance(content, str), "Content must be of type str"
        assert task in Ollama.tasks, "Not supported task: "+task
        payload = {
            "model": self._model,
            "stream": False,
            "messages": [{"role": "system", "content": Ollama.tasks[task]}, {"role": "user", "content": content}]
        }
        if params:
            payload.update(params)
        response = requests.post(self._url, json=payload)
        response = json.loads(response.text)["message"]["content"]
        if response.startswith("Here"):
            idx_colon = response.find(':')
            idx_dot = response.find('.')
            indices = [i for i in (idx_colon, idx_dot) if i != -1]
            if indices:
                response = response[min(indices) + 1:].strip()
        return response