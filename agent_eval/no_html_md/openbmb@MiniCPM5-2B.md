We are releasing **MiniCPM5-2B**, the second model in the **MiniCPM5** series, following [MiniCPM5-1B](https://huggingface.co/openbmb/MiniCPM5-1B). It is a dense 2B Transformer that scales up the same training recipe, built for on-device, local deployment, and resource-constrained scenarios, reaching 2B-class open-source SOTA.
🏆 **2B-class open-source SOTA**: compared with strong open-source models of similar size, MiniCPM5-2B achieves SOTA performance within this comparison set. It remains competitive with 4B-class models overall, while showing its advantages over models of comparable size in coding, mathematics, long-context understanding, tool use, and agentic tasks.
📂 **Open High-Quality Data**: Alongside the model, we are releasing the high-quality training datasets behind it as part of the [UltraData](https://ultradata.openbmb.cn/) family: [UltraX](https://huggingface.co/datasets/openbmb/UltraX-Preview), a high-quality web pre-training dataset; [UltraData-Code](https://huggingface.co/datasets/openbmb/UltraData-Code), featuring L0–L3 tiered code data management to drive a significant leap in coding capabilities; [UltraData-SFT-Agent-2609](https://huggingface.co/datasets/openbmb/UltraData-SFT-Agent-2609), comprising 500K agent training samples to enhance comprehensive on-device agent capabilities; and [UltraData-RL-2609](https://huggingface.co/datasets/openbmb/UltraData-RL-2609), with 80K+ high-quality RL training samples covering mathematics, code, general knowledge, and long-context reasoning.
Use this directory to choose the model format that matches your runtime:
- **[MiniCPM5-2B](https://huggingface.co/openbmb/MiniCPM5-2B)** · [ModelScope](https://www.modelscope.cn/models/OpenBMB/MiniCPM5-2B) · BF16 final release (post-trained with RL + OPD) **👈 you are here**
- **[MiniCPM5-2B-SFT](https://huggingface.co/openbmb/MiniCPM5-2B-SFT)** · [ModelScope](https://www.modelscope.cn/models/OpenBMB/MiniCPM5-2B-SFT) · BF16 SFT-only checkpoint (before RL / OPD)
- **[MiniCPM5-2B-Midtrain](https://huggingface.co/openbmb/MiniCPM5-2B-Midtrain)** · [ModelScope](https://www.modelscope.cn/models/OpenBMB/MiniCPM5-2B-Midtrain) · BF16 mid-training checkpoint (before SFT)
- **[MiniCPM5-2B-Base](https://huggingface.co/openbmb/MiniCPM5-2B-Base)** · [ModelScope](https://www.modelscope.cn/models/OpenBMB/MiniCPM5-2B-Base) · BF16 base checkpoint (pre-training only)
- **[MiniCPM5-2B-GGUF](https://huggingface.co/openbmb/MiniCPM5-2B-GGUF)** · [ModelScope](https://www.modelscope.cn/models/OpenBMB/MiniCPM5-2B-GGUF) · GGUF for llama.cpp / Ollama / LM Studio
- **[MiniCPM5-2B-MLX](https://huggingface.co/openbmb/MiniCPM5-2B-MLX)** · [ModelScope](https://www.modelscope.cn/models/OpenBMB/MiniCPM5-2B-MLX) · MLX / 4bit for Apple Silicon
- **[MiniCPM5-2B-GPTQ](https://huggingface.co/openbmb/MiniCPM5-2B-GPTQ)** · [ModelScope](https://www.modelscope.cn/models/OpenBMB/MiniCPM5-2B-GPTQ) · GPTQ / 4bit quantized model
- **[MiniCPM5-2B-DSpark](https://huggingface.co/openbmb/MiniCPM5-2B-DSpark)** · [ModelScope](https://www.modelscope.cn/models/OpenBMB/MiniCPM5-2B-DSpark) · DSpark draft model for inference acceleration
- **[MiniCPM5-2B-DSpark-GGUF](https://huggingface.co/openbmb/MiniCPM5-2B-DSpark-GGUF)** · [ModelScope](https://www.modelscope.cn/models/OpenBMB/MiniCPM5-2B-DSpark-GGUF) · GGUF version of DSpark draft model
- **[MiniCPM5-2B-LiteRT](https://huggingface.co/litert-community/MiniCPM5-2B)** · [ModelScope](https://www.modelscope.cn/models/litert-community/MiniCPM5-2B) · the LiteRT-LM version of MiniCPM5-2B
- **[MiniCPM5-1B](https://huggingface.co/openbmb/MiniCPM5-1B)** · [ModelScope](https://www.modelscope.cn/models/OpenBMB/MiniCPM5-1B) · BF16 final release (post-trained with RL + OPD)
- **[MiniCPM5-1B-SFT](https://huggingface.co/openbmb/MiniCPM5-1B-SFT)** · [ModelScope](https://www.modelscope.cn/models/OpenBMB/MiniCPM5-1B-SFT) · BF16 SFT-only checkpoint (before RL / OPD)
- **[MiniCPM5-1B-Base](https://huggingface.co/openbmb/MiniCPM5-1B-Base)** · [ModelScope](https://www.modelscope.cn/models/OpenBMB/MiniCPM5-1B-Base) · BF16 base checkpoint (pre-training only)
- **[MiniCPM5-1B-GGUF](https://huggingface.co/openbmb/MiniCPM5-1B-GGUF)** · [ModelScope](https://www.modelscope.cn/models/OpenBMB/MiniCPM5-1B-GGUF) · GGUF for llama.cpp / Ollama / LM Studio
- **[MiniCPM5-1B-MLX](https://huggingface.co/openbmb/MiniCPM5-1B-MLX)** · [ModelScope](https://www.modelscope.cn/models/OpenBMB/MiniCPM5-1B-MLX) · MLX / 4bit for Apple Silicon
MiniCPM5-2B has the following features:
- **Type**: Causal Language Model
- **Architecture**: Standard `LlamaForCausalLM`
- **Number of Parameters**: 2,516,756,480
- **Number of Non-Embedding Parameters**: 1,981,982,720
- **Number of Attention Heads (GQA)**: 16 for Q and 2 for KV
MiniCPM5-2B is the second model in the MiniCPM5 series. It is designed for local assistants, coding agents, tool-use workflows, and reasoning scenarios where a compact model is preferred. The model keeps a small deployment footprint while providing native long-context support.
We compare **MiniCPM5-2B** with strong open-source models in the same size class, including **LFM2.5-2.6B**, **Qwen3.5-2B**, and **Gemma-4-E2B-it**, while also listing larger models such as **Qwen3.5-4B**, **granite-4.2-3B**, **Nemotron-3-Nano-4B**, **Gemma-4-E4B-it**, and **LFM2.5-8B-A1B** for reference.
Within this comparison set, MiniCPM5-2B reaches 2B-class open-source SOTA with an average score of **53.9**, and also exceeds all of the larger models included here (the highest is **51.1**). Its advantages are most visible in code reasoning, math reasoning, long-context understanding, tool use, and multiple agentic tasks.
Evaluation Results of MiniCPM5-2B and Baselines
MiniCPM5-2B2B-class Models4B-class ModelsLFM2.5-2.6BQwen3.5-2BGemma-4-E2B-itQwen3.5-4Bgranite-4.2-3BNemotron-3-Nano-4BGemma-4-E4B-itLFM2.5-8B-A1B
Average53.933.228.024.651.142.732.631.228.4
LiveCodeBench v669.142.120.242.956.458.950.753.939.8
LCB-Pro 25Q2 (Easy)68.030.910.327.158.354.651.645.827.8
LCB-Pro 25Q2 (Medium)17.50.00.00.07.05.35.31.80.0
OJBench32.511.22.611.624.821.820.019.08.2
SciCode (wbg)26.3†14.2†2.8†20.9†16.1†24.9†16.4†24.4†7.8†
AIME 202586.541.929.631.778.879.456.337.146.0
AIME 202686.545.229.039.882.783.562.145.056.7
HMMT Feb 202663.833.720.517.864.060.851.330.138.5
MATH-50094.689.685.885.499.097.091.688.293.2
IFBench66.359.046.025.759.073.058.328.351.0
IFEval86.793.477.531.490.293.788.044.490.8
Multi-IF71.876.857.140.373.675.965.945.971.4
MMLU-Pro70.865.264.356.078.065.865.768.363.1
MMLU-Redux84.780.080.071.888.778.979.883.780.0
HLE8.9†6.2†2.6†4.8†9.9†6.6†4.9†3.8†6.9†
GPQA-Diamond70.2†55.8†45.6†43.3†77.1†55.9†51.3†57.6†51.3†
SuperGPQA40.826.238.630.352.839.937.838.734.5
AA-LCR59.0†5.3†28.7†17.0†61.0†24.3†17.3†33.0†0.0†
NoLiMa68.10.717.13.943.55.11.12.30.5
LongBenchPro44.823.78.242.258.434.827.953.519.6
LongBench v243.730.324.933.247.336.032.042.730.4
τ³-Bench Banking20.8†7.2†2.13.96.8†5.6†1.24.13.4
τ²-Bench Telecom97.190.469.0†20.8†92.1†40.928.1†20.8†16.1†
BFCL v466.661.143.636.656.852.243.747.049.2
SWE-bench Verified46.46.05.02.033.636.83.015.00.4
SWE-bench Pro14.40.60.80.028.212.30.13.30.4
Terminal-Bench v2.18.6†4.5†3.0†0.4†25.8†13.9†3.8†1.9†1.9
BrowseComp-ZH43.59.818.24.739.621.13.37.013.2
BrowseComp Top10039.713.719.36.033.319.04.76.39.7
GAIA Text-10388.749.547.930.178.657.326.539.541.1
GDPval-AA v219.6†4.50.00.011.70.0†0.00.00.0
Claw-Gym59.219.325.531.351.660.033.737.92.7
WildClaw23.910.29.28.917.020.08.914.34.5
QwenClaw42.919.318.214.537.136.416.816.74.5
1. Blue bold indicates the best result across all models in the row (including 4B-class models); Black bold indicates the best result among 2B-class models.2. Scores marked † come from the official Artificial Analysis release; all others are reproduced internally.
The training of MiniCPM5-2B is a full-stack practice of **[UltraData Tiered Data Management](https://arxiv.org/pdf/2602.09003)**, covering three stages: base training, mid-training, and post-training.
During **base training**, the model goes through stable training and decay training to build core language capability and training stability. It then enters **mid-training** to further strengthen target capabilities and adapt to the target data distribution. The training corpus is released alongside the model as [Ultra-FineWeb](https://huggingface.co/datasets/openbmb/Ultra-FineWeb), [Ultra-FineWeb-L3](https://huggingface.co/datasets/openbmb/Ultra-FineWeb-L3), [UltraX](https://huggingface.co/datasets/openbmb/UltraX-Preview), [UltraData-Code](https://huggingface.co/datasets/openbmb/UltraData-Code) and [UltraData-Math](https://huggingface.co/datasets/openbmb/UltraData-Math).
During **post-training**, we proceed in three steps: **SFT**, **RL**, and **OPD**. We first use **400B tokens of deep-thinking SFT** to establish deep-thinking and general chat abilities; the SFT data is released as [UltraData-SFT-2605](https://huggingface.co/datasets/openbmb/UltraData-SFT-2605) and the Agent SFT data is released as [UltraData-SFT-Agent-2609](https://huggingface.co/datasets/openbmb/UltraData-SFT-Agent-2609). We then train specialized **RL teachers** for math, code, agentic tasks, writing, and related domains (with the corresponding data also open-sourced as [UltraData-RL-2609](https://huggingface.co/datasets/openbmb/UltraData-RL-2609)), and use **On-Policy Distillation (OPD)** to distill these teachers back into one release model.
![MiniCPM5-2B Training Recipe](https://raw.githubusercontent.com/OpenBMB/MiniCPM/main/assets/minicpm5/minicpm5_2b_training_recipe.jpg)
**RL + OPD** is a key part of MiniCPM5-2B post-training. During the **RL** stage, we adopted the critic-based algorithm described in [JustRL II](https://panhaoxuan.notion.site/justrl-ii-scaling-small-llms-to-128k-reasoning-with-a-critic), substantially improving training stability and achieving significant gains across multiple domains. On the benchmarks listed below, RL + OPD improves reasoning and general capabilities by an average of **↑10.96 points**, and agentic capabilities by **↑6.96 points**.
**OPD** merges the capabilities of 16 expert models produced by RL training, including 5 agentic expert models. At each response position, we compute the full-vocabulary reverse KL divergence between student and teacher logits as the advantage estimate, replacing the original verification-based advantage. OPD directly reuses the prompts used to train each RL teacher as distillation data, so no additional corpus construction is required.
![MiniCPM5-2B RL + OPD Gains](https://raw.githubusercontent.com/OpenBMB/MiniCPM/main/assets/minicpm5/minicpm5_2b_rl_opd_score_gains.png)
> We recommend using the following sets of sampling parameters for generation: `temperature=1.0, top_p=0.95, min_p=0.0`.
> If you encounter repetitive outputs, try: `temperature=1.0, top_p=0.95, min_p=0.0, repetition_penalty=1.05`.
> Please note that the support for sampling parameters varies according to inference frameworks.
vllm serve openbmb/MiniCPM5-2B --port 8000
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
    "model": "openbmb/MiniCPM5-2B",
    "messages": [{"role": "user", "content": "Who are you? Please briefly introduce yourself."}],
pip install "sglang[srt]>=0.5.16"
python -m sglang.launch_server --model-path openbmb/MiniCPM5-2B --port 30000
curl http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
    "model": "openbmb/MiniCPM5-2B",
    "messages": [{"role": "user", "content": "Who are you? Please briefly introduce yourself."}],
**Speculative decoding (DSpark)**: we also release [MiniCPM5-2B-DSpark](https://huggingface.co/openbmb/MiniCPM5-2B-DSpark), a DSpark draft model trained for MiniCPM5-2B. Enable it in SGLang to accelerate decoding while keeping the target model's outputs unchanged:
python -m sglang.launch_server \
  --model-path openbmb/MiniCPM5-2B \
  --speculative-algorithm DSPARK \
  --speculative-draft-model-path openbmb/MiniCPM5-2B-DSpark \
  --speculative-dspark-block-size 7 \
llama-server -m MiniCPM5-2B-F16.gguf -a MiniCPM5-2B --port 8080 -ngl 99 -c 8192 --jinja
`-c 8192` sets the context length. You can adjust this value as needed.
curl http://localhost:8080/v1/chat/completions \
    -H "Content-Type: application/json" \
        "messages": [{"role": "user", "content": "1+1=?"}],
        "temperature": 1.0, "top_p": 0.95, "min_p": 0.0, "max_tokens": 256
In llama.cpp, the default `min_p=0.05` can lead to repetitive output: it filters out tokens whose probability is below 5% of the highest-probability token, potentially discarding the exact tokens needed to break out of a repetition loop. To prevent this, we set `min_p=0.0`.
pip install -U "transformers>=5.6" accelerate torch
from transformers import AutoModelForCausalLM, AutoTokenizer
model_id = "openbmb/MiniCPM5-2B"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
messages = [{"role": "user", "content": "Who are you? Please briefly introduce yourself."}]
inputs = tokenizer.apply_chat_template(
outputs = model.generate(**inputs, max_new_tokens=128)
print(tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True))
For tool / function calling, **SGLang is the recommended backend**. MiniCPM5-2B emits XML-style tool calls and SGLang's built-in `minicpm5` parser converts them to OpenAI-compatible `tool_calls` natively:
python -m sglang.launch_server --model-path openbmb/MiniCPM5-2B --port 30000 \
    --tool-call-parser minicpm5      # or: --tool-call-parser auto
## GitHub Cookbooks and Agent Skills
MiniCPM5-2B uses the **standard `LlamaForCausalLM` architecture**, so mainstream inference engines can load it directly: **no custom kernels, no model-code fork**. For step-by-step deployment and fine-tuning instructions, use the GitHub cookbooks below. Agent Skills are linked as GitHub resources for users working with Cursor / Claude Code style coding agents.
### Other Supported Frameworks
In addition to the deployment and fine-tuning frameworks listed above, MiniCPM5-2B is also supported by FlagOS for multi-chip deployment.
To enable large-scale deployment across different AI chips, Beijing Zhiyuan Research Institute, together with numerous research institutions, chip manufacturers, system vendors, and algorithm and software organizations both domestically and internationally, jointly initiated and established the FlagOS Open Source Community.
The FlagOS community is dedicated to building a unified, open-source system software stack for various AI chips, encompassing core open-source projects such as a large-scale operator library, a unified AI compiler, parallel training and inference frameworks, and a unified communication library. It aims to create an open technology ecosystem connecting the “model-system-chip” layers. By enabling “develop once, deploy across chips”, FlagOS unlocks the computational potential of hardware, breaks down the ecosystem silos between different chip software stacks, and effectively reduces migration costs for developers.The FlagOS community fosters an AI hardware and software ecosystem, overcomes single-vendor closed-source monopolies, promotes widespread deployment of AI hardware technologies, and is committed to rooted in China while embracing global collaboration.
Official website express: [https://flagos.io](https://flagos.io/)
FlagOS multi-chip support and usage
#### FlagOS: Supporting Multiple AI Chips
Thanks to FlagOS’s unified multi-chip AI system software stack, MiniCPM5-2B was adapted to 9 different AI chips in an extremely short time. Currently, the multi-chip version of MiniCPM5-2B has been released on FlagRelease, FlagOS’s platform for automatic migration, adaptation, and deployment of large models across multi-architecture AI chips. Details are as follows:
##### FlagOS Performance Acceleration on Nvidia
###### From FlagRelease (**Recommendation**)
FlagRelease is a platform developed by the FlagOS team for automatic migration, adaptation, and deployment of large models across multi-architecture AI chips. The multi-chip version of MiniCPM5-2B has already been released on FlagRelease. All necessary software packages are pre-installed on the platform, so users do not need to install anything.
###### FlagRelease Image Key Versions
###### FlagRelease Quick Start
- Dependencies: Python 3.12, GLIBC 2.39, GLIBCXX 3.4.33, CXXABI 1.3.15
###### Installing the FlagOS Operator Library
Official Repository: https://github.com/flagos-ai/FlagGems
pip install flag-gems==4.2.1rc0
###### Activating Acceleration
You can enable flagGems acceleration by adding the import of flagGems in the source code of vllm where inference is performed.
flag_gems.enable(record=True, once=True, path="/root/gems.txt")
--served-model-name ${model_name} \
##### Using FlagOS Unified Multi-Chip Backend Plugin
[**vllm-plugin-FL**](https://github.com/flagos-ai/vllm-plugin-FL) is a plugin built for the vLLM inference/service framework. Developed on top of FlagOS’s unified multi-chip backend, it is designed to extend vLLM’s capabilities and performance across a variety of hardware environments.
This model has no autonomous intent or legal personhood; its outputs are text generated from statistical patterns and may be inaccurate, biased, or offensive, and may be manipulated by carefully crafted prompts ("jailbreaks") into producing unintended content. Its responses on sensitive topics such as politics, health, finance, and law are not reviewed by experts and should not be treated as professional advice.
This model is provided "**AS IS**", without warranty of any kind, express or implied, and the developers are not liable for any damages arising from its use. Users must employ the model only for lawful, compliant, and ethical purposes, configure their own safeguards, and label AI-generated content where required; deliberate jailbreaking, injection attacks, or inducing harmful output is prohibited, and any such testing is at the user's own risk.
This repository and MiniCPM model weights are released under the [Apache-2.0](https://github.com/OpenBMB/MiniCPM/blob/main/LICENSE) License.
Please cite our paper if you find our work valuable:
  title={Minicpm4: Ultra-efficient llms on end devices},
  journal={arXiv preprint arXiv:2506.07900},