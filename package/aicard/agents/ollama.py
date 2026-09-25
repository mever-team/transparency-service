import requests
import os
import json
from aicard.agents.agent import Agent
from aicard.utils.image_converters import to_base64
from flask import Response


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
        "simplification": """
Your task is to rewrite the original text so that it is easier to understand
for non-AI experts.

Preserve the original meaning, information, and claims.

### Rules

1. Preserve information

- Preserve every factual claim, technical concept, attribute, component,
  relationship, and explicitly stated qualification from the original.
- Do not omit, weaken, replace, contradict, or remove information.
- Preserve the original grammatical person and level of certainty.
- Preserve explicit qualitative claims such as "state-of-the-art".
- Do not add information that is not stated or reasonably implied.

2. Explain technical concepts

- Keep important technical terms in the rewrite.
- Add short, simple explanations for technical or uncommon terms when needed
  for a non-AI expert to understand the text.
- Explanations should describe the general meaning of the term.
- Do not infer model-specific behavior from the technical term alone.
- Do not add benefits, advantages, performance claims, capabilities,
  purposes, or other properties unless supported by the original text.
- An explanation may make the rewrite longer.

3. Use the provided glossary explanations

Some technical terms from the original text have already been identified
automatically. Their explanations are provided below.

{glossary_context}

Use these explanations when explaining the corresponding terms.
Do not replace the original term with its explanation.

4. Use the technical-term explanation tool when necessary

You also have access to:

explain_technical_term(term)

The tool provides a short, general explanation of a technical term.

After examining the original text, identify any technical or uncommon terms
that are not already explained by the provided glossary context.

For EVERY such term that may be unfamiliar to a non-AI expert, you MUST call
explain_technical_term before writing the final answer.

Do not rely on your own knowledge to explain such a term when the tool can
provide an explanation.

Call the tool separately for each term.

If the tool provides no explanation, keep the original term but do not invent
a definition.

Do not call the tool for ordinary words or concepts that a non-AI expert
would reasonably understand.

5. Avoid unsupported claims

- Do not add subjective, evaluative, or qualitative adjectives or adverbs
  that are not supported by the original.
- Do not add claims about performance, quality, effectiveness, efficiency,
  benefits, advantages, capabilities, or complexity unless supported by
  the original.
- Do not add purposes or intended outcomes unless supported by the original.
- Do not add comparisons unless they appear in the original.
- Technical explanations must remain general and neutral.

6. Preserve original claims

Explanations must supplement the original claim, not replace it.

For example:

Original:
"Whisper is a state-of-the-art speech recognition model."

Correct:
"Whisper is a state-of-the-art speech recognition model, meaning it
represents a leading level of performance in speech recognition."

The explanation does not replace the original claim.

### Final verification

Before returning the answer, verify that:

1. Every original factual claim is preserved.
2. Every important technical concept is preserved.
3. Explicit attributes and qualifications are preserved.
4. Unfamiliar technical terms are explained.
5. Tool explanations are used accurately.
6. No unsupported claims or qualifiers were added.
7. No unsupported adjective or adverb was added.
8. No unsupported purpose, benefit, comparison, or evaluation was added.
9. No original claim was weakened, removed, or replaced.

Return ONLY the final rewritten text.
""",
        "vision": "Provide explanation about the image."
    }
    def name(self):
        return self._name

    def description(self):
        return self._description

    def __init__(
            self,
            model: str='mistral:latest',
            vision_model: str='gemma3:4b',
            base_url: str=os.getenv("OLLAMA_BASE_URL","http://localhost:11434"),
            name=None,
            description="Powered by Ollama.",
            timeout_secs=40
        ):  # pragma: no cover
        if name is None:
            name = "🦙 "+model.split(":")[0]
        self._description = description
        self._name = name
        self._base_url = base_url
        self._url = f"{base_url}/api/chat"
        self._model = model
        self._vision_model = vision_model
        self.timeout_secs = timeout_secs
        test = requests.post(self._url, json={
            "model": model,
            "stream": False,
            "messages": [{"role": "user", "content": "Request test"}],
        })
        assert test.status_code == 200, f"Failed to initialize model '{model}'\nResponse: {test.text}"

    def abort(self): # pragma: no cover
        """
        Abort the running Ollama model process.
        This function kills the process associated with the loaded model.
        It supports Linux, macOS, and Windows.
        """
        try: os.system(f'ollama stop {self._model}')
        except Exception as e: raise Exception(f"Failed to abort model {self._model}: {e}")

    def _run(self, content: str, task: str, **params):  # pragma: no cover
        assert isinstance(content, str), "Content must be of type str"
        assert task in Ollama.tasks, "Not supported task: "+task
        if not content:
            yield '{"message": {"content": ""}}\n'
            return
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
        response = requests.post(self._url, json=payload, timeout=self.timeout_secs)
        response = json.loads(response.text)["message"]["content"]
        if response.startswith("Here"):
            idx_colon = response.find(':')
            idx_dot = response.find('.')
            indices = [i for i in (idx_colon, idx_dot) if i != -1]
            if indices:
                response = response[min(indices) + 1:].strip()
        return response
    
    def _run_stream(self, content: str, task: str, **params):
        assert isinstance(content, str), "Content must be of type str"
        assert task in Ollama.tasks, "Not supported task: " + task

        if not content:
            yield '{"message": {"content": ""}}\n'
            return

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "explain_technical_term",
                    "description": (
                        "Return a simple explanation of a technical term "
                        "for a non-AI expert."
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

        prompt = Ollama.tasks[task]
        if task == 'simplification':
            glossary_context = build_glossary_context(content)
            print('added', glossary_context)
            prompt = Ollama.tasks[task].format(glossary_context=glossary_context)
            
        messages = [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": content
            }
        ]

        payload_params = dict(params)
        payload_params.pop("messages", None)
        payload_params.pop("tools", None)
        payload_params.pop("stream", None)
        tool_calls_count = 0
        while True:
            payload = {
                "model": self._model,
                "stream": True,
                "messages": messages,
                "tools": tools,
                **payload_params
            }

            tool_calls = []
            assistant_content = ""

            with requests.post(self._url, json=payload, stream=True) as r:
                r.raise_for_status()

                for line in r.iter_lines():
                    if not line:
                        continue
                    data = json.loads(line)
                    message = data.get("message", {})

                    # Accumulate normal streamed content
                    if message.get("content"):
                        assistant_content += message["content"]
                        yield json.dumps(data) + "\n"

                    # Accumulate streamed tool calls
                    if message.get("tool_calls"):
                        tool_calls.extend(message["tool_calls"])

            # No tool call -> model has finished
            if not tool_calls:
                break

            # Add the complete assistant message containing the tool calls
            messages.append({
                "role": "assistant",
                "content": assistant_content,
                "tool_calls": tool_calls
            })

            print(tool_calls)
            # Execute each requested tool
            for tool_call in tool_calls:
                function = tool_call.get("function", {})
                name = function.get("name")
                arguments = function.get("arguments", {})

                if name == "explain_technical_term":
                    tool_calls_count += 1
                    term = arguments.get("term", "")
                    result = explain_technical_term(term)
                    print(f"Tool calls: {tool_calls_count}")
                else:
                    result = f"Unknown tool: {name}"

                # Give the tool result back to Ollama
                messages.append({
                    "role": "tool",
                    "tool_name": name,
                    "content": result
                })
            
            

