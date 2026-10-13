**A next-generation family of agentic models built for long-horizon tasks in real-world environments.**
Today, Nex-AGI officially introduces **Nex-N2.5**, its next-generation family of agentic models.
Nex-N2.5 is available in three sizes: **mini**, **Pro**, and **Max**. Nex-N2.5-mini and Nex-N2.5-Pro continue to build on the multimodal foundations of Nex-N2, with focused improvements in computer use, web browsing, and visually grounded agentic capabilities. Nex-N2.5-Max is built on a 1.6-trillion-parameter, text-only Mixture-of-Experts (MoE) foundation model, marking our first complete post-training effort at trillion-parameter scale.
For long-horizon tasks in real-world environments, Nex-N2.5 further strengthens its ability to act continuously and self-correct through visual feedback. The models can operate computers and browsers, as well as autonomously execute and test programs. Vision is therefore no longer merely an input modality; it has become a critical interface through which an agent perceives its environment, verifies outcomes, and moves a task forward.
Building on this foundation, we have further expanded the range of agent training environments, task types, and productivity scenarios, while completing systematic post-training at trillion-parameter scale for the first time. Through broader task coverage and richer environmental feedback, Nex-N2.5 delivers further gains in scientific research, knowledge work, and complex productivity tasks. This work also provides valuable practical experience for training agentic capabilities in even larger models.
By jointly advancing model training, infrastructure, and real-world agent scenarios, Nex-AGI aims to continue driving progress in agentic intelligence.
Model weights for the Nex-N2.5 family will be released as open source, alongside hosted online services.
- **Nex-N2.5-Max:** [Hugging Face](https://huggingface.co/nex-agi/Nex-N2.5-Max) | [ModelScope](https://modelscope.cn/models/nex-agi/Nex-N2.5-Max)
- **Nex-N2.5-Pro:** [Hugging Face](https://huggingface.co/nex-agi/Nex-N2.5-Pro) | [ModelScope](https://modelscope.cn/models/nex-agi/Nex-N2.5-Pro)
- **Nex-N2.5-mini:** [Hugging Face](https://huggingface.co/nex-agi/Nex-N2.5-mini) | [ModelScope](https://modelscope.cn/models/nex-agi/Nex-N2.5-mini)
- **Hosted Access:** [OpenRouter (Nex-N2.5-Pro)](https://openrouter.ai/nex-agi/nex-n2.5-pro) | [OpenRouter (Nex-N2.5-mini)](https://openrouter.ai/nex-agi/nex-n2.5-mini)
- **Websites:** [Global](https://nex-agi.com/)
We welcome developers and enterprises to integrate and try Nex-N2.5 and share their feedback.
We evaluate Nex-N2.5 across coding, agentic workflows, computer use, and multimodal understanding.
![Nex-N2.5 Benchmark Overview: Text and Multimodal](./figures/Nex-N2.5-Benchmark-white.png)
The tables below compare **Nex-N2.5-mini**, **Nex-N2.5-Pro**, and **Nex-N2.5-Max** with leading models across our evaluation suite.1, 2 **Bold** marks the best result in each benchmark, including ties; — indicates unavailable data.10
Terminal-Bench 2.173.482.786.189.188.888.388.287.986.6
SWE-Bench Pro43.861.265.779.264.663.364.655.467.7
DeepSWE v1.136.155.865.673.772.767.566.962.869.3
AutomationBench v1.0.6532.344.250.250.345.846.748.243.239.8
Toolathlon Verified54.668.574.776.574.976.573.074.172.5
GDPval-AA v2144616281713183117111675176315801717
Job Bench28.541.453.665.745.452.958.254.153.4
BrowseComp683.489.792.690.890.491.2———
OSWorld-Verified871.282.275.283.483.284.862.376.786.1
OSWorld-230.556.422.368.362.758.3——46.7
WebTest8, 948.652.8——54.0———52.3
WebArena-Verified863.467.6——69.771.6—62.366.8
OSWorld-G82.987.4—76.877.779.683.359.484.9
Vision2Web752.968.259.0—79.8———75.1
SWE-MM25.538.2—59.440.237.320.639.239.2
OmniDoc89.792.291.6—92.991.1——92.1
1 Score sources: Where available, scores are drawn from official benchmark leaderboards and the latest evaluation reports published by model providers, including the Kimi-K3, Qwen3.8-Max, GLM-5.3, and HY4 reports. Results without a public source are obtained through our own evaluations.
2 Sampling parameters: Our evaluations use temperature = 0.7, top_p = 0.95, and top_k = 40.
3 Evaluation harness: Coding tasks are evaluated using the NexAU harness.
4 DeepSeek-V4-Pro: Our evaluations use the DeepSeek-V4-Pro-0813 version.
5 AutomationBench: We use the Public version.
6 BrowseComp: We apply the Summary context-compaction strategy when the token usage exceeds 60% of the model’s context window.
7 Vision2Web: We report the average score across the Frontend, Webpage, and Website categories, with Gemini-3.5-Flash as the VLM judge and GLM-5V-Turbo (Claude Code) as the GUI agent.
8 Computer-use and browser-use benchmarks, including OSWorld, WebTest, and WebArena, are evaluated using our NexCUA harness. Grounding coordinates are normalized to a 0–1000 scale. The NexCUA project will be open-sourced soon.
9 WebTestBench: These results are evaluated in oracle mode, using the ground-truth checklist to assess defect detection only, without checklist generation.
10 Notation: Bold marks the best result in each benchmark, including ties; — indicates unavailable data.
We also provide a prebuilt Docker image with our customized `sglang` fork preinstalled: **`nexagi/sglang:v0.5.18-nex-patch`**. The launch command is the same as above.
# Multi-node (2 nodes, 16 x H200). Run the same command on every node with:
#    = 0 on the head node, 1 on the other node
#     = IP of the head node (reachable from all others)
docker run --gpus all --shm-size 32g --network host \
  -v /path/to/your/model:/model \
  nexagi/sglang:v0.5.18-nex-patch \
  python3 -m sglang.launch_server \
    --model-path /path/to/your/model \
    --dist-init-addr "${MASTER_ADDR}:5000" \
    --moe-runner-backend deep_gemm \
    --cuda-graph-max-bs-decode 64 \
    --cuda-graph-backend-decode full \
    --cuda-graph-backend-prefill disabled \
    --chat-template /path/to/nex-n2.5-max/chat_template.jinja \
    --reasoning-parser deepseek-r1 \
    --tool-call-parser qwen3_coder
docker run --gpus all --shm-size 32g --ipc=host \
  -v /path/to/your/model:/model \
  nexagi/sglang:v0.5.18-nex-patch \
  python3 -m sglang.launch_server \
    --tool-call-parser qwen3_coder \
    --chat-template /path/to/nex-N2.5-Pro/chat-template.jinja \
    --mamba-scheduler-strategy extra_buffer
docker run --gpus all --shm-size 32g --ipc=host \
  -v /path/to/your/model:/model \
  nexagi/sglang:v0.5.18-nex-patch \
  python3 -m sglang.launch_server \
    --tool-call-parser qwen3_coder \
    --chat-template /path/to/nex-N2.5-mini/chat-template.jinja \
    --mamba-scheduler-strategy extra_buffer
### Recommended Sampling Parameters
For the best generation quality, we recommend the following sampling parameters:
Use `reasoning_effort` to control the thinking behavior of Nex-N2.5:
For adaptive thinking, set `reasoning_effort` to `"medium"` in your OpenAI-compatible Chat Completions request. Replace `` with the model name exposed by your server:
    {"role": "user", "content": "Explain how binary search works."}
The chat template uses `reasoning_effort`; parameters such as `enable_thinking` and `thinking_mode` require gateway-specific translation.
Nex-series models support robust function-calling capabilities. To enable function calling, add the `--tool-call-parser qwen3_coder` flag when launching the server:
python -m sglang.launch_server --model-path /path/to/your/model --tool-call-parser qwen3_coder
When the model produces a reasoning trace, configure SGLang to separate it from the final response:
- **Nex-N2.5-mini and Nex-N2.5-Pro:** `--reasoning-parser qwen3`
- **Nex-N2.5-Max:** `--reasoning-parser deepseek-r1`
The deployment commands above include the appropriate reasoning parser and `--tool-call-parser qwen3_coder`. The parser extracts reasoning content; use `reasoning_effort` to select the thinking mode.