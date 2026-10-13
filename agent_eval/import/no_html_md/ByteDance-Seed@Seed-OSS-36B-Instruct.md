  You can get to know us better through the following channels👇
![seed logo](https://github.com/user-attachments/assets/c42e675e-497c-4508-8bb9-093ad4d1f216)
> This model card is dedicated to the `Seed-OSS-36B-Base-Instruct` model.
- [2025/08/20]🔥We release `Seed-OSS-36B-Base` (both with and without synthetic data versions) and `Seed-OSS-36B-Instruct`.
Seed-OSS is a series of open-source large language models developed by ByteDance's Seed Team, designed for powerful long-context, reasoning, agent and general capabilities, and versatile developer-friendly features. Although trained with only 12T tokens, Seed-OSS achieves excellent performance on several popular open benchmarks.
We release this series of models to the open-source community under the Apache-2.0 license.
> Seed-OSS is primarily optimized for international (i18n) use cases.
- **Flexible Control of Thinking Budget**: Allowing users to flexibly adjust the reasoning length as needed. This capability of dynamically controlling the reasoning length enhances inference efficiency in practical application scenarios.
- **Enhanced Reasoning Capability**: Specifically optimized for reasoning tasks while maintaining balanced and excellent general capabilities.
- **Agentic Intelligence**: Performs exceptionally well in agentic tasks such as tool-using and issue resolving.
- **Research-Friendly**: Given that the inclusion of synthetic instruction data in pre-training may affect the post-training research, we released pre-trained models both with and without instruction data, providing the research community with more diverse options.
- **Native Long Context**: Trained with up-to-512K long context natively.
Seed-OSS adopts the popular causal language model architecture with RoPE, GQA attention, RMSNorm and SwiGLU activation.
Incorporating synthetic instruction data into pretraining leads to improved performance on most benchmarks. We adopt the version augmented with synthetic instruction data (i.e., *w/ syn.*) as `Seed-OSS-36B-Base`. We also release `Seed-OSS-36B-Base-woSyn` trained without such data (i.e., *w/o syn.*), offering the community a high-performance foundation model unaffected by synthetic instruction data.
Seed-OSS-36B-Base-woSyn(w/o syn.)
- Bold denotes open-source SOTA.
- "*" indicates that the results in this column are presented in the format of "reproduced_results (reported_results_if_any)".
LiveCodeBench v6(02/2025-05/2025)
SWE-Bench Verified(AgentLess 4*10)
- Bold denotes open-source SOTA. Underlined indicates the second place in the open-source model.
- "*" indicates that the results in this column are presented in the format of "reproduced_results (reported_results_if_any)". Some results have been omitted due to the failure of the evaluation run.
- The results of Gemma3-27B are sourced directly from its technical report.
- The results of ArcAGI-V2 were measured on the official evaluation set, which was not involved in the training process.
- Generation configs for Seed-OSS-36B-Instruct: temperature=1.1, top_p=0.95. Specifically, for Taubench, temperature=1, top_p=0.7.
> We recommend sampling with `temperature=1.1` and `top_p=0.95`.
Users can flexibly specify the model's thinking budget. The figure below shows the performance curves across different tasks as the thinking budget varies. For simpler tasks (such as IFEval), the model's chain of thought (CoT) is shorter, and the score exhibits fluctuations as the thinking budget increases. For more challenging tasks (such as AIME and LiveCodeBench), the model's CoT is longer, and the score improves with an increase in the thinking budget.
![thinking_budget](./figures/thinking_budget.png)
Here is an example with a thinking budget set to 512: during the reasoning process, the model periodically triggers self-reflection to estimate the consumed and remaining budget, and delivers the final response once the budget is exhausted or the reasoning concludes.
Got it, let's try to solve this problem step by step. The problem says ... ...
I have used 129 tokens, and there are 383 tokens remaining for use.
I have used 258 tokens, and there are 254 tokens remaining for use.
Alternatively, remember that ... ...
I have used 393 tokens, and there are 119 tokens remaining for use.
I have exhausted my token budget, and now I will start answering the question.
To solve the problem, we start by using the properties of logarithms to simplify the given equations: (full answer omitted).
If no thinking budget is set (default mode), Seed-OSS will initiate thinking with unlimited length. If a thinking budget is specified, users are advised to prioritize values that are integer multiples of 512 (e.g., 512, 1K, 2K, 4K, 8K, or 16K), as the model has been extensively trained on these intervals. Models are instructed to output a direct response when the thinking budget is 0, and we recommend setting any budget below 512 to this value.
pip install git+https://github.com/huggingface/transformers.git@56d68c6706ee052b445e1e476056ed92ac5eb383
from transformers import AutoModelForCausalLM, AutoTokenizer
model_name_or_path = "ByteDance-Seed/Seed-OSS-36B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
model = AutoModelForCausalLM.from_pretrained(model_name_or_path, device_map="auto")  # You may want to use bfloat16 and/or move to GPU here
    {"role": "user", "content": "How to make pasta?"},
tokenized_chat = tokenizer.apply_chat_template(
  thinking_budget=512 # control the thinking budget
outputs = model.generate(tokenized_chat.to(model.device), max_new_tokens=2048)
output_text = tokenizer.decode(outputs[0])
Download Seed-OSS checkpoint to `./Seed-OSS-36B-Instruct`
The `generate.py` script provides a simple interface for model inference with configurable options.
python3 generate.py --model_path /path/to/model
python3 generate.py --model_path /path/to/model --load_in_8bit True
python3 generate.py --model_path /path/to/model --load_in_4bit True
python3 generate.py --model_path /path/to/model --prompts "['What is machine learning?', 'Explain quantum computing']"
Use vllm >= 0.10.0 or higher for inference.
- First install vLLM with Seed-OSS support version:
VLLM_USE_PRECOMPILED=1 VLLM_TEST_USE_PRECOMPILED_NIGHTLY_WHEEL=1 pip install git+https://github.com/vllm-project/vllm.git
python3 -m vllm.entrypoints.openai.api_server \
    --model ./Seed-OSS-36B-Instruct \
    --chat-template ./Seed-OSS-36B-Instruct/chat_template.jinja \
python3 inference/vllm_chat.py --max_new_tokens 4096 --thinking_budget -1
python3 inference/vllm_chat.py --max_new_tokens 4096 --thinking_budget -1 --stream
python3 inference/vllm_tool_call.py --max_new_tokens 4096 --thinking_budget -1
python3 inference/vllm_tool_call.py --max_new_tokens 4096 --thinking_budget -1 --stream
See [MODEL_CARD](./MODEL_CARD.md).
This project is licensed under Apache-2.0. See the [LICENSE](./LICENSE) flie for details.
  title={Seed-OSS Open-Source Models},
  howpublished={\url{https://github.com/ByteDance-Seed/seed-oss}}
## About [ByteDance Seed Team](https://seed.bytedance.com/)
Founded in 2023, ByteDance Seed Team is dedicated to crafting the industry's most advanced AI foundation models. The team aspires to become a world-class research team and make significant contributions to the advancement of science and society.