JUDGE_MODEL = "gpt-oss:120b-cloud"
OLLAMA_URL = "http://localhost:11434/api/chat"

def _normalize_term(term: str) -> str:
    """Normalize a term for glossary lookup."""
    return " ".join(term.lower().strip().replace("-", " ").split())


def explain_technical_term(term: str) -> str:
    """
    Return a simple explanation of a technical term
    """
    
    entry = find_glossary_entry(term)

    if entry is not None:
        print('HIT!!!!')
        return entry["explanation"]

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
        "model": JUDGE_MODEL,
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=60
    )
    response.raise_for_status()

    data = response.json()
    explanation = data["message"]["content"].strip()
    print('MISS :(')

    return explanation

import re
from pathlib import Path

glossary_path = Path(__file__).resolve().parent / "glossary.json"
with Path(glossary_path).open("r", encoding="utf-8") as f:
    glossary = json.load(f)
def find_glossary_entry(term: str) -> dict | None:
    for entry in glossary.values():
        for match_term in entry["match_terms"]:
            if term_matches_text(match_term, term):
                return entry
    return None
def find_glossary_terms(text: str) -> list[dict]:
    matches = []
    for entry in glossary.values():
        for term in entry["match_terms"]:
            if term_matches_text(term, text):
                matches.append(entry)
                break
    return matches

def build_glossary_context(text: str) -> str:
    entries = find_glossary_terms(text)
    if not entries:
        return ""
    lines = [
        "The following technical terms were found in the original text.",
        "Use these explanations when making the text understandable.",
        "",
    ]
    for entry in entries:
        lines.append(
            f"- {entry['term']}: {entry['explanation']}"
        )
    return "\n".join(lines)


from nltk.stem import SnowballStemmer


stemmer = SnowballStemmer("english")


def normalize_tokens(text: str) -> list[str]:
    text = text.lower()

    text = text.replace("-", " ")
    text = text.replace("_", " ")

    # Keep only words and numbers.
    tokens = re.findall(r"\b\w+\b", text)

    return [
        stemmer.stem(token)
        for token in tokens
    ]
    
def term_matches_text(term: str, text: str) -> bool:
    term_tokens = normalize_tokens(term)
    text_tokens = normalize_tokens(text)

    if not term_tokens:
        return False

    term_length = len(term_tokens)

    for i in range(
        len(text_tokens) - term_length + 1
    ):
        window = text_tokens[
            i:i + term_length
        ]

        if window == term_tokens:
            return True

    return False