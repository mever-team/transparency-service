import json
from modelcard.agents.gpt import GPT
from modelcard.agents.ollama import Ollama

# linux ollama installation
# - curl -fsSL https://ollama.com/install.sh | sh
# - ollama pull llama3.2
# run in the console for testing
# - ollama run llama3.2

some_text = """Artificial intelligence (AI) refers to the ability of machines to perform tasks that typically 
require human intelligence. This includes learning, reasoning, problem-solving, perception, and decision-making. 
AI is a broad field encompassing various technologies, including machine learning and natural language processing. 
It is used in numerous applications, from self-driving cars to language translation and data analysis."""

llama = Ollama("llama3.2")
llama_summary = llama.summarization(some_text)
print('llama summarization:', llama_summary)
llama_json = llama.completion(json.dumps({"your_name": "", "a_joke": ""}))
print('llama completion:', llama_json)

gpt = GPT()
gpt_summary = gpt.summarization(some_text)
print('gpt summarization:', gpt_summary)
gpt_json = gpt.completion(json.dumps({"your_name": "", "a_joke": ""}))
print('gpt completion:', gpt_json)