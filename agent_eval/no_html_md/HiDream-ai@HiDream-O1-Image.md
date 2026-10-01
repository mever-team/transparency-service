HiDream-O1-Image is a natively unified image generative foundation model built on a Pixel-level Unified Transformer (UiT) without external VAEs or disjoint text encoders, which natively encodes raw pixels, text, and task-specific conditions in a single shared token space — supporting text-to-image, image editing, and subject-driven personalization at up to 2,048 × 2,048.
- 💬 **June 22, 2026:** Join our Discord community for questions, support, and discussions. 
- 🚀 **May 14, 2026:** We open-sourced [**HiDream-O1-Image-Dev-2604**](https://huggingface.co/HiDream-ai/HiDream-O1-Image-Dev-2604) with its [prompt refiner](https://huggingface.co/HiDream-ai/Prompt-Refine), tailored for text-to-image generation task.
- 🛠️ **May 13, 2026:** Inference & pipeline updates — accelerated IP inference; the IP pipeline now supports **layout** and **skeleton** conditioning; updated the Dev editing scheduler. For editing tasks we recommend using the **full** model. PyTorch 2.9.x is not recommended due to the [issue](https://github.com/QwenLM/Qwen3-VL/issues/1811).
- 🤗 **May 10, 2026:** Try **HiDream-O1-Image** online on Hugging Face Spaces — [🤗 HiDream-O1-Image](https://huggingface.co/spaces/HiDream-ai/HiDream-O1-Image) and [🤗 HiDream-O1-Image-Dev](https://huggingface.co/spaces/HiDream-ai/HiDream-O1-Image-Dev).
- 📕 **May 10, 2026:** Our **technical report** is now available — [📑 HiDream-O1-Image.pdf](https://arxiv.org/pdf/2605.11061v1).
- 🚀 **May 8, 2026:** We've open-sourced **HiDream-O1-Image (8B)**, including both the undistilled and distilled Dev variants, together with the Reasoning-Driven Prompt Agent.
> **HiDream-O1-Image-Dev-2604 debuts at #8 in the Artificial Analysis Text to Image Arena, which is positioned to be the new leading open weights Text to Image model.**
Artificial Analysis Text to Image Arena at up to 2,048 × 2,048.
General text-to-image generation at up to 2,048 × 2,048.
Long-text rendering & layout control — accurate, multi-region, multilingual text.
Subject-driven personalization — preserve identity / IP across new scenes.
- 🧬 **Pixel-Level Unified Transformer** — One end-to-end model on raw pixels, no VAE, no disjoint text encoder.
- 🎨 **One Model, Many Tasks** — Text-to-image, long-text rendering, instruction editing, subject-driven personalization, and storyboard generation in a single architecture.
- 🧠 **Reasoning-Driven Prompt Agent** — Built-in "thinking" agent that resolves implicit knowledge, layout, and text rendering before generation.
- 🖼️ **Native High Resolution** — Direct synthesis up to 2,048 × 2,048 with sharp fine-grained detail.
- ⚡ **Exceptional Efficiency and Versatility at 8B Scale** — With only 8B parameters, achieves performance parity with or even surpasses larger open-source DiTs and leading closed-source models.
We benchmark HiDream-O1-Image against state-of-the-art open-source and proprietary models on five widely-used evaluation suites covering compositional generation, dense prompt alignment, human preference, complex visual text generation, and long-text rendering. In each table, the **best** result is highlighted in bold and the second-best is underlined. Click any benchmark below to expand or collapse.
GenEval — compositional generation
DPG-Bench — dense prompt alignment
HPSv3 — human preference across 12 categories
CVTG-2K — complex visual text generation (click to expand)
LongText-Bench — long-text rendering, EN & ZH (click to expand)
git clone https://github.com/HiDream-ai/HiDream-O1-Image.git
2. Install the required dependencies:
pip install -r requirements.txt
> **Note on `flash-attn`.** We highly recommend installing [`flash-attn`](https://github.com/Dao-AILab/flash-attention) for optimized attention computation. **If you do not (or cannot) install `flash-attn`, you must edit `models/pipeline.py` line 341 and change `"use_flash_attn": True` to `"use_flash_attn": False`** — otherwise inference will fail to import the kernel.
## Reasoning-Driven Prompt Agent
HiDream-O1-Image ships with a Reasoning-Driven Prompt Agent (`prompt_agent.py`) that explicitly reasons through layout, subject attributes, physical logic, and text-rendering details, then rewrites a raw user instruction into a self-contained English prompt. It supports two backends — pick one with `--backend`.
The agent prints a JSON object with three fields: `prompt` (rewritten English prompt), `reasoning`, and `resolved_knowledge`. Feed the `prompt` field into `inference.py` for best results on intricate, reasoning-heavy requests.
### Option A — Local Backend (Gemma-4-31B-it)
1. Download the Gemma weights (requires accepting the Gemma license on HuggingFace):
huggingface-cli download google/gemma-4-31B-it --local-dir /path/to/gemma-4-31B-it
    --model_id /path/to/gemma-4-31B-it \
### Option B — External OpenAI-Compatible API
Use any OpenAI-compatible endpoint (OpenAI, Azure, vLLM, SGLang, DeepSeek, etc.) by providing `--base_url`, `--api_key`, and `--model_name`:
    --base_url https://api.openai.com/v1 \
    --model_name deepseek-v4-pro \
A CUDA-capable GPU is required for inference. The examples below use the **undistilled** model (`--model_type full`); see the last subsection for running the same tasks with the **distilled** model (`--model_type dev`).
### 1. Text-to-Image Generation
Generate an image from a text prompt:
    --model_path /path/to/HiDream-O1-Image \
    --prompt "medium shot, eye-level, front view. A woman is seated in an ornate bedroom, illuminated by candlelight, with a calm and composed expression. The subject is a young woman with fair skin, light brown hair styled in an updo with loose tendrils framing her face, and blue eyes. She wears a cream-colored satin robe with delicate floral embroidery and lace trim along the neckline. Her ears are adorned with pearl drop earrings. She is seated on a bed with a dark, intricately carved wooden headboard. To her left, a wooden nightstand holds three lit white candles and a candelabra with multiple lit candles in the background. The bed is covered with patterned pillows and a dark, textured blanket. The walls are paneled with dark wood and feature a large, ornate tapestry with muted earth tones. The lighting creates soft highlights on her face and robe, with warm shadows cast across the room." \
    --output_image results/t2i.png \
### 2. Instruction-Based Image Editing
Provide a single reference image and an editing instruction:
    --model_path /path/to/HiDream-O1-Image \
    --prompt "remove the earphones" \
    --ref_images assets/edit/test.jpg \
    --output_image results/edit.png \
### 3. Multi-Reference Subject-Driven Personalization
Provide two or more reference images that define the subject(s), and a prompt that places them in a new scene:
    --model_path /path/to/HiDream-O1-Image \
    --prompt "A young boy with blonde hair stands on steps wearing light blue jeans, a white t-shirt with logo, and blue and white sneakers. He wears a brown cord necklace with beads, a black wristwatch with digital display, and carries a yellow fanny pack with white zipper. In his hand is a red boxing glove with white top, a teal plastic toy car, and a plastic toy figure of Captain America. He wears a straw hat with cream band. Natural light illuminates the scene." \
    --ref_images assets/IP/1.jpg assets/IP/2.jpg assets/IP/3.jpg assets/IP/4.jpg assets/IP/5.jpg assets/IP/6.jpg assets/IP/7.jpg assets/IP/8.jpg assets/IP/9.jpg assets/IP/10.jpg \
    --output_image results/subject.png
### 4. Multi-Reference Subject-Driven Personalization with Skeleton
    --model_path /path/to/HiDream-O1-Image \
    --prompt "Create a realistic try-on image of the person wearing the provided clothing." \
    --ref_images assets/IP_skeleton/0.face.jpg assets/IP_skeleton/0.bg.jpg assets/IP_skeleton/0.openpose.jpg assets/IP_skeleton/0.part_1.jpg assets/IP_skeleton/0.part_2.jpg assets/IP_skeleton/0.part_3.jpg  \
    --output_image results/subject.png
### 5. Multi-Reference Subject-Driven Personalization with Layout
    --model_path /path/to/HiDream-O1-Image \
    --prompt "City council members pose with relaxed smiles on a sunlit terrace, warm approachable mood, golden hour, cinematic soft glow." \
    --ref_images assets/IP_layout/0.jpg assets/IP_layout/1.jpg \
    --layout_bboxes "[[0.20507812, 0.43945312, 0.48828125, 0.7421875 ], [0.57617188, 0.80078125, 0.08789062, 0.34179688]]" \
    --output_image results/ip_layout.png
### 6. Running with the Dev Model
All three tasks above can be run with the **Dev** model by switching `--model_path` to the Dev checkpoint and setting `--model_type dev`. For example:
    --model_path /path/to/HiDream-O1-Image-Dev \
    --prompt "A dog holds a sign that says \"HiDream-O1-Image release.\"" \
    --output_image results/t2i_dev.png \
For **editing** tasks (exactly one reference image), the Dev model defaults to the `flow_match` scheduler. `flow_match` is recommended for editing tasks. Pass `--editing_scheduler flash` to use the flash scheduler instead. This flag has no effect on the `full` model or on non-editing tasks.
- `--model_path`: Path to the complete HuggingFace model directory (undistilled or distilled).
- `--prompt`: Text prompt for the generation or editing task.
- `--ref_images`: Paths to one or more reference images (optional; space-separated).
- `--output_image`: Path to save the generated image (default: `output.png`).
- `--height` / `--width`: Output image dimensions (default: `2048` × `2048`; values snap to valid resolutions internally).
- `--model_type`: `full` or `dev` (default: `full`). Selects the inference recipe:
  - `full`: 50 steps, guidance scale `5.0`, shift `3.0`, default scheduler.
  - `dev`: 28 steps, guidance scale `0.0`, shift `1.0`, flash scheduler with predefined timesteps. For editing tasks (exactly one reference image), the default scheduler is `flow_match` instead — see `--editing_scheduler`.
- `--seed`: Random seed (default: `32`).
- `--guidance_scale`: Guidance scale (default: `5.0`). Only effective when `--model_type` is `full`.
- `--noise_scale_start`, `--noise_scale_end`: Control the scale of the noise injected by the scheduler at each denoising step; the per-step scale linearly interpolates from `noise_scale_start` (first step) to `noise_scale_end` (last step). See `models/pipeline.py:313` (initial noise) and `models/pipeline.py:323-326` (per-step linear interpolation). Defaults: `7.5`, `7.5`.
- `--noise_clip_std`: Per-step clipping threshold (in units of the injected noise's standard deviation) applied to the noise added during scheduler stepping. See `models/flash_scheduler.py:350-354`. Default: `2.5`.
- `--editing_scheduler`: Scheduler to use for editing tasks (exactly one reference image) when `--model_type dev`. Choices: `flow_match` (default) or `flash`. Ignored for the `full` model and for non-editing tasks.
- `--keep_original_aspect`: When exactly one reference image is provided, resize it with `max_size=2048` and use its dimensions for the target image (preserves the reference's aspect ratio) if `True`. 
`app.py` is a single-file Flask web UI (with HTML / CSS / JS embedded inline) that exposes all generation modes. It also integrates the Reasoning-Driven Prompt Agent.
    --model_path /path/to/HiDream-O1-Image \
Then open `http://localhost:7860` in your browser.
All four CLI arguments above can also be set via environment variables (see `.env.example`): `HIDREAM_MODEL_PATH`, `HIDREAM_MODEL_TYPE`, `HIDREAM_HOST`, and `HIDREAM_PORT`.
The Prompt Agent panel in the Web Demo reads additional environment variables from `.env`:
The sidebar contains a Prompt Agent panel that calls the same Reasoning-Driven Prompt Agent used by `prompt_agent.py`. Select either the *OpenAI-compatible API* backend (any endpoint, key, and model name) or the *Local · Gemma* backend (set `HIDREAM_AGENT_MODEL` in `.env` or the environment to point to your local Gemma-4-31B-it weights).
### Editing Scheduler (Dev model only)
When the server is launched with `--model_type dev`, the **Edit** tab exposes a *Scheduler* dropdown with two options: `flow_match` (default) and `flash`. The selector is hidden for the `full` model and for the Text → Image / Subject tabs, where the scheduler is fixed.
The code in this repository and the HiDream-O1-Image models are licensed under MIT License.
  title={HiDream-O1-Image: A Natively Unified Image Generative Foundation Model with Pixel-level Unified Transformer},
  author={Cai, Qi and Chen, Jingwen and Gao, Chengmin and Gong, Zijian and Li, Yehao and Mei, Tao and Pan, Yingwei and Peng, Yi and Qiu, Zhaofan and Yao, Ting and Yu, Kai and Zhang, Yiheng and others},
  journal={arXiv preprint arXiv:2605.11061},