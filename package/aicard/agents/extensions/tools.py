import requests
from pathlib import Path
from aicard.agents.extensions.glossary.glossary import Glossary

class Tools:
    def __init__(self):
        self._model = "gpt-oss:120b-cloud"
        self._ollama_url = "http://localhost:11434/api/chat"
        self._tool_list = [
            {
                "type": "function",
                "function": {
                    "name": "explain_technical_term",
                    "description": (
                        "Return a simple explanation of a technical term for a non-AI expert."
                    ),
                    "parameters": {
                        "type": "object",
                        "required": ["term"],
                        "properties": {
                            "term": {
                                "type": "string",
                                "description": "The technical term to explain."
                            }
                        }
                    }
                }
            }
        ]
        self.__glossary = Glossary()

    ###########################
    #   Tools
    ###########################

    def explain_technical_term(self, term: str) -> str:
        """
        Return a simple explanation of a technical term
        """
        # Even though system  prompt contains the term, the agent might request a tool call
        # for it. Check if it exists in the glossary. If not, request Ollama
        entry = self.__glossary.find_glossary_entry(term)

        if entry is not None:
            return entry["explanation"]
        BASE_DIR = Path(__file__).resolve().parent
        with open(BASE_DIR / "glossary" / "missed.txt", "a") as f:
            f.write(f"{term}\n")
        # IMPORTANT: when we set up ollama cloud access, remove early return.
        return 'No explanation provided for this term.'

        prompt = f"""
    Explain the following technical term for a general audience.

    Term: {term}

    Rules:
    - Give a short explanation in 1-2 sentences.
    - Explain only the general meaning of the term.
    - Use simple, plain language.
    - Be accurate and neutral.
    - Do not assume anything about a specific model, system, dataset, or application.
    - Do not add benefits, advantages, performance claims, or other properties
    unless they are part of the basic definition of the term.
    - Do not invent information.
    - Avoid introducing other technical terms that require explanation.
    - Return ONLY the explanation.
    """

        payload = {
            "model": 'gpt-oss:120b-cloud',
            "stream": False,
            "messages": [{"role": "user", "content": prompt}
            ]
        }

        response = requests.post(
            "http://localhost:11434/api/chat",
            json=payload,
            timeout=60
        )
        response.raise_for_status()

        data = response.json()
        explanation = data["message"]["content"].strip()
        print('MISS :(')

        return explanation

