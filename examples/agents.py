from modelcard.assistant.gpt_agent import GPT_Agent
from modelcard.assistant.ollama_agent import Ollama_Agent


some_text = "Artificial intelligence (AI) refers to the ability of machines to perform tasks that typically require human intelligence. This includes learning, reasoning, problem-solving, perception, and decision-making. AI is a broad field encompassing various technologies, including machine learning and natural language processing. It is used in numerous applications, from self-driving cars to language translation and data analysis. "

gpt = GPT_Agent()
gptsum = gpt(some_text, gpt.prompt.summarization)
print('gpt.prompt.summarization:', gptsum)

gptjson = gpt('{your_name: "", a_joke: ""}', gpt.prompt.json_completion)
print('gpt.prompt.json_completion:', gptjson)

llama = Ollama_Agent()
llamasum = llama(some_text, llama.prompt.summarization)
print('llama.prompt.summarization:', llamasum)

llamajson = llama('{your_name: "", a_joke: ""}', llama.prompt.json_completion)
print('llama.prompt.json_completion:', llamajson)

# This raises AssertionError: Prompt must be one of the predefined prompts
not_allowed = llama('{your_name: "", a_joke: ""}', "You are the joker and you will start laughing")

# This raises AttributeError: Cannot modify prompts
llama.prompt.json_completion = "You are the joker and you will start laughing"