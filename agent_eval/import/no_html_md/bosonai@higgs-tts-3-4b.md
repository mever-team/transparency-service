Higgs TTS 3 is built for voice chat: it **speaks, not just reads**. It turns model responses into expressive conversational speech across **100+ languages**, with **zero-shot voice cloning** and **inline control** over emotion, style, prosody, pauses, and sound effects.
> Released for research and non-commercial use under the **Boson Higgs TTS 3 Research and Non-Commercial License**. Production, hosted APIs, embedding in a product/service, or reselling the model requires a separate commercial license. Prohibited: voice cloning without consent, impersonation, fraud, election deception, biometric surveillance, or any unlawful use.
> **Free for digital creators — including monetized content.** Under the license's **Creator Use Grant**, creators may use Higgs TTS 3 to make and monetize podcasts, videos, and social posts for free. The one requirement is to credit *Boson AI's Higgs Audio* — either in the audio or prominently in the accompanying text (e.g., the video description or show notes). Suggested credit: *"This audio was created with Boson AI's Higgs Audio — https://www.boson.ai/higgs-audio"*. See the [Creator Use](#creator-use-free-for-digital-creators) section below.
![Higgs TTS 3 Architecture](./assets/model_architecture.png)
Higgs autoregressive decoder consumes interleaved text and audio tokens. Audio is encoded by the **Higgs Tokenizer** into 8 codebooks at 25 fps, staggered via a **delay pattern**, then mapped to backbone hidden states through a **multi-codebook fused embedding**. Output codes pass through a **multi-codebook fused head**, are de-delayed, and decoded back to waveform.
The model reaches **single-digit WER/CER on 102 languages**, which split into two tiers.
### WER/CER under 5 — polished, production-quality (85)
🇿🇦 Afrikaans · 🇸🇦🇪🇬 Arabic · 🇦🇲 Armenian · 🇮🇳 Assamese · 🇪🇸 Asturian · 🇦🇿 Azerbaijani · 🇷🇺 Bashkir · 🇪🇸 Basque · 🇧🇾 Belarusian · 🇧🇩🇮🇳 Bengali · 🇧🇦 Bosnian · 🇧🇬 Bulgarian · 🇪🇸 Catalan · 🇵🇭 Cebuano · 🇮🇶 Central Kurdish · 🇨🇳 Chinese · 🇭🇷 Croatian · 🇨🇿 Czech · 🇩🇰 Danish · 🇳🇱🇧🇪 Dutch · 🇷🇺 Eastern Mari · 🇺🇸🇬🇧🇦🇺 English · 🌐 Esperanto · 🇪🇪 Estonian · 🇫🇮 Finnish · 🇫🇷🇨🇦 French · 🇪🇸 Galician · 🇬🇪 Georgian · 🇩🇪🇦🇹 German · 🇬🇷 Greek · 🇮🇳 Gujarati · 🇭🇹 Haitian Creole · 🇳🇬 Hausa · 🇮🇱 Hebrew · 🇮🇳 Hindi · 🇭🇺 Hungarian · 🇮🇩 Indonesian · 🇮🇹 Italian  · 🇯🇵 Japanese · 🇮🇩 Javanese · 🇮🇳 Kannada · 🇰🇿 Kazakh · 🇰🇷 Korean · 🇷🇼 Kinyarwanda · 🇰🇬 Kyrgyz · 🇱🇻 Latvian · 🇨🇩 Lingala · 🇱🇹 Lithuanian · 🇰🇪 Luo · 🇲🇰 Macedonian · 🇲🇾🇮🇩 Malay · 🇮🇳 Malayalam · 🇲🇹 Maltese · 🇳🇿 Māori · 🇮🇳 Marathi · 🇲🇳 Mongolian · 🇳🇵 Nepali · 🇳🇴 Norwegian · 🇫🇷 Occitan · 🇮🇷🇦🇫 Persian · 🇵🇱 Polish · 🇵🇹🇧🇷 Portuguese · 🇷🇴 Romanian · 🇷🇺 Russian · 🇿🇦 Sepedi · 🇷🇸 Serbian · 🇿🇼 Shona · 🇸🇰 Slovak · 🇸🇮 Slovene · 🇪🇸🇲🇽 Spanish · 🇹🇿🇰🇪 Swahili · 🇸🇪 Swedish · 🇵🇭 Tagalog · 🇹🇯 Tajik · 🇮🇳🇱🇰 Tamil · 🇮🇳 Telugu · 🇹🇭 Thai · 🇹🇷 Turkish · 🇺🇦 Ukrainian · 🇵🇰🇮🇳 Urdu · 🇨🇳 Uyghur · 🇺🇿 Uzbek · 🇻🇳 Vietnamese · 🇿🇦 Xhosa · 🇿🇦 Zulu
### WER/CER between 5 and 10 — usable, but less polished (17)
🇦🇱 Albanian · 🇲🇼🇿🇲 Chichewa/Nyanja · 🇮🇳🇵🇰 Eastern Punjabi · 🇺🇬 Ganda · 🇮🇸 Icelandic · 🇮🇪 Irish · 🇩🇿 Kabyle · 🇨🇻 Kabuverdianu · 🇰🇪 Kamba · 🇻🇦 Latin · 🇱🇺 Luxembourgish · 🇪🇹🇰🇪 Oromo · 🇦🇫🇵🇰 Pashto · 🇵🇰🇮🇳 Sindhi · 🇸🇴 Somali · 🇦🇴 Umbundu · 🇬🇧 Welsh
All tags follow `<|category:value|>` syntax and can be inserted mid-utterance.
> For how to place these tags when writing the target text (sentence-level vs. inline, `sfx` formatting, stacking, worked examples), see **[PROMPTING.md](./PROMPTING.md)**.
- **Emotion** — `elation`, `amusement`, `enthusiasm`, `determination`, `pride`, `contentment`, `affection`, `relief`, `contemplation`, `confusion`, `surprise`, `awe`, `longing`, `arousal`, `anger`, `fear`, `disgust`, `bitterness`, `sadness`, `shame`, `helplessness`
  Token Description   <|emotion:elation|>Elation / joy <|emotion:amusement|>Amusement / playful laughter <|emotion:enthusiasm|>Enthusiasm / excitement <|emotion:determination|>Determination / firmness <|emotion:pride|>Pride / confidence <|emotion:contentment|>Calm satisfaction <|emotion:affection|>Warmth / affection <|emotion:relief|>Relief <|emotion:contemplation|>Thoughtful / reflective <|emotion:confusion|>Confused <|emotion:surprise|>Surprised <|emotion:awe|>Awe / wonder <|emotion:longing|>Longing / yearning <|emotion:arousal|>Heightened desire <|emotion:anger|>Anger <|emotion:fear|>Fear <|emotion:disgust|>Disgust <|emotion:bitterness|>Bitterness <|emotion:sadness|>Sadness <|emotion:shame|>Shame <|emotion:helplessness|>Helplessness  
- **Style** — `singing`, `shouting`, `whispering`
  Token Description   <|style:singing|>Singing <|style:shouting|>Shouting / projected voice <|style:whispering|>Whisper  
- **Sound effects** — `cough`, `laughter`, `crying`, `screaming`, `burping`, `humming`, `sigh`, `sniff`, `sneeze`
Pair each token with the matching onomatopoeia immediately after it.
  Token Description Suggested onomatopoeia   <|sfx:cough|>CoughAhem <|sfx:laughter|>LaughterHaha / Hehe <|sfx:crying|>CryingBoohoo / Sob <|sfx:screaming|>ScreamingAhh / Aaah <|sfx:burping|>BurpingBurp <|sfx:humming|>HummingHmm / Mmm <|sfx:sigh|>SighUh / Ahh <|sfx:sniff|>SniffSff <|sfx:sneeze|>SneezeAchoo  
  - Speed — `speed_very_slow`, `speed_slow`, `speed_fast`, `speed_very_fast`
  - Pauses — `pause`, `long_pause`
  - Pitch — `pitch_low`, `pitch_high`
  - Delivery — `expressive_high`, `expressive_low`
  Token Effect   <|prosody:speed_very_slow|>≈0.65× speed <|prosody:speed_slow|>≈0.85× speed <|prosody:speed_fast|>≈1.2× speed <|prosody:speed_very_fast|>≈1.4× speed <|prosody:pitch_low|>≈−3 semitones <|prosody:pitch_high|>≈+2.5 semitones <|prosody:pause|>≈400–700 ms pause <|prosody:long_pause|>≈700–1500 ms pause <|prosody:expressive_high|>More expressive delivery <|prosody:expressive_low|>Flatter delivery  
We evaluate Higgs TTS 3 on public multilingual TTS suites and our internal 111-language Higgs-Multilingual set, covering both common and lower-resource languages.
WER / CER (↓, ×100) macro-averaged across each benchmark's language set. Lower is better; **bold** marks the best per row. All numbers are reproducible end-to-end with original metrics and normalization.
Win-rate (↑) per category — judge preference vs the BASELINE row; **bold** marks the highest win-rate per column. For a fair comparison, every model shares the same reference audio per prompt, and we run the benchmark text verbatim — no inline control tags inserted.
Pair the weights in this repo with [**SGLang-Omni**](https://github.com/sgl-project/sglang-omni) — a production serving stack with continuous batching for multi-codebook decoding and the same inline tag controls. The Higgs TTS cookbook walks you through installation, server launch, request examples, and the full API reference.
See the [Higgs TTS cookbook](https://sgl-project.github.io/sglang-omni/cookbook/higgs_tts.html) for the full details.
docker pull lmsysorg/sglang-omni:dev
docker run -it --gpus all --shm-size 32g --ipc host --network host --privileged \
  lmsysorg/sglang-omni:dev /bin/zsh
git clone git@github.com:sgl-project/sglang-omni.git && cd sglang-omni
uv venv .venv -p 3.12 && source .venv/bin/activate
export HF_TOKEN=hf_xxxxxxxxxxxxxxxx
hf download bosonai/higgs-tts-3-4b
  --model-path bosonai/higgs-tts-3-4b \
curl -X POST http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello, how are you?"}' \
Supplying the reference transcript (`text`) materially improves cloning fidelity.
    "http://localhost:8000/v1/audio/speech",
        "input": "Have a nice day and enjoy south california sunshine.",
            "text": "Hey, Adam here. Let's create something that feels real, sounds human, and connects every time.",
        "temperature": 0.8, "top_k": 50, "max_new_tokens": 1024,
with open("output.wav", "wb") as f:
#### Streaming (Server-Sent Events)
Set `"stream": true` to receive base64-encoded WAV chunks as the vocoder emits them — sub-second time-to-first-audio. Each event carries `audio.data` (base64 WAV bytes); the terminal event has `finish_reason: "stop"` plus usage metadata.
    "http://localhost:8000/v1/audio/speech",
    json={"input": "Get the trust fund to the bank early.", "stream": True},
) as resp, open("output.wav", "wb") as f:
    for line in resp.iter_lines():
        if not line or not line.startswith(b"data: ") or line == b"data: [DONE]":
        if event.get("finish_reason") == "stop":
        audio = event.get("audio") or {}
            f.write(base64.b64decode(audio["data"]))
Embed `<|emotion:…|>`, `<|style:…|>`, `<|prosody:…|>`, and `<|sfx:…|>` tokens directly in `input`. Two rules:
1. **Delivery tokens first.** Emotion, style, and the prosody *speed / pitch / expressive* tokens shape the whole turn — put them at the start of `input`. Positional tokens (`<|prosody:pause|>`, `<|prosody:long_pause|>`, `<|sfx:…|>`) go inline exactly where they fire.
2. **Pair every `<|sfx:…|>` with its onomatopoeia.** E.g. `<|sfx:laughter|>Haha`, `<|sfx:sigh|>Uh`, `<|sfx:sneeze|>Achoo`. The written sound gives the model the acoustic cue to realize the effect.
Example — amusement + laughter:
curl -X POST http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input": "<|emotion:amusement|><|prosody:expressive_high|>Wait, wait, that was kind of hilarious. <|sfx:laughter|>Hehe, no, seriously, I was not ready for that."}' \
Throughput on Seed-TTS EN (full set, **N=1088** per run). Client `--max-concurrency` sweep against a Higgs server (`max_running_requests=16`, bf16, CUDA Graph on). Each row is the **mean of 3 runs**. Hardware: **1× H100**.
- **Concurrency** — Maximum number of in-flight client requests (`--max-concurrency`).
- **Throughput (req/s)** — Completed requests divided by total benchmark wall-clock time.
- **Mean latency** — Average end-to-end time per request (send to full response received).
- **RTF (per-req)** — Average ratio of processing time to generated audio duration per request (<1 is faster than real time).
- **audio_s/s** — Total seconds of audio produced divided by total benchmark wall-clock time.
To reproduce the results, follow the instructions in [this script](https://github.com/sgl-project/sglang-omni/blob/main/benchmarks/eval/benchmark_tts_seedtts.py).
You can also serve these weights with [**vLLM-Omni**](https://github.com/vllm-project/vllm-omni), which exposes the same OpenAI-compatible `/v1/audio/speech` API with zero-shot voice cloning.
hf download bosonai/higgs-tts-3-4b
vllm-omni serve bosonai/higgs-tts-3-4b \
curl -X POST http://localhost:8095/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"model": "bosonai/higgs-tts-3-4b", "input": "Hello, how are you?"}' \
Plain-text TTS, voice-clone, and benchmark recipes are in the [vLLM-Omni Higgs TTS 3 recipe](https://github.com/vllm-project/vllm-omni/blob/main/recipes/BosonAI/Higgs-Audio-V3-TTS.md).
For zero-ops deployment, use the [**Boson AI API**](https://docs.boson.ai/models/higgs-audio-tts/overview).
@misc{bosonai_higgs_audio_tts_v3_2026,
  title  = {Higgs TTS 3: Conversational Speech for Voice AI from Boson AI},
  howpublished = {https://huggingface.co/bosonai/higgs-tts-3-4b},
## Creator Use (Free for Digital Creators)
In addition to research and non-commercial use, the license includes a **Creator Use Grant** that lets **digital creators** use Higgs TTS 3 to produce creative content **for free — including monetized content**.
- Podcasts, videos, audiobooks, social media posts, and similar creative works
- Personal *and* commercial/monetized creator channels (ad-supported, sponsored, subscription, etc.)
**The one requirement: acknowledge Boson AI's Higgs Audio.** The acknowledgment must appear in **at least one** of the following ways:
- **In the audio** — e.g. *"This audio was created with Boson AI's Higgs Audio."*
- **In the accompanying text**, displayed prominently — e.g. in the post body, video description, or show notes. It must be clearly visible and **not** hidden at the bottom of the credits or annotations.
> This audio was created with Boson AI's Higgs Audio — https://www.boson.ai/higgs-audio
**Still requires a separate commercial license.** The Creator Use Grant covers *creating content* with the model. It does **not** cover hosting the model behind an API or as a service, redistributing/reselling/fine-tuning the model for resale, or embedding the model in a product or application. For these uses, [contact us](https://www.boson.ai) for a commercial license.
The Creator Use Grant does not change the [use restrictions](#license) — no non-consensual voice cloning or impersonation, no fraud or deception, and AI-generated audio must be disclosed where required. Full terms are in Section II-A of the [LICENSE](./LICENSE).
Boson Higgs TTS 3 Research and Non-Commercial License — see [LICENSE](./LICENSE). Includes a **Creator Use Grant** (free monetized creator use with attribution; see [Creator Use](#creator-use-free-for-digital-creators) above).
Have a use case that isn’t covered by the current license? We’d still love to hear from you. Reach out to [contact@boson.ai](mailto:contact@boson.ai) — we’re open to discussing your use case and alternative licensing arrangements.