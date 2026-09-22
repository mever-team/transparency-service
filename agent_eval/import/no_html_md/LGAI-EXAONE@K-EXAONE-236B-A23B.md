Check out the  NVFP4+GPTQ weights by FuriosaAI!   ➡️ link 
We introduce **K-EXAONE**, a large-scale multilingual language model developed by LG AI Research. Built using a Mixture-of-Experts architecture, K-EXAONE features **236 billion total** parameters, with **23 billion active** during inference. Performance evaluations across various benchmarks demonstrate that K-EXAONE excels in reasoning, agentic capabilities, general knowledge, multilingual understanding, and long-context processing.
- **Architecture & Efficiency:** Features a 236B fine-grained MoE design (23B active) optimized with **Multi-Token Prediction (MTP)**, enabling self-speculative decoding that boosts inference throughput by approximately 1.5x.
- **Long-Context Capabilities:** Natively supports a **256K context window**, utilizing a **3:1 hybrid attention** scheme with a **128-token sliding window** to significantly minimize memory usage during long-document processing.
- **Multilingual Support:** Covers 6 languages: Korean, English, Spanish, German, Japanese, and Vietnamese. Features a redesigned **150k vocabulary** with **SuperBPE**, improving token efficiency by ~30%.
- **Agentic Capabilities:** Demonstrates superior tool-use and search capabilities via **multi-agent strategies.**
- **Safety & Ethics:** Aligned with **universal human values**, the model uniquely incorporates **Korean cultural and historical contexts** to address regional sensitivities often overlooked by other models. It demonstrates high reliability across diverse risk categories.
For more details, please refer to the [technical report](https://arxiv.org/abs/2601.01739), [blog](https://www.lgresearch.ai/blog/view?seq=619) and [GitHub](https://github.com/LG-AI-EXAONE/K-EXAONE).
![main_figure](assets/main_figure.png)
- Number of Parameters: 236B in total and 23B activated
- Number of Parameters (without embeddings): 234B
- Number of Layers: 48 Main layers + 1 MTP layers
  - Hybrid Attention Pattern: 12 x (3 Sliding window attention + 1 Global attention)
  - Number of Attention Heads: 64 Q-heads and 8 KV-heads
  - Head Dimension: 128 for both Q/KV
  - Number of Attention Heads: 64 Q-heads and 8 KV-heads
  - Head Dimension: 128 for both Q/KV
  - No Rotary Positional Embedding Used (NoPE)
  - Number of Activated Experts: 8
  - MoE Intermediate Size: 2,048
- Context Length: 262,144 tokens
- Knowledge Cutoff: Dec 2024 (2024/12)
The following table shows the evaluation results of the K-EXAONE model in reasoning mode, compared to our previous model, [EXAONE-4.0](https://github.com/LG-AI-EXAONE/EXAONE-4.0), and other competing models. The evaluation details can be found in the [technical report](https://arxiv.org/abs/2601.01739).
LiveCodeBench Pro 25Q2 (Medium)
K-EXAONE is supported by multiple libraries. Please install the required libraries as needed for your use case.
You should install `transformers >= 5.1.0` for the K-EXAONE model.
To serve the K-EXAONE model on a vLLM server, you should install both Transformers and vLLM (`vllm >= 0.14.0`).
You should install both Transformers and SGLang to serve the K-EXAONE model on SGLang server.
You can install the latest version of SGLang from source using the following commands.
git clone https://github.com/sgl-project/sglang.git
To use the K-EXAONE model with llama.cpp library, you should install `llama.cpp >= b7737`.
You can use the K-EXAONE model with the Transformers library version `5.1.0` or later.
For tasks that require accurate results, you can run the K-EXAONE model in reasoning mode as below.
from transformers import AutoModelForCausalLM, AutoTokenizer
model_name = "LGAI-EXAONE/K-EXAONE-236B-A23B"
model = AutoModelForCausalLM.from_pretrained(
tokenizer = AutoTokenizer.from_pretrained(model_name)
    {"role": "system", "content": "You are K-EXAONE, a large language model developed by LG AI Research in South Korea, built to serve as a helpful and reliable assistant."},
    {"role": "user", "content": "Which one is bigger, 3.9 vs 3.12?"}
input_ids = tokenizer.apply_chat_template(
    enable_thinking=True,   # skippable (default: True)
generated_ids = model.generate(
output_ids = generated_ids[0][input_ids['input_ids'].shape[-1]:]
print(tokenizer.decode(output_ids, skip_special_tokens=True))
For tasks where latency matters more than accuracy, you can run the K-EXAONE model in non-reasoning mode as below.
    {"role": "system", "content": "You are K-EXAONE, a large language model developed by LG AI Research in South Korea, built to serve as a helpful and reliable assistant."},
    {"role": "user", "content": "Explain how wonderful you are"}
input_ids = tokenizer.apply_chat_template(
generated_ids = model.generate(
output_ids = generated_ids[0][input_ids['input_ids'].shape[-1]:]
print(tokenizer.decode(output_ids, skip_special_tokens=True))
For your AI-powered agent, you can leverage K-EXAONE’s tool calling capability. 
The K-EXAONE model is compatible with both OpenAI and HuggingFace tool calling specifications. 
The example below demonstrates tool calling using HuggingFace’s docstring-to-tool-schema utility.
Please check the [example file](examples/example_output_search.txt) for an example of a search agent conversation using K-EXAONE.
from transformers.utils import get_json_schema
    Roll a dice with the number 1 to N. User can select the number N.
        max_num: The maximum number on the dice.
    return random.randint(1, max_num)
tool_schema = get_json_schema(roll_dice)
    {"role": "system", "content": "You are K-EXAONE, a large language model developed by LG AI Research in South Korea, built to serve as a helpful and reliable assistant."},
    {"role": "user", "content": "Roll a D20 twice and sum the results."}
input_ids = tokenizer.apply_chat_template(
generated_ids = model.generate(
output_ids = generated_ids[0][input_ids['input_ids'].shape[-1]:]
print(tokenizer.decode(output_ids, skip_special_tokens=True))
> To achieve the expected performance, we recommend using the following configurations:
> - We strongly recommend to use `temperature=1.0`, `top_p=0.95`, `presence_penalty=0.0` for best performance.
> - Different from EXAONE-4.0, K-EXAONE uses `enable_thinking=True` as default. Thus, you need to set `enable_thinking=False` when you want to use non-reasoning mode.
TensorRT-LLM provides official support for the K-EXAONE model. Please refer to the [EXAONE Documentation](https://github.com/NVIDIA/TensorRT-LLM/tree/main/examples/models/core/exaone) in the TensorRT-LLM repository for more information.
We support the K-EXAONE model on vLLM. You need to install `vllm >= 0.14.0`.
Practically, you can serve the model with a 256K context length using tensor parallel on 4 H200 GPUs.
After you install the vLLM library with an EXAONE-MoE implementation, you can run the vLLM server by following command:
vllm serve LGAI-EXAONE/K-EXAONE-236B-A23B \
    --reasoning-parser deepseek_v3 \
An OpenAI-compatible API server will be available at http://localhost:8000/v1.
You can test the vLLM server by sending a chat completion request as below:
curl -X POST http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
        "model": "LGAI-EXAONE/K-EXAONE-236B-A23B",
            {"role": "user", "content": "How many r'\''s in \"strawberry\"?"}
        "chat_template_kwargs": {"enable_thinking": true}
If you are interested in using MTP weights for speculative decoding, add according options as below.
vllm serve LGAI-EXAONE/K-EXAONE-236B-A23B \
    --reasoning-parser deepseek_v3 \
We support the K-EXAONE model on SGLang. You need to install the latest version of the SGLang library from source. Please check the [requirements](#requirements) section.
Practically, you can serve the model with a 256K context length using tensor parallel on 4 H200 GPUs.
python -m sglang.launch_server \
    --model LGAI-EXAONE/K-EXAONE-236B-A23B \
A SGLang server will be available at http://localhost:30000.
> Currently, using the OpenAI-compatible server is incompatible with the `transformers>=5.0.0rc0`, so you need to use SGLang native API for now.
> For native API, please refer to the [official documentation](https://docs.sglang.io/basic_usage/native_api.html).
> Once the issue is resolved, we will update this section accordingly.
You can test the SGLang server by sending a request as below:
from transformers import AutoTokenizer
model_name = "LGAI-EXAONE/K-EXAONE-236B-A23B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
    {"role": "user", "content": "How many r'\''s in \"strawberry\"?"}
input_text = tokenizer.apply_chat_template(
    f"http://localhost:30000/generate",
print(response.json()['text'])
If you are interested in in using MTP weights for speculative decoding, add according options as below.
python -m sglang.launch_server \
    --model LGAI-EXAONE/K-EXAONE-236B-A23B \
    --speculative-algorithm EAGLE \
    --speculative-num-draft-tokens 4
The K-EXAONE language model has certain limitations and may occasionally generate inappropriate responses. The language model generates responses based on the output probability of tokens, and it is determined during learning from training data. While we have made every effort to exclude personal, harmful, and biased information from the training data, some problematic content may still be included, potentially leading to undesirable responses. Please note that the text generated by K-EXAONE language model does not reflect the views of LG AI Research.
- Inappropriate answers may be generated, which contain personal, harmful or other inappropriate information.
- Biased responses may be generated, which are associated with age, gender, race, and so on.
- The generated responses rely heavily on statistics from the training data, which can result in the generation of semantically or syntactically incorrect sentences.
- Since the model does not reflect the latest information, the responses may be false or contradictory.
LG AI Research strives to reduce potential risks that may arise from K-EXAONE language models. Users are not allowed to engage in any malicious activities (e.g., keying in illegal information) that may induce the creation of inappropriate outputs violating LG AI's ethical principles when using K-EXAONE language models.
The model is licensed under [K-EXAONE AI Model License Agreement](./LICENSE)
  title={K-EXAONE Technical Report},
  journal={arXiv preprint arXiv:2601.01739},
LG AI Research Technical Support: contact_us@lgresearch.ai