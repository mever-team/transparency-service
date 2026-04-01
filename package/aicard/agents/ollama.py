from dotenv import dotenv_values
import requests
import os
import json
from typing import Optional
from aicard.agents.agent import Agent
from aicard.utils.image_converters import to_base64


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
        "simplification": """Your task:

- Rewrite the text under each header to make it easier to understand
- Improve clarity and explain ideas more explicitly, without changing the meaning
- Keep the EXACT same Markdown structure

Rules:

- Keep all headers (#) exactly as they are (same number, same order)
- Do NOT merge or remove sections
- Do NOT add new sections
- Do NOT introduce new information that is not implied by the original text
- Do NOT remove or omit any information
- Use simple, natural language
- Prefer slightly longer explanations only when they improve understanding
- Use natural language
- When a concept is complex, briefly explain it in simple terms
- When using technical or uncommon words, add a short explanation in parentheses
- Preserve the original meaning
- The result should be understandable by a 12-year-old

Output:

- Return ONLY the final Markdown
- Do NOT include any extra text before or after
""",
        "vision": "Provide explanation about the image."
    }
    def name(self):
        return self._name

    def description(self):
        return self._description

    def __init__(
            self,
            model: str,
            vision_model: str='gemma3:4b',
            base_url: str=os.getenv("OLLAMA_BASE_URL","http://localhost:11434"),
            env: Optional[str] = None,
            name=None,
            description="Powered by Ollama.",
            timeout_secs=40
        ):
        config = dotenv_values(env) if env else {}
        if name is None:
            name = "🦙 "+model.split(":")[0]
        self._description = description
        self._name = name
        self._base_url = base_url
        self.OLLAMA_API_KEY = config.get("OLLAMA_API_KEY", '')
        self._url = f"{base_url}/api/chat"
        self._model = model
        self._vision_model = vision_model
        self.timeout_secs = timeout_secs
        test = requests.post(self._url, json={
            "model": model,
            "stream": False,
            "messages": [{"role": "user", "content": "Request test"}],
            },
            headers={"Authorization": "Bearer " + self.OLLAMA_API_KEY},
        )
        assert test.status_code == 200, f"Failed to initialize model '{model}'\nResponse: {test.text}"

    def abort(self):
        """
        Abort the running Ollama model process.
        This function kills the process associated with the loaded model.
        It supports Linux, macOS, and Windows.
        """
        try: os.system(f'ollama stop {self._model}')
        except Exception as e: raise Exception(f"Failed to abort model {self._model}: {e}")

    def _run(self, content: str, task: str, **params):
        assert isinstance(content, str), "Content must be of type str"
        assert task in Ollama.tasks, "Not supported task: "+task
        if task == "vision":
            content, status = to_base64(content)
            if status != 200:
                return  content
            payload = {
                "model": self._vision_model,
                "stream": False,
                "messages": [{"role": "user", "content": Ollama.tasks[task], "images": [content]}]
            }
        else:
            payload = {
                "model": self._model,
                "stream": False,
                "messages": [{"role": "system", "content": Ollama.tasks[task]}, {"role": "user", "content": content}]
            }
        if params:
            payload.update(params)
        response = requests.post(
            self._url, 
            json=payload, 
            headers={"Authorization": "Bearer " + self.OLLAMA_API_KEY},)
            # timeout=self.timeout_secs)
        response = json.loads(response.text)["message"]["content"]
        if response.startswith("Here"):
            idx_colon = response.find(':')
            idx_dot = response.find('.')
            indices = [i for i in (idx_colon, idx_dot) if i != -1]
            if indices:
                response = response[min(indices) + 1:].strip()
        return response

class OllamaCloud(Ollama):
       def __init__(
            self,
            model: str, # nemotron-3-nano:30b qwen3-next:80b gemma3:27b qwen3.5:397b 
            vision_model: str='gemma3:4b',
            base_url: str="https://ollama.com",
            env: Optional[str] = None,
            name=None,
            description="Powered by Ollama.",
            timeout_secs=40
        ):
           super().__init__(
                model = model,
                vision_model= vision_model,
                base_url = base_url,
                env = env,
                name = name,
                description = description,
                timeout_secs = timeout_secs
            )