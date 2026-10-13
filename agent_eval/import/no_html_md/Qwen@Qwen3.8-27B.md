> This repository contains model weights and configuration files for the post-trained model in the Hugging Face Transformers format. 
> These artifacts are compatible with Hugging Face Transformers, vLLM, SGLang, TokenSpeed, etc.
> For users seeking managed, scalable inference without infrastructure maintenance, the official Qwen API service is provided by [Qwen Cloud](https://www.qwencloud.com).
> In particular, **Qwen3.8-27B** will be available as a hosted version with more production features, e.g., 1M context length by default, official built-in tools. For more information, please refer to the [Qwen3.8-27B Overview](https://www.qwencloud.com/models/qwen3.8-27b). The service is coming soon. Stay tuned for updates.
Following the widespread community adoption of the Qwen3.5 and Qwen3.6 series, we are pleased to introduce Qwen3.8, the most capable generation in the Qwen open-model family to date.
Built on the architectural foundation of Qwen3.5, Qwen3.8 delivers substantial gains across coding, professional work, research, and long-horizon agentic tasks. Qwen3.8-27B brings these advances to a compact, deployment-friendly dense model: a native vision-language model that understands images and videos, with flexible thinking control, designed to carry complex, multi-step tasks through to completion with greater reliability.
Qwen3.8-27B features the following enhancements:
- **Core Capabilities**: Comprehensive improvements across coding, professional work, research, and long-horizon agentic tasks.
- **Agent Execution**: Stronger autonomous planning and better handling of environment feedback, leading to more reliable end-to-end task completion.
- **Downstream Compatibility**: Broader support for popular harnesses and development tools, making it easier to integrate into your existing stack.
- **Flexible Thinking Control**: Thinking mode is on by default and can be disabled per request; reasoning depth can be tuned with `reasoning_effort`, and reasoning context from historical messages is retained via `preserve_thinking`.
- **Vision-Language Understanding**: Native support for image and video understanding, from STEM diagrams and documents to hour-scale videos.
- Type: Causal Language Model with Vision Encoder
- Training Stage: Pre-training & Post-training
    - Token Embedding: 248,320 (Padded)
    - Hidden Layout: 16 × (3 × (Gated DeltaNet → FFN) → 1 × (Gated Attention → FFN))
        - Number of Linear Attention Heads: 48 for V and 16 for QK
        - Number of Attention Heads: 24 for Q and 4 for KV
        - Rotary Position Embedding Dimension: 64
        - Intermediate Dimension: 17,408
    - MTP (Multi-Token Prediction): trained with multiple steps
- Context Length: 262,144 natively and extensible up to 1,000,000 tokens.
Qwen3.8-27BQwen3.6-27BQwen3.7-PlusMuse Glimmer-30BOpus4.6 Max
Agentic terminal codingTerminal Bench 2.1 (Terminus)
Repo-level code generationNL2Repo-Bench
Software engineeringQwenSWEBench
Long-horizon office workCoWorkBench
Professional job tasksJobBench
Frontier agentic tasksAgents' Last Exam
Scientific reasoningGPQA Diamond
Multidisciplinary reasoningHLE
Competitive codingLiveCodeBench v6
SWE-bench Pro: Except for Opus4.6 Max, which uses the officially reported score, all models are evaluated with the Claude Code harness at temp=1.0, top_p=0.95, and a 256K context window. Problematic tasks were corrected, and all baseline models were re-evaluated on the refined benchmark.
NL2Repo-Bench: Evaluated with the Claude Code harness. To prevent reward hacking, we disable Bash commands that attempt to access the specific repository, such as pip download, pip install, and git clone.
DeepSWE 1.1: Evaluated with the Claude Code harness at temp=1.0, top_p=0.95, and a 256K context window.
QwenSWEBench: In-house coding benchmark for evaluating models' software engineering capabilities. Evaluated with the Claude Code harness. Reporting avg@3 with an 8-hour timeout, max_tokens=32,768, temperature=1.0, and a 256K context window.
CoWorkBench: In-house cowork benchmark for evaluating long-horizon tasks across computer science, finance, law, medical, and other productivity domains.
The best result in each row is shown in bold.
Empty cells (--) indicate that results are not yet available or not applicable.
Qwen3.8-27BQwen3.6-27BQwen3.7-PlusMuse Glimmer-30BOpus4.6 Max
Agentic Multimodal Intelligence
Computer useOSWorld-Verified84.363.973.365.972.7
Browser useWebArena-Verified64.848.855.3----
Mobile useAndroidWorld81.970.381.0--62.0
Application recreationRecreationBench47.129.830.2----
Multimodal tool useClawEval-MMPass@357.4Average56.9Pass@342.6Average50.4Pass@357.4Average60.1--Pass@352.5Average54.7
Multimodal software engineeringSWE-MM38.625.730.0--27.1
Visual web developmentVision2Web62.945.042.1----
General Multimodal Intelligence
Visual math problem solvingMathVisionWithout CI90.0With CI94.6Without CI85.1Without CI90.3--Without CI65.5
General visual reasoningBabyVisionWithout CI65.7With CI85.6Without CI28.9Without CI64.7With CI70.4--Without CI12.6
Scientific chart analysisCharXiv (RQ)Without CI83.7With CI90.2Without CI78.4Without CI85.8With CI85.978.8Without CI66.0
Document intelligenceOmniDocBench 1.591.189.491.475.886.6
Real-world perceptionRealWorldQA85.984.186.9--73.9
Embodied intelligenceERQA65.562.569.8--40.8
MathVision, BabyVision, and CharXiv (RQ): Where both settings are available, cells report “Without CI” and “With CI” separately; otherwise, only the available setting is shown. A small number of incorrect ground-truth annotations in MathVision and CharXiv (RQ) were corrected following manual verification, and all reported scores on those benchmarks were computed using the corrected annotations.
MathVision: Qwen3.8-27B is evaluated using the fixed prompt: “Please reason step by step, and put your final answer within \boxed{}.” For the remaining models, we report the higher score from two prompt variants—one with and one without the \boxed{} formatting requirement.
WebArena-Verified: Scores are computed with the official WebArena-Verified grader under the OSWorld scaffold.
RecreationBench: An in-house, long-horizon application-recreation benchmark designed to evaluate hybrid-agent capabilities across five platforms: desktop (Ubuntu, macOS, and Windows), mobile (Android), and the web.
ClawEval-MM: Scores are reported as “Pass@3 / average score.” Pass@3 is the percentage of tasks passed in at least one of three trials; the average score is the mean benchmark score across the three trials.
Vision2Web: Scores are averaged across the frontend, webpage, and website categories. Evaluations use the Claude Code harness and are judged by gpt-5.4-2026-03-05.
SWE-MM: Scores are evaluated on the Claude Code harness using the public dev split of SWE-bench Multimodal, with the modifications described in Appendix 8.3 of the Claude Opus 4.7 system card.
Empty cells (--) indicate that results are not yet available or not applicable.
For streamlined integration, we recommend using Qwen3.8 via APIs.
> Inference efficiency and throughput vary significantly across frameworks. 
> We recommend using the latest framework versions to ensure optimal performance and compatibility.
> For production workloads or high-throughput scenarios, dedicated serving engines such as SGLang, vLLM, or TokenSpeed are recommended.
Qwen3.8 can be deployed with popular inference frameworks, e.g.:
- [SGLang](https://www.sglang.io/): [Qwen3.8 Cookbook](https://docs.sglang.io/cookbook/autoregressive/Qwen/Qwen3.8-27B)
- [vLLM](https://vllm.ai/): [Qwen3.8 Recipe](https://recipes.vllm.ai/Qwen/Qwen3.8-27B)
- [TokenSpeed](https://lightseek.org/tokenspeed/): [Qwen3.8 Recipe](https://lightseek.org/tokenspeed/recipes/models#qwen3-8)
> Qwen3.8 models operate in thinking mode by default, generating thinking content signified by `\n...\n\n` before producing the final response.
> To disable thinking content and obtain a direct response, refer to the examples [here](#instruct-or-non-thinking-mode).
> We recommend using the following sets of sampling parameters for generation:
> - Thinking Mode: `temperature=1.0`, `top_p=0.95`, `top_k=20`, `min_p=0.0`, `presence_penalty=0.0`, `repetition_penalty=1.0`
> - Instruct (or non-thinking) mode: `temperature=0.7`, `top_p=0.80`, `top_k=20`, `min_p=0.0`, `presence_penalty=1.5`, `repetition_penalty=1.0`
> Please note that the support for sampling parameters varies according to inference frameworks.
Qwen3.8 comes with official support for `reasoning_effort`, which can be used to adjust reasoning depth and control cost:  
  - `xhigh` (default): for complex tasks demanding thorough analysis
  - `medium`: balancing accuracy and speed
  - `low`: efficient reasoning optimizing for speed and cost
In addition, `preserve_thinking` is enabled by default for all workloads for the best out-of-the-box experience. To disable preserved thinking, refer to the examples [here](#disable-preserved-thinking).
> In multi-turn agentic tasks, lower reasoning effort does not always reduce overall task completion time. Although it may produce faster per-turn responses, it can also lead to insufficient analysis, more failures, and repeated retries, which may increase total latency and token consumption.
The Chat Completions API can be used with most inference frameworks, as well as [Qwen Cloud](https://www.qwencloud.com/).
Before starting, make sure the OpenAI Python SDK is installed and the API key and the API base URL are configured, e.g.:
# Set the following accordingly
export OPENAI_BASE_URL='your-base-url'
export OPENAI_API_KEY='your-api-key'
# Configured by environment variables
messages = [{"role": "user", "content": "Write a Python function to merge two sorted linked lists."}]
completion = client.chat.completions.create(
            "enable_thinking": True,  # on by default
            "preserve_thinking": True, # on by default
    reasoning_effort="xhigh",  # xhigh by default; supported levels are xhigh, medium, and low
    stream_options={"include_usage": True},
print("\n" + "=" * 20 + "Reasoning" + "=" * 20 + "\n")
    delta = chunk.choices[0].delta
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
            print(delta.reasoning_content, end="", flush=True)
        reasoning_content += delta.reasoning_content
    elif hasattr(delta, "reasoning") and delta.reasoning is not None:
            print(delta.reasoning, end="", flush=True)
        reasoning_content += delta.reasoning
    if hasattr(delta, "content") and delta.content:
            print("\n" + "=" * 20 + "Answer" + "=" * 20 + "\n")
        print(delta.content, end="", flush=True)
        answer_content += delta.content
    "reasoning_content": reasoning_content,
    "reasoning": reasoning_content,
# Configured by environment variables
                    "url": "https://qianwen-res.oss-accelerate.aliyuncs.com/Qwen3.5/demo/CI_Demo/mathv-1327.jpg"
                "text": "The centres of the four illustrated circles are in the corners of the square. The two big circles touch each other and also the two little circles. With which factor do you have to multiply the radii of the little circles to obtain the radius of the big circles?\nChoices:\n(A) $\\frac{2}{9}$\n(B) $\\sqrt{5}$\n(C) $0.8 \\cdot \\pi$\n(D) 2.5\n(E) $1+\\sqrt{2}$"
chat_response = client.chat.completions.create(
print("Chat response:", chat_response)
# Configured by environment variables
                    "url": "https://qianwen-res.oss-accelerate.aliyuncs.com/Qwen3.5/demo/video/N1cdUjctpG8.mp4"
                "text": "How many porcelain jars were discovered in the niches located in the primary chamber of the tomb?"
chat_response = client.chat.completions.create(
# When vLLM is launched with `--media-io-kwargs '{"video": {"num_frames": -1}}'`,
# video frame sampling can be configured via `extra_body` (e.g., by setting `fps`).
# This feature is currently supported only in vLLM.
# By default, `fps=2` and `do_sample_frames=True`.
# With `do_sample_frames=True`, you can customize the `fps` value to set your desired video sampling rate.
# chat_response = client.chat.completions.create(
#     model="Qwen/Qwen3.8-27B",
#         "mm_processor_kwargs": {"fps": 2, "do_sample_frames": True},
print("Chat response:", chat_response)
##### Instruct (or Non-Thinking) Mode
Qwen3.8-27B will think by default before responding.
You can obtain a direct response from the model without thinking by configuring the API parameters. 
# Configured by environment variables
                    "url": "https://qianwen-res.oss-accelerate.aliyuncs.com/Qwen3.5/demo/RealWorld/RealWorld-04.png"
chat_response = client.chat.completions.create(
        "chat_template_kwargs": {"enable_thinking": False},
print("Chat response:", chat_response)
> If you are using APIs from Qwen Cloud, in addition to changing `model`, please use `"enable_thinking": False` instead of `"chat_template_kwargs": {"enable_thinking": False}`.
##### Disable Preserved Thinking
By default, Qwen3.8 retains thinking blocks from all historical messages, maintaining a complete reasoning trace across the conversation. This behavior, known as preserved thinking, ensures full context continuity and is especially beneficial for agent scenarios where decision consistency and reduced redundant reasoning are critical. It also improves KV cache utilization, optimizing inference efficiency in both thinking and non-thinking modes.
If you prefer to retain only the thinking blocks from the latest user message, you can disable this behavior by setting `preserve_thinking` to `False`:
# Configured by environment variables
chat_response = client.chat.completions.create(
        "chat_template_kwargs": {"preserve_thinking": False},
print("Chat response:", chat_response)
> If you are using APIs from Qwen Cloud, in addition to changing `model`, please use `"preserve_thinking": False` directly instead of wrapping it in `chat_template_kwargs`.
To achieve optimal performance, we recommend the following settings:
1. **Sampling Parameters**: We suggest using the following sets of sampling parameters:  
    - Thinking Mode: `temperature=1.0`, `top_p=0.95`, `top_k=20`, `min_p=0.0`, `presence_penalty=0.0`, `repetition_penalty=1.0`
    - Instruct (or non-thinking) mode: `temperature=0.7`, `top_p=0.80`, `top_k=20`, `min_p=0.0`, `presence_penalty=1.5`, `repetition_penalty=1.0`
    For supported frameworks, you can adjust the `presence_penalty` parameter between 0 and 2 to reduce endless repetition. However, using a higher value may occasionally result in language mixing and a slight decrease in model performance.
2. **Adequate Output Length**: To optimize performance on agentic tasks, we recommend allocating sufficient output length to allow the model to generate detailed and comprehensive responses. For frameworks that support separate token limits for internal reasoning and final outputs, we suggest the following configuration within the 1M context length:
    - Reasoning Content: Set the maximum output length to 262,144 tokens.
    - Final Response: Set the maximum output length to 131,072 tokens.
    These settings provide the necessary capacity for complex reasoning while ensuring ample space for high-quality final deliverables.
3. **Processing Ultra-Long Texts**: Qwen3.8-27B natively supports context lengths of up to 262,144 tokens. For long-horizon tasks where the total length (including both input and output) exceeds this limit, we recommend using RoPE scaling techniques to handle long texts effectively, e.g., YaRN.
    YaRN is currently supported by several inference frameworks, e.g., vLLM, SGLang, and TokenSpeed. 
    In general, there are two approaches to enabling YaRN for supported frameworks:
    - Modifying the model configuration file:
        In the `config.json` file, change the `rope_parameters` fields in `text_config` to:
            "partial_rotary_factor": 0.25,
            "original_max_position_embeddings": 262144,
    - Passing command line arguments:
        VLLM_ALLOW_LONG_MAX_MODEL_LEN=1 vllm serve ... --hf-overrides '{"text_config": {"rope_parameters": {"mrope_interleaved": true, "mrope_section": [11, 11, 10], "rope_type": "yarn", "rope_theta": 10000000, "partial_rotary_factor": 0.25, "factor": 4.0, "original_max_position_embeddings": 262144}}}' --max-model-len 1000000  
        SGLANG_ALLOW_OVERWRITE_LONGER_CONTEXT_LEN=1 python -m sglang.launch_server ... --json-model-override-args '{"text_config": {"rope_parameters": {"mrope_interleaved": true, "mrope_section": [11, 11, 10], "rope_type": "yarn", "rope_theta": 10000000, "partial_rotary_factor": 0.25, "factor": 4.0, "original_max_position_embeddings": 262144}}}' --context-length 1000000
        TOKENSPEED_ALLOW_OVERWRITE_LONGER_CONTEXT_LEN=1 tokenspeed serve ... --hf-overrides '{"text_config": {"rope_parameters": {"mrope_interleaved": true, "mrope_section": [11, 11, 10], "rope_type": "yarn", "rope_theta": 10000000, "partial_rotary_factor": 0.25, "factor": 4.0, "original_max_position_embeddings": 262144}}}' --max-model-len 1000000  
    > All the notable open-source frameworks implement static YaRN, which means the scaling factor remains constant regardless of input length, **potentially impacting performance on shorter texts.**
    > We advise modifying the `rope_parameters` configuration only when processing long contexts is required. 
    > It is also recommended to modify the `factor` as needed. For example, if the typical context length for your application is 524,288 tokens, it would be better to set `factor` as 2.0. 
4. **Long Video Understanding**: To optimize inference efficiency for plain text and images, the `size` parameter in the released `video_preprocessor_config.json` is conservatively configured. It is recommended to set the `longest_edge` parameter in the video_preprocessor_config file to 469,762,048 (corresponding to 224k video tokens) to enable higher frame-rate sampling for hour-scale videos and thereby achieve superior performance. For example,
    {"longest_edge": 469762048, "shortest_edge": 4096}
    Alternatively, override the default values via engine startup parameters. For implementation details, refer to: [vLLM](https://github.com/vllm-project/vllm/pull/34330) / [SGLang](https://github.com/sgl-project/sglang/pull/18467).
If you find our work helpful, feel free to give us a cite.
    title = {{Qwen3.8-Max}: A New Bar for Coding and Cowork},
    url = {https://qwen.ai/blog?id=qwen3.8},