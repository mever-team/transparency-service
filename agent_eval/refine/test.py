import json
from aicard.service.assistants.prompter import Prompter
from aicard.agents import Ollama
from aicard.service.logger import Logger

logger = Logger()
prompter = Prompter(Ollama("mistral:latest", name="🌬️ Mistral", timeout_secs=45))


with open("dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

for i, sample in enumerate(dataset):
    text = ''
    for chunks in prompter.refine_field(sample['input'], logger):
        chunks = json.loads(chunks)
        text += chunks['message']['content']
        
    print(f'Output {i}:\n' + text)