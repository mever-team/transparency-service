We introduce LongCat-Flash, a powerful and efficient language model with 560 billion total parameters, featuring an innovative Mixture-of-Experts (MoE) architecture. The model incorporates a dynamic computation mechanism that activates 18.6B∼31.3B parameters (averaging∼27B) based on contextual demands, optimizing both computational efficiency and performance. To achieve advanced training and inference efficiency, we employ a shortcut-connected architecture that expands computation-communication overlap window, achieving over 100 tokens per second (TPS) for inference cost-effectively. Our comprehensive training and scaling strategies ensure stable, efficient training, while tailored data strategies enhance model performance. 
Now we release LongCat-Flash-Chat, a non-thinking foundation model that delivers highly competitive performance among leading models, with exceptional strengths in agentic tasks.
#### 🌟 Scalable Architectural Design for Computational Efficiency
LongCat-Flash is designed and optimized under two key principles: efficient computation utilization, as well as  efficient training and inference. Specifically, (1) As not all tokens are equal, we introduce the zero-computation experts mechanism in MoE blocks to allocate a dynamic computation budget to important tokens based on their significance, i.e., activating 18.6 to 31.3 billion parameters (out of 560 billion total) based on contextual demands. To ensure consistent computation load, we employ expert bias adjusted by a PID-controller, maintaining an average of∼27 billion activated parameters per token. (2) As communication overhead becomes a bottleneck during MoE model scaling, we incorporate the Shortcut-connected MoE (ScMoE) design to expand the computation-communication overlap window. Combined with customized infrastructure optimizations, this design enables training at a massive scale of over tens of thousands accelerators and inference with high throughput and low latency.
#### 🌟 Effective Model Scaling Strategy
Effectively and efficiently scaling model size remains a key challenge in strategy design. To this end, we develop a comprehensive stability-and-scaling framework for robustly training large-scale models: (1) We successfully apply a hyperparameter transfer strategy to such a large model, predicting optimal hyperparameter configurations by leveraging results from smaller proxy models with theoretical guarantees. (2) We initialize the model using a model-growth mechanism based on a refined half-scale checkpoint, achieving improved performance compared to conventional initialization methods. (3) A multi-pronged stability suite incorporates principled router-gradient balancing, a hidden z-loss to suppress massive activations, and fine-tuned optimizer configurations. (4) To enhance the reliability of large-scale cluster training, we introduce deterministic computation. This guarantees the exact reproducibility of experiments and enables the detection of SDC (Silent Data Corruption) during the training process. These interventions ensure that LongCat-Flash ’s training remains stable, with no irrecoverable loss spikes.
#### 🌟 Multi-Stage Training Pipeline for Agentic Capability
Through a meticulously designed pipeline, LongCat-Flash is endowed with advanced agentic behaviors. Initial efforts focus on constructing a more suitable base model for agentic post-training, where we design a two-stage pretraining data fusion strategy to concentrate reasoning-intensive domain data. During mid-training, we enhance reasoning and coding capabilities while extending the context length to 128k to meet agentic post-training requirements. Building on this advanced base model, we proceed with a multi-stage post-training. Recognizing the scarcity of high-quality, high-difficulty training problems for agentic tasks, we design a multi-agent synthesis framework that defines task difficulty across three axes, i.e., information processing, tool-set complexity, and user interaction—using specialized controllers to generate complex tasks requiring iterative reasoning and environmental interaction.
For more detail, please refer to the comprehensive [***LongCat-Flash Technical Report***](https://github.com/meituan-longcat/LongCat-Flash-Chat/blob/main/tech_report.pdf).
* Values marked with `*` are sourced from other public reports. 
* DeepSeek-V3.1, Qwen3-235B-A22B, Gemini2.5-Flash, and Claude4-Sonnet are evaluated under their non-thinking mode.
The details of our chat template are provided in the `tokenizer_config.json` file. Below are some examples.
With the following prefix, LongCat-Flash can generate responses corresponding to user queries:
[Round 0] USER:{query} ASSISTANT:
When a system prompt is specified, the prefix will take the following format:
SYSTEM:{system_prompt} [Round 0] USER:{query} ASSISTANT:
In multi-turn scenarios, the prefix is constructed by concatenating the context with the latest user query:
SYSTEM:{system_prompt} [Round 0] USER:{query} ASSISTANT:{response}... [Round N-1] USER:{query} ASSISTANT:{response} [Round N] USER:{query} ASSISTANT:
Here, N denotes the N-th round of user queries, with indexing starting from zero.
LongCat-Flash supports tool calling in the following format:
SYSTEM:{system_prompt} [Round 0] USER:{query} ASSISTANT:
You have access to the following tools: 
Description: {func.description}
{json.dumps(func.parameters, indent=2)}
**Note**: For each function call, return a json object with function name and arguments within  XML tags as follows:
When multiple functions need to be called simultaneously, each function call should be wrapped in its own  tag and placed consecutively. For example:
We have implemented basic adaptations in both SGLang and vLLM to support the deployment of LongCat-Flash. For comprehensive guidance, please refer to the [Deployment Guide](https://github.com/meituan-longcat/LongCat-Flash-Chat/blob/main/docs/deployment_guide.md) in the LongCat-Flash-Chat repository.
You can chat with LongCat-Flash on our official website: [https://longcat.ai](https://longcat.ai).
This repository, including both the model weights and the source code, is released under the **MIT License**. 
Any contributions to this repository are licensed under the MIT License, unless otherwise stated. This license does not grant any rights to use Meituan trademarks or patents. 
For details, see the [LICENSE](./LICENSE) file. 
This model has not been specifically designed or comprehensively evaluated for every possible downstream application. 
Developers should take into account the known limitations of large language models, including performance variations across different languages, and carefully assess accuracy, safety, and fairness before deploying the model in sensitive or high-risk scenarios. 
It is the responsibility of developers and downstream users to understand and comply with all applicable laws and regulations relevant to their use case, including but not limited to data protection, privacy, and content safety requirements. 
Nothing in this Model Card should be interpreted as altering or restricting the terms of the MIT License under which the model is released. 
We kindly encourage citation of our work if you find it useful.
@misc{meituan2025longcatflashtechnicalreport, 
    title={LongCat-Flash Technical Report}, 
    author={Meituan LongCat Team}, 
    url={https://arxiv.org/abs/2509.01322}, 
Please contact us at longcat-team@meituan.com or open an issue if you have any questions.