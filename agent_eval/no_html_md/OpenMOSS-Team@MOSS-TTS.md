MOSS‑TTS Family is an open‑source **speech and sound generation model family** from [MOSI.AI](https://mosi.cn/#hero) and the [OpenMOSS team](https://www.open-moss.com/). It is designed for **high‑fidelity**, **high‑expressiveness**, and **complex real‑world scenarios**, covering stable long‑form speech, multi‑speaker dialogue, voice/character design, environmental sound effects, and real‑time streaming TTS.
When a single piece of audio needs to **sound like a real person**, **pronounce every word accurately**, **switch speaking styles across content**, **remain stable over tens of minutes**, and **support dialogue, role‑play, and real‑time interaction**, a single TTS model is often not enough. The **MOSS‑TTS Family** breaks the workflow into five production‑ready models that can be used independently or composed into a complete pipeline.
- **MOSS‑TTS**: The flagship production model featuring high fidelity and optimal zero-shot voice cloning. It supports **long-speech generation**, **fine-grained control over Pinyin, phonemes, and duration**, as well as **multilingual/code-switched synthesis**.
- **MOSS‑TTSD**: A spoken dialogue generation model for expressive, multi-speaker, and ultra-long dialogues. The new **v1.0 version** achieves **industry-leading performance on objective metrics** and **outperformed top closed-source models like Doubao and Gemini 2.5-pro** in subjective evaluations. You can visit the [MOSS-TTSD repository](https://github.com/OpenMOSS/MOSS-TTSD) for details.
- **MOSS‑VoiceGenerator**: An open-source voice design model capable of generating diverse voices and styles directly from text prompts, **without any reference speech**. It unifies voice design, style control, and synthesis, functioning independently or as a design layer for downstream TTS. Its performance **surpasses other top-tier voice design models in arena ratings**.
- **MOSS‑TTS‑Realtime**: A multi-turn context-aware model for real-time voice agents. It uses incremental synthesis to ensure natural and coherent replies, making it **ideal for building low-latency voice agents when paired with text models**. The TTFB (Time To First Byte) of MOSS-TTS-Realtime reaches 180 ms, and the $T_{\text{LLM-first-sentence}} + T_{\text{MOSS-TTS-Realtime-TTFB}}$ is 377 ms.
- **MOSS‑SoundEffect**: A content creation model specialized in **sound effect generation** with wide category coverage and controllable duration. It generates audio for natural environments, urban scenes, biological sounds, human actions, and musical fragments, suitable for film, games, and interactive experiences.
We train **MossTTSDelay** and **MossTTSLocal** as complementary baselines under one training/evaluation setup: **Delay** emphasizes long-context stability, inference speed, and production readiness, while **Local** emphasizes lightweight flexibility and strong objective performance for streaming-oriented systems. Together they provide reproducible references for deployment and research.
**MossTTSRealtime** is not a third comparison baseline; it is a capability-driven design for voice agents. By modeling multi-turn context from both prior text and user acoustics, it delivers low-latency streaming speech that stays coherent and voice-consistent across turns.
MOSS-TTS, MOSS-TTSD and MOSS-TTS-Realtime currently supports **20 languages**:
**MOSS-TTS** is a next-generation, production-grade TTS foundation model focused on **voice cloning**, **ultra-long stable speech generation**, **token-level duration control**, **multilingual & code-switched synthesis**, and **fine-grained Pinyin/phoneme-level pronunciation control**. It is built on a clean autoregressive discrete-token recipe that emphasizes high-quality audio tokenization, large-scale diverse pre-training data, and efficient discrete token modeling.
### 1.1 TTS Family Positioning
MOSS-TTS is the **flagship base model** in our open-source **TTS Family**. It is designed as a production-ready synthesis backbone that can serve as the primary high-quality engine for scalable voice applications, and as a strong research baseline for controllable TTS and discrete audio token modeling.
- **Production readiness**: robust voice cloning with stable, on-brand speaker identity at scale
- **Controllability**: duration and pronunciation controls that integrate into real workflows
- **Long-form stability**: consistent identity and delivery for extended narration
- **Multilingual coverage**: multilingual and code-switched synthesis as first-class capabilities
MOSS-TTS delivers state-of-the-art quality while providing the fine-grained controllability and long-form stability required for production-grade voice applications, from zero-shot cloning and hour-long narration to token- and phoneme-level control across multilingual and code-switched speech.
* **State-of-the-art evaluation performance** — top-tier objective and subjective results across standard TTS benchmarks and in-house human preference testing, validating both fidelity and naturalness.
* **Zero-shot Voice Cloning (Voice Clone)** — clone a target speaker’s timbre (and part of speaking style) from short reference audio, without speaker-specific fine-tuning.
* **Ultra-long Speech Generation (up to 1 hour)** — support continuous long-form speech generation for up to one hour in a single run, designed for extended narration and long-session content creation.
* **Token-level Duration Control** — control pacing, rhythm, pauses, and speaking rate at token resolution for precise alignment and expressive delivery.
* **Phoneme-level Pronunciation Control** — supports:
  * mixed **Chinese / English / Pinyin / IPA** input in any combination
* **Multilingual support** — high-quality multilingual synthesis with robust generalization across languages and accents.
* **Code-switching** — natural mixed-language generation within a single utterance (e.g., Chinese–English), with smooth transitions, consistent speaker identity, and pronunciation-aware rendering on both sides of the switch.
MOSS-TTS includes **two complementary architectures**, both trained and released to explore different performance/latency tradeoffs and to support downstream research.
**Architecture A: Delay Pattern (MossTTSDelay)**
- Single Transformer backbone with **(n_vq + 1) heads**.
- Uses **delay scheduling** for multi-codebook audio tokens.
- Strong long-context stability, efficient inference, and production-friendly behavior.
**Architecture B: Global Latent + Local Transformer (MossTTSLocal)**
- Backbone produces a **global latent** per time step.
- A lightweight **Local Transformer** emits a token block per step.
- **Streaming-friendly** with simpler alignment (no delay scheduling).
- **Exploration of architectural potential** and validation across multiple generation paradigms.
- **Different tradeoffs**: Delay pattern tends to be faster and more stable for long-form synthesis; Local is smaller and excels on objective benchmarks.
- **Open-source value**: two strong baselines for research, ablation, and downstream innovation.
- **[moss_tts_delay/README.md](https://github.com/OpenMOSS/MOSS-TTS/blob/main/moss_tts_delay/README.md)**
- **[moss_tts_local/README.md](https://github.com/OpenMOSS/MOSS-TTS/tree/main/moss_tts_local)**
**Recommended decoding hyperparameters (per model)**
We recommend a clean, isolated Python environment with **Transformers 5.0.0** to avoid dependency conflicts.
conda create -n moss-tts python=3.12 -y
Install all required dependencies:
git clone https://github.com/OpenMOSS/MOSS-TTS.git
pip install --extra-index-url https://download.pytorch.org/whl/cu128 -e .
#### (Optional) Install FlashAttention 2
For better speed and lower GPU memory usage, you can install FlashAttention 2 if your hardware supports it.
pip install --extra-index-url https://download.pytorch.org/whl/cu128 -e ".[flash-attn]"
If your machine has limited RAM and many CPU cores, you can cap build parallelism:
MAX_JOBS=4 pip install --extra-index-url https://download.pytorch.org/whl/cu128 -e ".[flash-attn]"
- Dependencies are managed in `pyproject.toml`, which currently pins `torch==2.9.1+cu128` and `torchaudio==2.9.1+cu128`.
- If FlashAttention 2 fails to build on your machine, you can skip it and use the default attention backend.
- FlashAttention 2 is only available on supported GPUs and is typically used with `torch.float16` or `torch.bfloat16`.
> Tip: For production usage, prioritize **MossTTSDelay-8B**. The examples below use this model; **MossTTSLocal-1.7B** supports the same API, and a practical walkthrough is available in [moss_tts_local/README.md](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Local-Transformer).
MOSS-TTS provides a convenient `generate` interface for rapid usage. The examples below cover:
1. Direct generation (Chinese / English / Pinyin / IPA)
from transformers import AutoModel, AutoProcessor
# Disable the broken cuDNN SDPA backend
torch.backends.cuda.enable_cudnn_sdp(False)
# Keep these enabled as fallbacks
torch.backends.cuda.enable_flash_sdp(True)
torch.backends.cuda.enable_mem_efficient_sdp(True)
torch.backends.cuda.enable_math_sdp(True)
pretrained_model_name_or_path = "OpenMOSS-Team/MOSS-TTS"
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16 if device == "cuda" else torch.float32
def resolve_attn_implementation() -> str:
    # Prefer FlashAttention 2 when package + device conditions are met.
        and importlib.util.find_spec("flash_attn") is not None
        and dtype in {torch.float16, torch.bfloat16}
        major, _ = torch.cuda.get_device_capability()
    # CUDA fallback: use PyTorch SDPA kernels.
attn_implementation = resolve_attn_implementation()
print(f"[INFO] Using attn_implementation={attn_implementation}")
processor = AutoProcessor.from_pretrained(
    pretrained_model_name_or_path,
processor.audio_tokenizer = processor.audio_tokenizer.to(device)
text_1 = "亲爱的你，\n你好呀。\n\n今天，我想用最认真、最温柔的声音，对你说一些重要的话。\n这些话，像一颗小小的星星，希望能在你的心里慢慢发光。\n\n首先，我想祝你——\n每天都能平平安安、快快乐乐。\n\n希望你早上醒来的时候，\n窗外有光，屋子里很安静，\n你的心是轻轻的，没有着急，也没有害怕。\n\n希望你吃饭的时候胃口很好，\n走路的时候脚步稳稳，\n晚上睡觉的时候，能做一个又一个甜甜的梦。\n\n我希望你能一直保持好奇心。\n对世界充满问题，\n对天空、星星、花草、书本和故事感兴趣。\n当你问“为什么”的时候，\n希望总有人愿意认真地听你说话。\n\n我也希望你学会温柔。\n温柔地对待朋友，\n温柔地对待小动物，\n也温柔地对待自己。\n\n如果有一天你犯了错，\n请不要太快责怪自己，\n因为每一个认真成长的人，\n都会在路上慢慢学会更好的方法。\n\n愿你拥有勇气。\n当你站在陌生的地方时，\n当你第一次举手发言时，\n当你遇到困难、感到害怕的时候，\n希望你能轻轻地告诉自己：\n“我可以试一试。”\n\n就算没有一次成功，也没有关系。\n失败不是坏事，\n它只是告诉你，你正在努力。\n\n我希望你学会分享快乐。\n把开心的事情告诉别人，\n把笑声送给身边的人，\n因为快乐被分享的时候，\n会变得更大、更亮。\n\n如果有一天你感到难过，\n我希望你知道——\n难过并不丢脸，\n哭泣也不是软弱。\n\n愿你能找到一个安全的地方，\n慢慢把心里的话说出来，\n然后再一次抬起头，看见希望。\n\n我还希望你能拥有梦想。\n这个梦想也许很大，\n也许很小，\n也许现在还说不清楚。\n\n没关系。\n梦想会和你一起长大，\n在时间里慢慢变得清楚。\n\n最后，我想送你一个最最重要的祝福：\n\n愿你被世界温柔对待，\n也愿你成为一个温柔的人。\n\n愿你的每一天，\n都值得被记住，\n都值得被珍惜。\n\n亲爱的你，\n请记住，\n你是独一无二的，\n你已经很棒了，\n而你的未来，\n一定会慢慢变得闪闪发光。\n\n祝你健康、勇敢、幸福，\n祝你永远带着笑容向前走。"
text_2 = "We stand on the threshold of the AI era.\nArtificial intelligence is no longer just a concept in laboratories, but is entering every industry, every creative endeavor, and every decision. It has learned to see, hear, speak, and think, and is beginning to become an extension of human capabilities. AI is not about replacing humans, but about amplifying human creativity, making knowledge more equitable, more efficient, and allowing imagination to reach further. A new era, jointly shaped by humans and intelligent systems, has arrived."
text_3 = "nin2 hao3，qing3 wen4 nin2 lai2 zi4 na3 zuo4 cheng2 shi4？"
text_4 = "nin2 hao3，qing4 wen3 nin2 lai2 zi4 na4 zuo3 cheng4 shi3？"
text_5 = "您好，请问您来自哪 zuo4 cheng2 shi4？"
text_6 = "/həloʊ, meɪ aɪ æsk wɪtʃ sɪti juː ɑːr frʌm?/"
# Use audio from ./assets/audio to avoid downloading from the cloud.
ref_audio_1 = "https://speech-demo.oss-cn-shanghai.aliyuncs.com/moss_tts_demo/tts_readme_demo/reference_zh.wav"
ref_audio_2 = "https://speech-demo.oss-cn-shanghai.aliyuncs.com/moss_tts_demo/tts_readme_demo/reference_en.m4a"
    [processor.build_user_message(text=text_1)],
    [processor.build_user_message(text=text_2)],
    [processor.build_user_message(text=text_3)],
    [processor.build_user_message(text=text_4)],
    [processor.build_user_message(text=text_5)],
    [processor.build_user_message(text=text_6)],
    # Voice cloning (with reference)
    [processor.build_user_message(text=text_1, reference=[ref_audio_1])],
    [processor.build_user_message(text=text_2, reference=[ref_audio_2])],
    [processor.build_user_message(text=text_2, tokens=325)],
    [processor.build_user_message(text=text_2, tokens=600)],
model = AutoModel.from_pretrained(
    pretrained_model_name_or_path,
    # If FlashAttention 2 is installed, you can set attn_implementation="flash_attention_2"
    attn_implementation=attn_implementation,
save_dir = Path("inference_root")
save_dir.mkdir(exist_ok=True, parents=True)
    for start in range(0, len(conversations), batch_size):
        batch_conversations = conversations[start : start + batch_size]
        batch = processor(batch_conversations, mode="generation")
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
            attention_mask=attention_mask,
        for message in processor.decode(outputs):
            audio = message.audio_codes_list[0]
            out_path = save_dir / f"sample{sample_idx}.wav"
            torchaudio.save(out_path, audio.unsqueeze(0), processor.model_config.sampling_rate)
### Continuation + Voice Cloning (Prefix Audio + Text)
MOSS-TTS supports continuation-based cloning: provide a prefix audio clip in the assistant message, and make sure the **prefix transcript** is included in the text. The model continues in the same speaker identity and style.
from transformers import AutoModel, AutoProcessor
# Disable the broken cuDNN SDPA backend
torch.backends.cuda.enable_cudnn_sdp(False)
# Keep these enabled as fallbacks
torch.backends.cuda.enable_flash_sdp(True)
torch.backends.cuda.enable_mem_efficient_sdp(True)
torch.backends.cuda.enable_math_sdp(True)
pretrained_model_name_or_path = "OpenMOSS-Team/MOSS-TTS"
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16 if device == "cuda" else torch.float32
def resolve_attn_implementation() -> str:
    # Prefer FlashAttention 2 when package + device conditions are met.
        and importlib.util.find_spec("flash_attn") is not None
        and dtype in {torch.float16, torch.bfloat16}
        major, _ = torch.cuda.get_device_capability()
    # CUDA fallback: use PyTorch SDPA kernels.
attn_implementation = resolve_attn_implementation()
print(f"[INFO] Using attn_implementation={attn_implementation}")
processor = AutoProcessor.from_pretrained(
    pretrained_model_name_or_path,
processor.audio_tokenizer = processor.audio_tokenizer.to(device)
text_1 = "亲爱的你，\n你好呀。\n\n今天，我想用最认真、最温柔的声音，对你说一些重要的话。\n这些话，像一颗小小的星星，希望能在你的心里慢慢发光。\n\n首先，我想祝你——\n每天都能平平安安、快快乐乐。\n\n希望你早上醒来的时候，\n窗外有光，屋子里很安静，\n你的心是轻轻的，没有着急，也没有害怕。\n\n希望你吃饭的时候胃口很好，\n走路的时候脚步稳稳，\n晚上睡觉的时候，能做一个又一个甜甜的梦。\n\n我希望你能一直保持好奇心。\n对世界充满问题，\n对天空、星星、花草、书本和故事感兴趣。\n当你问“为什么”的时候，\n希望总有人愿意认真地听你说话。\n\n我也希望你学会温柔。\n温柔地对待朋友，\n温柔地对待小动物，\n也温柔地对待自己。\n\n如果有一天你犯了错，\n请不要太快责怪自己，\n因为每一个认真成长的人，\n都会在路上慢慢学会更好的方法。\n\n愿你拥有勇气。\n当你站在陌生的地方时，\n当你第一次举手发言时，\n当你遇到困难、感到害怕的时候，\n希望你能轻轻地告诉自己：\n“我可以试一试。”\n\n就算没有一次成功，也没有关系。\n失败不是坏事，\n它只是告诉你，你正在努力。\n\n我希望你学会分享快乐。\n把开心的事情告诉别人，\n把笑声送给身边的人，\n因为快乐被分享的时候，\n会变得更大、更亮。\n\n如果有一天你感到难过，\n我希望你知道——\n难过并不丢脸，\n哭泣也不是软弱。\n\n愿你能找到一个安全的地方，\n慢慢把心里的话说出来，\n然后再一次抬起头，看见希望。\n\n我还希望你能拥有梦想。\n这个梦想也许很大，\n也许很小，\n也许现在还说不清楚。\n\n没关系。\n梦想会和你一起长大，\n在时间里慢慢变得清楚。\n\n最后，我想送你一个最最重要的祝福：\n\n愿你被世界温柔对待，\n也愿你成为一个温柔的人。\n\n愿你的每一天，\n都值得被记住，\n都值得被珍惜。\n\n亲爱的你，\n请记住，\n你是独一无二的，\n你已经很棒了，\n而你的未来，\n一定会慢慢变得闪闪发光。\n\n祝你健康、勇敢、幸福，\n祝你永远带着笑容向前走。"
text_2 = "We stand on the threshold of the AI era.\nArtificial intelligence is no longer just a concept in laboratories, but is entering every industry, every creative endeavor, and every decision. It has learned to see, hear, speak, and think, and is beginning to become an extension of human capabilities. AI is not about replacing humans, but about amplifying human creativity, making knowledge more equitable, more efficient, and allowing imagination to reach further. A new era, jointly shaped by humans and intelligent systems, has arrived."
ref_text_2 = "But I really can't complain about not having a normal college experience to you."
# Use audio from ./assets/audio to avoid downloading from the cloud.
ref_audio_1 = "https://speech-demo.oss-cn-shanghai.aliyuncs.com/moss_tts_demo/tts_readme_demo/reference_zh.wav"
ref_audio_2 = "https://speech-demo.oss-cn-shanghai.aliyuncs.com/moss_tts_demo/tts_readme_demo/reference_en.m4a"
        processor.build_user_message(text=ref_text_1 + text_1),
        processor.build_assistant_message(audio_codes_list=[ref_audio_1])
    # Continuation with voice cloning
        processor.build_user_message(text=ref_text_2 + text_2, reference=[ref_audio_2]),
        processor.build_assistant_message(audio_codes_list=[ref_audio_2])
model = AutoModel.from_pretrained(
    pretrained_model_name_or_path,
    # If FlashAttention 2 is installed, you can set attn_implementation="flash_attention_2"
    attn_implementation=attn_implementation,
save_dir = Path("inference_root")
save_dir.mkdir(exist_ok=True, parents=True)
    for start in range(0, len(conversations), batch_size):
        batch_conversations = conversations[start : start + batch_size]
        batch = processor(batch_conversations, mode="continuation")
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
            attention_mask=attention_mask,
        for message in processor.decode(outputs):
            audio = message.audio_codes_list[0]
            out_path = save_dir / f"sample{sample_idx}.wav"
            torchaudio.save(out_path, audio.unsqueeze(0), processor.model_config.sampling_rate)
### Generation Hyperparameters
> Note: MOSS-TTS is a pretrained base model and is **sensitive to decoding hyperparameters**. See **Released Models** for recommended defaults.
Use tone-numbered Pinyin such as `ni3 hao3 wo3 men1`. You can convert Chinese text with [pypinyin](https://github.com/mozillazg/python-pinyin), then adjust tones for pronunciation control.
from pypinyin import pinyin, Style
def fix_punctuation_spacing(s: str) -> str:
    s = re.sub(rf"\s+([{CN_PUNCT}])", r"\1", s)
    s = re.sub(rf"([{CN_PUNCT}])\s+", r"\1", s)
def zh_to_pinyin_tone3(text: str, strict: bool = True) -> str:
    s = " ".join(item[0] for item in result)
    return fix_punctuation_spacing(s)
text = zh_to_pinyin_tone3("您好，请问您来自哪座城市？")
# Expected: nin2 hao3，qing3 wen4 nin2 lai2 zi4 na3 zuo4 cheng2 shi4？
# Try: nin2 hao3，qing4 wen3 nin2 lai2 zi4 na4 zuo3 cheng4 shi3？
Use `/.../` to wrap IPA sequences so they are distinct from normal text. You can use [DeepPhonemizer](https://github.com/spring-media/DeepPhonemizer) to convert English paragraphs or words into IPA sequences.
from dp.phonemizer import Phonemizer
# Download a phonemizer checkpoint from https://public-asai-dl-models.s3.eu-central-1.amazonaws.com/DeepPhonemizer/en_us_cmudict_ipa_forward.pt
phonemizer = Phonemizer.from_checkpoint(model_path)
english_texts = "Hello, may I ask which city you are from?"
model_input_text = f"/{phoneme_outputs}/"
# Expected: /həloʊ, meɪ aɪ æsk wɪtʃ sɪti juː ɑːr frʌm?/
MOSS-TTS achieved state-of-the-art results on the open-source zero-shot TTS benchmark Seed-TTS-eval, not only surpassing all open-source models but also rivaling the most powerful closed-source models.