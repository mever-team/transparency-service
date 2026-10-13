# Agents-A1: Scaling the Horizon, Not the Parameters: Reaching Trillion-Parameter Performance with a 35B Agent
> This repository contains model weights and configuration files for Agents-A1 in the Hugging Face Transformers format.
> These artifacts are compatible with Hugging Face Transformers, vLLM, SGLang, etc.
- **2026.7.14**: 🔥🔥 The 4B model has been released.
- **2026.7.8**: 🔥🔥 By popular demand from the community, our 4B model is coming in the next few days — making it faster and easier to build your own local AI assistant.
- **2026.7.2**: 🔥🔥 Based on Agents-A1, we have released a series of quantized model variants. Please refer to the [Agents-A1 collection](https://huggingface.co/collections/InternScience/agents-a1). Besides, we’d like to thank the [mlx-community](https://huggingface.co/collections/mlx-community/agents-a1) for providing quantized versions at multiple scales. Try running Agents-A1 on your Mac!
- **2026.6.26**: 🔥🔥 We have open-sourced the Agents-A1 35B-A3B model, along with the evaluation code for selected domains and the technical report.
**Agents‑A1** is a 35B Mixture‑of‑Experts agentic model from [InternScience](https://huggingface.co/InternScience), built to scale heterogeneous agentic abilities across multiple domains including **Long‑horizon Search, Engineering, Scientific Research, Instruction Following, and Tool-calling**. We investigate agent-horizon scaling from two perspectives: scaling long-horizon trajectories and scaling heterogeneous agent abilities. 
From the scaling of long-horizon trajectories, **Agents‑A1** is trained with the assistance of a domain-grounded knowledge-action infrastructure that jointly constructs actions, observations, and verifier outcomes, turning the agent's process into a trainable target. From the scaling of heterogeneous agent abilities, **Agents‑A1** presents a three-stage training paradigm for building scalable general-purpose agentic model. First, we perform full-domain supervised fine-tuning to align the base model with broad agentic behaviors. Second, we train domain-level teacher models to capture specialized expertise in each domain. Third, we propose multi-teacher multi-domain on-policy distillation with heterogeneity-aware optimization to improve knowledge transfer efficiency across different domains.
![Agents-A1 Benchmark Overview](./figures/a1_benchmarks_altair_grid.svg)
- **Agentic Reasoning**: Agents-A1 excels at decomposing complex tasks into executable sub-steps, planning ahead, and adapting its strategy based on intermediate results.
- **Tool Use**: Natively supports function calling and tool integration, enabling seamless interaction with APIs, code interpreters, search engines, and other external tools.
- **Scientific and Professional Reasoning**: Handles tool-integrated scientific reasoning and professional knowledge question answering.
- **Instruction Following**: Precisely follows detailed, multi-constraint instructions across diverse domains.
We welcome developers and enterprises to integrate and try Agents-A1 and share their feedback.
We evaluate Agents-A1 in real-world agentic and research-oriented workflows across six directions — long-horizon search, engineering tasks, scientific research, instruction following, general agentic tasks, and scientific agentic tasks. Despite operating in the ~35B model class, Agents-A1 delivers highly competitive performance against frontier-scale systems such as GPT-5.5, DeepSeek-V4-pro, and Kimi-K2.6. It achieves overall SOTA results on several challenging benchmarks, including Seal-0 (56.4), HiPhO (46.4), FrontierScience-Olympiad (79.0), FrontierScience-Research (40.00), IFBench (80.6), and IFEval (94.8), while also ranking as the best among comparable models on a broad range of tasks such as BrowseComp (75.5), XBench-DS-2510 (86.0), GAIA (96.0), SciCode (44.3), HLE with tools (47.6), and MolBench-bind (56.8). These results show that Agents-A1 combines strong long-horizon search ability, robust scientific reasoning, and reliable instruction following, establishing it as a highly capable and efficient agentic model that narrows the gap with much larger frontier models.
🟢 Best Among Comparable Models (~35B)
[SGLang](https://github.com/sgl-project/sglang) is a fast serving framework for large language models and vision language models.
uv venv --python 3.12 --seed --managed-python
See [its documentation](https://docs.sglang.ai/get_started/install.html) for more details.
The following commands create API endpoints at `http://localhost:8000/v1`:
- **Standard Version** (1 GPUs, 262K context):
  python -m sglang.launch_server \
    --model-path InternScience/Agents-A1 \
  python -m sglang.launch_server \
    --model-path InternScience/Agents-A1 \
    --tool-call-parser qwen3_coder
[vLLM](https://github.com/vllm-project/vllm) is a high-throughput and memory-efficient inference and serving engine for LLMs.
Install vLLM from the main branch via uv:
uv venv --python 3.12 --seed --managed-python
uv pip install vllm --torch-backend=auto
See [its documentation](https://docs.vllm.ai/en/stable/getting_started/installation/index.html) for more details.
The following commands create API endpoints at `http://localhost:8000/v1`:
- **Standard Version** (1 GPUs, 262K context):
  vllm serve InternScience/Agents-A1 \
  vllm serve InternScience/Agents-A1 \
    --tool-call-parser qwen3_coder
- **Text-Only** (skips vision encoder to free KV cache memory):
  vllm serve InternScience/Agents-A1 \
### Recommended Sampling Parameters
For the best generation quality, we recommend the following sampling parameters:
## Agent Capability Evaluation
To provide the community with a unified agent evaluation codebase for fair comparison, we have also open-sourced an evaluation framework for assessing agentic models across core capabilities, including tool use and multi-step reasoning. The evaluation code is included in the [Agents-A1/evaluation](https://github.com/InternScience/Agents-A1/tree/main/evaluation) of this repository.
We use this framework to evaluate the released model under a standardized and reproducible setting. 
Specifically, the model is tested on a set of agent-oriented tasks that require it to understand user goals, decompose complex instructions, interact with tools or environments when necessary, and produce final results. The evaluation results reported in [Model Card](https://huggingface.co/InternScience/Agents-A1) are generated using the open-source framework above, so that users can reproduce the experiments, compare other models under the same protocol, and further extend the benchmark for new agent scenarios. (**Note that:** To ensure a fair comparison, we report the benchmark results from their original technical reports. If a model does not report the corresponding benchmark results, we evaluate it using the same evaluation protocol as our model.)
For detailed evaluation scripts, task definitions, metrics, and reproduction instructions, please refer to the evaluation codebase.
If you find our work helpful, feel free to give us a cite.
@misc{bai2026scalinghorizonparametersreaching,
      title={Scaling the Horizon, Not the Parameters: Reaching Trillion-Parameter Performance with a 35B Agent}, 
      author={Lei Bai and Zongsheng Cao and Yang Chen and Zhiyao Cui and Shangheng Du and Yue Fan and Shiyang Feng and Zijie Guo and Haonan He and Liang He and Xiaohan He and Shuyue Hu and Yusong Hu and Songtao Huang and Yichen Jiang and Hao Li and Xin Li and Dahua Lin and Weihao Lin and Fenghua Ling and Dongrui Liu and Zhuo Liu and Runmin Ma and Chunjiang Mu and Haoyang Peng and Tianshuo Peng and Jinxin Shi and Luohe Shi and Boyuan Sun and Zelin Tan and Shengji Tang and Qianyi Wang and Yiming Wu and Yi Xie and Xiangchao Yan and Jingqi Ye and Peng Ye and Fangchen Yu and Jiakang Yuan and Bihao Zhan and Bo Zhang and Chen Zhang and Shufei Zhang and Shuaiyu Zhang and Wenlong Zhang and Yiqun Zhang and Junpeng Zhao and Zhijie Zhong and Bowen Zhou and Yuhao Zhou},
      url={https://arxiv.org/abs/2606.30616}, 