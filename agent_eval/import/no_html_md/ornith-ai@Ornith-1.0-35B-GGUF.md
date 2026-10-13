[![Ornith Blog](https://img.shields.io/badge/%F0%9F%A6%A2%EF%B8%8F%20Ornith%20Blog%20-FD8E5B)](https://deep-reinforce.com/ornith.html)
Aloha! 🌺 Today, we are releasing Ornith-1.0, a self-improving family of open-source models for agentic coding. 
- **State-of-the-Art Coding Agents**: Available in 9B-Dense, 31B-Dense, 35B-MoE, and 397B-MoE (post-trained on top of Gemma 4 and Qwen 3.5), achieving state-of-the-art performance among open-source models of comparable size on coding benchmarks such as Terminal-Bench 2.1, SWE-Bench, NL2Repo and OpenClaw. 
- **Self-Improving Training Framework**:  Ornith-1.0 employs RL to learn to generate not only solution rollouts, but also the scallfold that drive those rollouts. By jointly optimizing the scaffold and the resulting solution, the model  discovers better search trajectories and generates higher-quality solutions. 
- **Licence**: MIT licensed, globally accessible, and free from regional limitations.
This model card documents **Ornith-1.0-35B**, the lightweight member of the Ornith family, designed for efficient single-GPU deployment.
Terminal-Bench 2.1 (Terminus-2)
Terminal-Bench 2.1 (Claude Code)
* Terminal-Bench 2.1 (Terminus-2): We evaluate Terminal-Bench 2.1 using the Harbor/Terminus-2 framework with parser=json, temperature=1.0, top_p=1.0, and a 128K context window. Each run uses a 4-hour timeout with 32 CPU cores and 48GB RAM, and results are averaged over 5 runs. We adjust the Qwen chat template to ensure consistency between training and inference (https://huggingface.co/deepreinforce-ai/Ornith-1.0-397B/blob/main/chat_template.jinja), and modify Harbor to align with vLLM's reasoning_content key.
* Terminal-Bench 2.1 (Claude Code): We evaluate Terminal-Bench 2.1 using Claude Code 2.1.126 with parser=json, temperature=1.0, top_p=1.0, max_new_tokens=131072. Results are averaged over 5 runs. Again, Qwen chat template needs to be modified.
* SWE-Bench Verified, Pro and Multilingual: using OpenHands harness with temp=1.0, top_p=0.95, 256k context window.
* SWE Atlas QnA, RF, TW: using mini SWE agent harness with temp=1.0, top_p=0.95, 128K context window. Results are averaged over 5 runs.
* NL2Repo: with temperature=1.0, top_p=1.0, 400K context, 48K output and anti-hacking filters.
* ClawEval: An agentic code benchmark over real-user task distributions; temp=0.6 and 256K context.
Ornith-1.0-35B is a reasoning model: by default the assistant turn opens with a <think> … </think> block before the final answer. The serving recipes below enable a reasoning parser so the chain-of-thought is returned in a separate reasoning_content field, and a tool-call parser so the model's <tool_call> blocks are surfaced as OpenAI-style tool_calls.
Serving Ornith-1.0-35B requires recent runtimes:
The two recipes below stand up an OpenAI-compatible server on a single 8×80GB GPU node (tensor-parallel 8). Adjust `--tensor-parallel-size` / `--tp` to the number of GPUs you have.
vllm serve deepreinforce-ai/Ornith-1.0-35B \
    --served-model-name Ornith-1.0-35B \
    --gpu-memory-utilization 0.90 \
    --enable-auto-tool-choice --tool-call-parser qwen3_xml \
python -m sglang.launch_server \
    --model-path deepreinforce-ai/Ornith-1.0-35B \
    --served-model-name Ornith-1.0-35B \
    --tool-call-parser qwen3_coder \
#### Hugging Face Transformers
For a quick local test (or to script offline generation), load the model directly with Transformers. Make sure you have a recent release installed — see the [Transformers installation guide](https://huggingface.co/docs/transformers/installation); Ornith-1.0-35B requires `transformers >= 5.8.1`.
from transformers import AutoModelForCausalLM, AutoTokenizer
model_name = "deepreinforce-ai/Ornith-1.0-35B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    {"role": "user", "content": "Write a Python function is_prime(n). Keep it short."}
text = tokenizer.apply_chat_template(
inputs = tokenizer(text, return_tensors="pt").to(model.device)
output_ids = generated[0][inputs.input_ids.shape[1]:]
# The reply contains a  ...  reasoning block followed by the answer.
content = tokenizer.decode(output_ids, skip_special_tokens=True)
To split the reasoning trace from the final answer, parse on the `` marker:
text = tokenizer.decode(output_ids, skip_special_tokens=True)
    reasoning, answer = text.split("", 1)
    reasoning = reasoning.replace("", "").strip()
    reasoning, answer = "", text.strip()
### Using Ornith-1.0-35B via the Chat Completions API
Once a vLLM or SGLang server is running, talk to it with any OpenAI-compatible client.
    base_url="http://localhost:8000/v1",
    api_key="EMPTY",  # any non-empty string works for a local server
response = client.chat.completions.create(
        {"role": "user", "content": "Write a one-line Python lambda that squares a number."}
message = response.choices[0].message
# reasoning_content holds the  trace; content holds the final answer.
print("reasoning:", getattr(message, "reasoning_content", None))
print("answer:", message.content)
You can also stream tokens, or hand the model tools — Ornith-1.0-35B emits well-formed function calls that the server parses into the standard `tool_calls` field:
            "description": "Get the current weather for a city",
                "properties": {"city": {"type": "string"}},
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "What is the weather in Paris right now?"}],
tool_call = response.choices[0].message.tool_calls[0]
print(tool_call.function.name, tool_call.function.arguments)
# -> get_weather {"city": "Paris"}
You can point any OpenAI-compatible SDK (Python, Node.js, etc.) or `curl` at the same `/v1/chat/completions` endpoint.
Ornith-1.0-35B excels in tool-calling and agentic coding capabilities.
Because Ornith-1.0-35B exposes an OpenAI-compatible endpoint with tool calling, it works out of the box with standard agent frameworks. Below is a minimal example that connects Ornith-1.0-35B to tools through an MCP server.
    base_url=os.getenv("OPENAI_BASE_URL", "http://localhost:8000/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "EMPTY"),
            "description": "Run a shell command and return its output.",
                    "command": {"type": "string", "description": "The command to run"}
messages = [{"role": "user", "content": "List the Python files in the current directory."}]
response = client.chat.completions.create(
    model="deepreinforce-ai/Ornith-1.0-35B",
print(response.choices[0].message)
**Examples of using Ornith with agent harness:**
# Hermes talks to any OpenAI-compatible endpoint — point it at your Ornith server.
export OPENAI_BASE_URL="http://localhost:8000/v1"
export MODEL="deepreinforce-ai/Ornith-1.0-35B"
#### Atomic.chat/ Ollama / llama.cpp 
# Both runtimes load a GGUF build of Ornith (publish one at deepreinforce-ai/Ornith-1.0-35B-GGUF).
# llama.cpp — serve an OpenAI-compatible API on port 8000.
llama-server -hf deepreinforce-ai/Ornith-1.0-35B-GGUF --port 8000 -c 262144
# Ollama — pull and chat with the same GGUF straight from Hugging Face.
ollama run hf.co/deepreinforce-ai/Ornith-1.0-35B-GGUF
# OpenClaw talks to any OpenAI-compatible endpoint — point it at your Ornith server.
export OPENAI_BASE_URL="http://localhost:8000/v1"
export OPENAI_MODEL="deepreinforce-ai/Ornith-1.0-35B"
# Load Ornith for fast local inference or fine-tuning (Python):
#   from unsloth import FastLanguageModel
#   model, tokenizer = FastLanguageModel.from_pretrained(
#       "deepreinforce-ai/Ornith-1.0-35B",
#       max_seq_length=262144,
# OpenHands routes through LiteLLM; the "openai/" prefix selects the OpenAI-compatible path.
export LLM_MODEL="openai/deepreinforce-ai/Ornith-1.0-35B"
export LLM_BASE_URL="http://localhost:8000/v1"
# Launch the CLI (or run the official OpenHands Docker image with the same env vars).
Ornith-1.0-35B is optimized for terminal-based coding agents. Point any OpenAI-compatible coding CLI at your Ornith-1.0-35B endpoint (set `OPENAI_BASE_URL` and `OPENAI_API_KEY`) to understand large codebases, automate tedious work, and ship faster.
# Register your local Ornith endpoint as a provider in ~/.config/opencode/opencode.json:
#   "$schema": "https://opencode.ai/config.json",
#       "npm": "@ai-sdk/openai-compatible",
#       "name": "Ornith (local)",
#       "options": { "baseURL": "http://localhost:8000/v1", "apiKey": "EMPTY" },
#       "models": { "deepreinforce-ai/Ornith-1.0-35B": { "name": "Ornith-1.0-35B" } }
If you find our work helpful, feel free to give us a cite.
    title = {{Ornith-1.0-35B}: Agentic Coding, Open to All},
    url = {https://deep-reinforce.com/ornith_1_0.html},
    author = {{DeepReinforce Team}},