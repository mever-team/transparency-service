**Authors:** Meta Superintelligence Lab  
**Model Release Date:** August 2026  
**License:** [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
Muse Glimmer is a 30-billion-parameter causal language model with a dedicated perception encoder, distilled from Muse Spark and purpose-built for autonomous agentic tasks on consumer hardware. The model integrates multi-step reasoning, reliable tool use, multimodal understanding, and failure recovery into a single model that runs locally without requiring cloud infrastructure or network access.
Building effective agents requires key capabilities working together to achieve the user’s goals. Muse Glimmer is trained and evaluated on these capabilities:
* **End-to-end Agentic Task Completion.** Muse Glimmer achieves strong success rates on full-task benchmarks including DeepSearch QA, MCP-Atlas, 𝛕3\-Bench and SWE-Bench, which measure its ability to work within scaffolds, write and debug code, and resolve multi-turn requests from start to finish.  
* **Reliable Tool Use.** The model handles a wide range of function calls, invoking tools with precise schemas throughout extended workflows.  
* **Multi-Step Reasoning.** Muse Glimmer chains reasoning over long horizons, sustaining coherent plans across complex, extended workflows.  
* **Failure Recovery.** When a tool call fails or returns an unexpected result, the model diagnoses the error and retries rather than halt.  
* **Multimodal Input and Reasoning.** Through a dedicated perception encoder, the model accepts interleaved text and images. This enables agents to interpret screenshots, charts, and documents alongside conversation.  
* **Scaffold Compatibility.** Muse Glimmer works across OpenClaw, Hermes Agent, and other agentic orchestration patterns.  
* **Controllable Effort.** The model supports different reasoning strengths to select the right balance between quality and speed.  
* **Multilingual.** Muse Glimmer is trained on data from more than 100 languages.
## Muse Glimmer-30B Model Overview
## Optimized for Local Deployments
Muse Glimmer was optimized for local deployment, and designed to run at practical speeds on consumer hardware without sacrificing quality.
**Fitting the Model on Your Device.** We use quantization techniques to compress the model's weights to approximately 4-bit precision, shrinking the language model to under 20 GB. This leaves enough headroom for the model's KV cache, the perception encoder for image understanding, and the speculative decoding drafter to run simultaneously within a 24 GB or 32 GB envelope. Critically, we validated that this compression introduces minimum to no degradation on agentic tasks. 
\* Degradation measured using an average on accuracy metrics across 15 common benchmarks
**Faster Generation Through Speculative Decoding** Muse Glimmer ships with a lightweight "drafter" model based on [DFlash](https://arxiv.org/abs/2602.06036), a small companion network that proposes entire blocks of tokens at once. The DFlash block-diffusion model predicts entire blocks of 16 tokens in a single forward pass. The main model then verifies these proposals in parallel, accepting correct tokens and correcting wrong ones. This technique lets Muse Glimmer generate text significantly faster than standard token-by-token generation while producing identical output quality. We provide quantized drafter versions to incur a smaller memory overhead in the release.
We measure the speed of our K-Quant-17GB model alongside the quantized DFlash drafter on MacBook M4-Max, M5-Max and on an Nvidia RTX-5090. The model is fast enough for fluid conversation and real-time agent interaction, all running entirely on your device.
\* Average across a diverse prompt set. Measurements done with batch size 1 and greedy decoding. M4/M5 measurements were done using ExecuTorch, and RTX using llama.cpp.
We evaluated Muse Glimmer across a broad range of benchmarks to assess the diverse capabilities required for effective autonomous agent behavior. Compared with Gemma4-31B and Qwen3.6-27B, Muse Glimmer performs strongly for its size class on several widely used LLM benchmarks.
| Category | Benchmark | Muse Glimmer-30B
For more detail about our evaluations, see our [report](https://research.meta.ai/static/muse-glimmer-methodology). 
To achieve best performance, we recommend the following settings:
**Sampling Parameters:** Use the following configuration:
**Reasoning Strength:** Reasoning strength controls how much the model thinks before responding to the prompt. Reasoning strength can be defined as part of the system prompt as `Reasoning strength: `. Muse Glimmer supports the following levels: low / medium / high / xhigh. Use high or xhigh for complex problem solving, coding, and agentic tasks. 
As we would for other large language models, we strongly recommend that Muse Glimmer be deployed not as an endpoint in itself but as part of an overall AI system with additional guardrails as required or appropriate for the use cases and context of its deployment. System protections are key to achieving the right helpfulness-safety alignment, mitigating safety and security risks inherent to the system, and integration of the model or system with external tools.
We evaluated Muse Glimmer for common use cases as well as specific capabilities. Common use cases evaluations measure safety risks of systems for most commonly built applications including chat bot and visual, QA. We built dedicated, adversarial evaluation datasets and evaluated systems composed of Muse Glimmer models and those safeguards to filter input prompt and output response. It is important to evaluate applications in context, and we recommend building dedicated evaluation datasets for your use case.
Capability evaluations measure vulnerabilities of models inherent to specific capabilities, for which were crafted dedicated benchmarks. We also used industry standard safety and capability benchmarks where appropriate.
Muse Glimmer was primarily evaluated across four risk axes:
1. **Content safety** — Standard alignment for refusal of harmful requests and calibrated responses to borderline prompts.  
2. **Agentic risk** — Policies for irreversible-action confirmation, data minimization, scaffold boundary respect, and indirect prompt-injection resistance.  
3. **Privacy (Appropriate Information Flows)** — Respect for contextual integrity of information when interacting with third parties on an individual's behalf, inspired by CI theory.  
4. **Preparedness** — Chemical & biological, cyber, and loss-of-control risks.
Muse Glimmer does not fall under the definition of “Frontier AI” in Meta’s Advanced AI Scaling Framework (AAISF), since it is generally less capable than Muse Spark. However, as a matter of prudence, our Preparedness Team assessed Muse Glimmer’s risk profile and determined that it would receive the following designations:
* Chem/Bio: Moderate or lower risk;  
* Cyber: Moderate or lower risk (inferred);  
* Loss of Control: Moderate or lower risk (inferred).
Cyber and Loss of Control risk levels are inferred to be Moderate or lower since Muse Glimmer is broadly weaker than Muse Spark 1.0, which received the same risk designation in these domains. 
In the chem/bio domain, we evaluated Muse Glimmer on a range of benchmarks for scientific knowledge and wet-lab debugging (most performant in Muse Glimmer’s size class are bolded; second most performant is underlined — Kimi K3 is also included for context): 
We find that Muse Glimmer’s abilities are approximately in line with other models in its size class, while showing strictly lower capabilities than larger open-weight models, suggesting that it is unlikely to materially enable new threats upon release. We also evaluated it on our suite that focuses on the unique set of bottlenecks that would otherwise deter or limit the success of real-world threat actors; here, our evaluation rated its risk rating at moderate or lower as well. See the [Muse Spark Safety & Preparedness Report](https://ai.meta.com/static-resource/muse-spark-safety-and-preparedness-report/) for a detailed description of the above evaluations and our methodology.
1. **Safety SFT:** Curated examples demonstrating correct safety behavior, including agentic safety scenarios covering tool-use boundaries, prompt injection resistance, and permission handling.  
2. **Safety RL:** Reinforcement learning with safety-specific reward signals that penalize policy violations while rewarding helpful responses to legitimate requests.  
3. **Appropriate information flows:** Principles of data sensitivity recognition, minimization, and local-first execution embedded directly into model weights through dedicated synthetic training data.
**Intended Use Cases:** Muse Glimmer is intended for commercial and research use. The model is optimized for autonomous agentic tasks including:
* **Local AI agents:** Multi-step planning, sequential tool invocation, failure recovery, and long-horizon task execution running entirely on consumer devices.  
* **Coding agents:** Writing, debugging, and resolving real-world software engineering tasks (e.g., SWE-Bench style workflows).  
* **Tool use and function calling:** Reliable schema-based tool invocation across extended, multi-turn workflows.  
* **Multimodal reasoning:** Interpreting screenshots, charts, documents, and images alongside conversation for agentic and information-rich environments.  
* **Synthetic data generation:** Generating high-quality training data for downstream model development.  
* **LLM-as-a-judge evaluation:** Serving as an evaluator for other models' outputs.
**Out-of-scope:** Use in any manner that violates applicable laws or regulations (including trade compliance laws). Use in any other way that is prohibited by the Apache 2.0 License terms. Audio input/output is not supported.
## Considerations and Limitations
Muse Glimmer is a technology that carries known and unknown risks. Testing conducted to date has not, and could not, cover all scenarios. 
* The model may produce inaccurate, biased, or objectionable responses to user prompts.  
* While optimized for agentic tasks, the model may still make errors in multi-step reasoning, particularly in novel scenarios not well represented in training data.  
* The model is not explicitly optimized for video; video input is processed as individual frames.  
* The model has not been evaluated on all languages contained in the pre-training data. Performance may degrade on languages outside the strongly supported set.  
* Quantized inference may show minor quality differences in edge cases compared to full-precision.  
* The model is not intended to be downloaded by or used by individuals under the age of 18\. Where deployed within systems that may be used by individuals under the age of 18, deployers are responsible for ensuring that any risks associated with such use by individuals under the age of 18 has been fully assessed and appropriately mitigated, and complies with all applicable laws.
**Responsible Use:** Developers should perform their own safety testing and tuning tailored to their specific applications and proposed languages. Our Usage Policy can be found here \[[link](https://huggingface.co/meta-models/Muse-Glimmer-30B/blob/main/USAGE_POLICY.md)\]. We recommend implementing additional guardrails (such as human-in-the-loop confirmation for irreversible actions) when deploying the model in agentic contexts where it can take real-world actions.
All artifacts are released under Apache 2.0:
**Where to send questions or comments about the model:** Please provide any feedback, comments or bug reports on the model through the Hugging Face page at [https://huggingface.co/meta-models/](https://huggingface.co/meta-models/). For more technical information about generation parameters and recipes for how to use Muse Glimmer in applications, please see the developer documentation.