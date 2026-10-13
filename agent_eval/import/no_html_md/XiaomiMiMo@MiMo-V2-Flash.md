**MiMo-V2-Flash** is a Mixture-of-Experts (MoE) language model with **309B total parameters** and **15B active parameters**. Designed for high-speed reasoning and agentic workflows, it utilizes a novel hybrid attention architecture and Multi-Token Prediction (MTP) to achieve state-of-the-art performance while significantly reducing inference costs.
MiMo-V2-Flash creates a new balance between long-context modeling capability and inference efficiency. Key features include:
  * **Hybrid Attention Architecture**: Interleaves Sliding Window Attention (SWA) and Global Attention (GA) with a 5:1 ratio and an aggressive 128-token window. This reduces KV-cache storage by nearly 6x while maintaining long-context performance via learnable **attention sink bias**.
  * **Multi-Token Prediction (MTP)**: Equipped with a lightweight MTP module (0.33B params/block) using dense FFNs. This triples output speed during inference and will be good to accelerates rollout in RL training.
  * **Efficient Pre-Training**: Trained on 27T tokens using FP8 mixed precision and native 32k seq length. The context window supports up to 256k length.
  * **Agentic Capabilities**: Post-training utilizes Multi-Teacher On-Policy Distillation (MOPD) and large-scale agentic RL, achieving superior performance on **SWE-Bench** and complex reasoning tasks.
> We also open-source the 3-layer MTP weights to foster community research.
MiMo-V2-Flash-Base demonstrates strong performance across standard benchmarks, surpassing models with significantly larger parameter counts.
> \* indicates the model may fail to follow the prompt or format.
### Post-training Model Evaluation
Following our Post-Training Paradigm with MOPD and Agentic RL, the model achieves SOTA reasoning and agentic performance.
### Hybrid Sliding Window Attention
MiMo-V2-Flash addresses the quadratic complexity of long contexts by interleaving Local Sliding Window Attention (SWA) and Global Attention (GA).
  * **Configuration**: Stacks of \\(M=8\\) hybrid blocks. Each block contains \\(N=5\\) SWA layers followed by 1 GA layer.
  * **Efficiency**: SWA layers use a window size of 128 tokens, reducing KV cache significantly.
  * **Sink Bias**: Learnable attention sink bias is applied to maintain performance despite the aggressive window size.
### Lightweight Multi-Token Prediction (MTP)
Unlike traditional speculative decoding, our MTP module is natively integrated for training and inference.
  * **Structure**: Uses a dense FFN (instead of MoE) and SWA (instead of GA) to keep the parameter count low (0.33B per block).
  * **Performance**: Facilitates self-speculative decoding, tripling generation speed and mitigating GPU idleness during small-batch RL training.
## 5. Post-Training Technical Highlights
MiMo-V2-Flash leverages a post-training pipeline designed to maximize reasoning and agentic capabilities through innovative distillation and reinforcement learning strategies.
### 5.1 Multi-Teacher On-Policy Distillation (MOPD)
We introduce **Multi-Teacher On-Policy Distillation (MOPD)**, a new paradigm that formulates knowledge distillation as a reinforcement learning process.
* **Dense Token-Level Guidance**: Unlike methods relying on sparse sequence-level feedback, MOPD utilizes domain-specific expert models (teachers) to provide supervision at every token position.
* **On-Policy Optimization**: The student model learns from its own generated responses rather than a fixed dataset. This eliminates exposure bias and ensures smaller, more stable gradient updates.
* **Inherent Reward Robustness**: Rewards are derived from the distribution divergence between student and teacher, making the process naturally resistant to reward hacking.
We significantly scale up the agentic training environments to improve intelligence and generalization.
* **Massive Code Agent Environments**: We utilize real-world GitHub issues to create over 100,000 verifiable tasks. Our automated pipeline maintains a Kubernetes cluster capable of running over 10,000 concurrent pods with a 70% environment setup success rate.
* **Multimodal Verifier for WebDev**: For web development tasks, we employ a vision-based verifier that evaluates code execution via recorded videos rather than static screenshots. This reduces visual hallucination and ensures functional correctness.
* **Cross-Domain Generalization**: Our experiments show that large-scale RL training on code agents effectively generalizes to other domains, boosting performance in Math and General Agent tasks.
### 5.3 Advanced RL Infrastructure
To support high-throughput RL training for large-scale MoE models, we implemented several infrastructure optimizations on top of SGLang and Megatron-LM.
* **Rollout Routing Replay (R3)**: Addresses numerical precision inconsistencies in MoE routing between inference and training. R3 reuses the exact routed experts from rollout during the training pass, ensuring consistency with negligible overhead.
* **Request-Level Prefix Cache**: In multi-turn agent training, this cache stores KV states and routed experts from prior turns. It avoids re-computation and ensures sampling consistency across turns.
* **Fine-Grained Data Scheduler**: We extend the rollout engine to schedule fine-grained sequences instead of micro-batches. Combined with partial rollout, this significantly reduces GPU idleness caused by long-tail stragglers.
* **Toolbox & Tool Manager**: A two-layer design using Ray actor pools to handle resource contention. It eliminates cold-start delays for tool execution and isolates task logic from system policies.
MiMo-V2-Flash supports FP8 mixed precision inference. We recommend using **SGLang** for optimal performance.
python3 -m sglang.launch_server \
        --model-path XiaomiMiMo/MiMo-V2-Flash \
        --served-model-name mimo-v2-flash \
        --chunked-prefill-size 16384 \
        --speculative-algorithm EAGLE \
        --speculative-num-draft-tokens 4 \
curl -i http://localhost:9001/v1/chat/completions \
    -H 'Content-Type:application/json' \
                "content": "Nice to meet you MiMo"
### Inference with KTransformers (CPU Offloading)
[KTransformers](https://github.com/kvcache-ai/ktransformers) enables efficient MiMo-V2-Flash deployment on consumer-grade hardware by offloading MoE expert computations to CPU, built on top of SGLang. With **4× RTX 5090 + 2× AMD EPYC 9355**, it achieves up to **35.7 tokens/s** decode speed.
For quick start and benchmarks, visit [KTransformers](https://ktransformers.net/zh/benchmarks#MiMo-V2-Flash-FP8-TP4).
> The following system prompts are **HIGHLY** recommended, please choose from English and Chinese version.
You are MiMo, an AI assistant developed by Xiaomi.
Today's date: {date} {week}. Your knowledge cutoff date is December 2024.
你是MiMo（中文名称也是MiMo），是小米公司研发的AI智能助手。
今天的日期：{date} {week}，你的知识截止日期是2024年12月。
> Recommended sampling parameters:
> `temperature=0.8` for math, writing, web-dev
> `temperature=0.3` for agentic taks (e.g., vibe-coding, tool-use)
> In the thinking mode with multi-turn tool calls, the model returns a `reasoning_content` field alongside `tool_calls`. To continue the conversation, the user must persist all history `reasoning_content` in the `messages` array of each subsequent request.
If you find our work helpful, please cite our technical report:
  title={MiMo-V2-Flash Technical Report},
  url={https://github.com/XiaomiMiMo/MiMo-V2-Flash/paper.pdf}
Please contact us at [mimo@xiaomi.com](mailto:mimo@xiaomi.com), join our WeChat group below or open an issue if you have any questions.