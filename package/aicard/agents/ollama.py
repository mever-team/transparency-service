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
        "simplification": """Your task:

* Rewrite the text to make it easier to understand for non-AI experts.
* Improve clarity and explain ideas more explicitly, without changing the original meaning.

### Rules

#### Preserve the original information

* Preserve every factual claim, technical concept, attribute, and component from the original text.
* Do NOT remove, omit, weaken, or replace information from the original text.
* Preserve the original grammatical person (first, second, or third person).
* Preserve the original level of certainty.
* If the original text explicitly states a qualitative attribute, preserve it. For example, if the original says "state-of-the-art," do not remove it or replace it with a weaker term such as "advanced."
* Do NOT introduce information that is not stated or reasonably implied by the original text.

#### Make technical concepts understandable

* Use simple, natural language suitable for non-AI experts.
* When the original text contains a technical or uncommon concept, explain it briefly in simple language when this improves understanding.
* Do NOT omit a technical concept merely because explaining it requires additional words.
* Distinguish between explaining the meaning of an existing concept and introducing a new claim about the specific model.
* Accurate, neutral definitions of technical concepts are allowed and encouraged.
* When appropriate, explain both what a technical component is and what it does.
* When using technical or uncommon words, add a short explanation in parentheses or in the surrounding sentence.
* Prefer slightly longer explanations when they are necessary to make an existing concept understandable.
* The goal is not to minimize the length of the rewrite. The goal is to make the original information understandable while preserving its factual content.

For example:

* "fine-tuned" can be explained as "further trained or adapted for a specific task."
* "image embeddings" can be explained as "numerical representations of images that the model can process."
* "parameter-efficient" can be explained as using relatively few model parameters, without adding unsupported claims about performance.
* "labeled data" can be explained as data accompanied by labels or corresponding information identifying the desired output.
* "reinforcement learning" can be explained as a training approach in which a model learns from feedback or rewards.
* "end-to-end" can be explained as a process in which the input is transformed into the final output through one integrated pipeline.

These explanations should clarify the concept, not evaluate it.

#### Avoid unsupported claims and qualifiers

* Do NOT add subjective, evaluative, or qualitative adjectives or adverbs that are not supported by the original text.
* Do NOT describe a model, method, system, component, or result as "powerful," "effective," "efficient," "advanced," "sophisticated," "versatile," "complex," "innovative," "robust," or similar unless the original text explicitly supports that description.
* Do NOT add claims about performance, quality, effectiveness, efficiency, benefits, advantages, or capabilities unless they are stated or reasonably implied by the original text.
* Do NOT add purposes or intended outcomes that are not stated or reasonably implied by the original text.
* Do NOT add comparisons with other models, systems, or methods unless the original text contains such a comparison.
* Do NOT use adjectives or adverbs merely to make the text sound more impressive, informative, or natural.
* When simplifying a technical statement, explain what the concept means or does rather than describing it positively or negatively.
* When explaining a technical component, describe its general function accurately and neutrally. Do not invent specific implementation details or unsupported benefits.

For example:

Original:
"The model supports tool calling."

Incorrect:
"The model supports tool calling effectively."

Reason:
"Effectively" introduces an unsupported claim about the quality of the capability.

Correct:
"The model supports tool calling."

---

Original:
"The model uses agentic reinforcement learning for decision-making."

Incorrect:
"The model uses sophisticated agentic reinforcement learning for intelligent decision-making."

Reason:
"Sophisticated" and "intelligent" introduce unsupported qualitative judgments.

Correct:
"The model uses agentic reinforcement learning, a training approach in which the model learns through feedback or rewards, for decision-making."

---

Original:
"The model combines information from different domains."

Incorrect:
"The model combines information from different domains to achieve better performance."

Reason:
"Better performance" introduces an unsupported benefit.

Correct:
"The model combines information from different domains."

#### Explanations must not replace original claims

* Do not replace an explicit claim with only an explanation of that claim.
* Preserve the original claim and add the explanation when needed.

For example:

Original:
"Whisper is a state-of-the-art speech recognition model."

Incorrect:
"Whisper is an advanced speech recognition model."

Reason:
The original claim "state-of-the-art" has been weakened and replaced.

Correct:
"Whisper is a state-of-the-art speech recognition model, meaning it represents a leading level of performance in speech recognition."

Only add the explanation if it can be expressed accurately and neutrally.

#### Final verification

Before returning the answer, check the rewrite internally:

1. Is every original factual claim still present?
2. Is every important technical concept still present?
3. Have explicitly stated attributes been preserved?
4. Are unfamiliar technical concepts explained when an explanation would improve understanding?
5. Does each explanation accurately describe the concept without adding unsupported model-specific information?
6. Did I introduce any new claim about performance, quality, effectiveness, efficiency, benefits, capabilities, or complexity?
7. Did I introduce any unsupported adjective or adverb?
8. Did I add a purpose, benefit, comparison, or evaluation that was not in the original?
9. Did I accidentally weaken, remove, or replace an original claim?
10. If an added sentence only explains an existing concept and does not introduce a new unsupported claim, keep it.

If an added word or sentence makes the model sound better, more capable, more efficient, more advanced, or more sophisticated without support from the original text, remove it.

### Output

* Return ONLY the final rewritten text.
* Do NOT include an introduction sentence.
* Do NOT include an explanation of your changes.
* Do NOT include any extra text before or after the rewritten text.
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
        assert task in Ollama.tasks, "Not supported task: "+task
        if not content:
            yield '{"message": {"content": ""}}\n'
            return
        payload = {
            "model": self._model,
            "stream": True,
            "messages": [{"role": "system", "content": Ollama.tasks[task]}, {"role": "user", "content": content}]
        }
        if params:
            payload.update(params)
            
            
        with requests.post(self._url, json=payload, stream=True) as r:
            for line in r.iter_lines():
                if line:
                    data = json.loads(line)
                    # data = data['message']['content']
                    yield json.dumps(data) + "\n"
            