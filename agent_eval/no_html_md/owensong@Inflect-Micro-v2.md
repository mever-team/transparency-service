![Inflect-Micro-v2 release cover](assets/inflect-v2-repository-hero.png)
Complete local text-to-waveform speech synthesis under 10M parameters.
Fixed-voice English TTS with deterministic seeds, long-text handling, and CPU or CUDA inference.
> Thanks so much for all the support shown on this project! I built and funded Inflect v2 independently - if this release finds a real audience, I would like to continue the project with a v3, which might include things like more langauges, voices, and voice quality improvements. If the model is useful to you, leaving a like on Hugging Face genuinely helps more people discover it.
9,356,513 deployable parameters · 37.53 MB FP32 · 24 kHz mono output
> **New: public adaptation toolkit**
> Prepare data, audit train/validation splits, adapt a fixed voice or language, resume training, evaluate checkpoints, and export PyTorch or ONNX packages with the [Inflect adaptation toolkit](https://github.com/owenawsong/Inflect/tree/main/finetune). Adapted quality is experimental and depends on the dataset, frontend, and fluent-speaker evaluation.
Inflect v2 uses one public API across two sizes: **Micro prioritizes quality below 10M parameters; Nano prioritizes footprint below 4M.**
These are held-out text generations, not reconstructions of training audio. Each transcript is shown exactly as passed to the public frontend.
No single metric captures TTS quality. Inflect v2 reports **human preference**, **predicted naturalness**, **multi-ASR intelligibility**, **complete footprint**, and **runtime** separately rather than compressing them into one unverifiable score.
The headline row always refers to **Inflect-Micro-v2**. Detailed competitor results and protocol boundaries are kept visible below.
**Comparison set.** Results include [KittenTTS Nano](https://huggingface.co/KittenML/kitten-tts-nano-0.8), [Piper Low](https://huggingface.co/rhasspy/piper-voices), and [Supertonic 3](https://huggingface.co/Supertone/supertonic-3), established compact or local TTS baselines with larger deployable weight footprints than both Inflect releases. Weight sizes are compared at package level, and no single metric is treated as proof of overall superiority.
![Community blind listening](assets/evidence/human-preference.svg)
Inflect-Micro-v2 recorded a **66.2% preference rate** (21 wins · 10 losses · 3 ties) in the final anonymous community study. Systems were hidden, left/right order was randomized, and ties count as half a win. This is descriptive community evidence, not formal MOS.
### 2. Predicted naturalness versus footprint
![Predicted quality versus footprint](assets/evidence/quality-vs-footprint.svg)
The UTMOS22 run used 500 identical unseen prompts per voice. KittenTTS and Piper are equal-weight two-voice means; their observed voice ranges appear as whiskers. Supertonic 3-step is reported below the plotted range rather than flattening every other system.
**Inflect-Micro-v2: 4.395 UTMOS22**, 95% bootstrap CI **4.381–4.408**. UTMOS22 is a learned predictor, not human MOS.
### 3. Intelligibility on unseen text
![Two-ASR semantic WER consensus](assets/evidence/asr-consensus.svg)
The headline score is the equal-weight mean of Qwen3-ASR and Nemotron 3.5 corpus WER for **every** system. Whisper is excluded consistently from the headline because it produced insertion-heavy hallucinations on a subset of otherwise intelligible Supertonic 8-step clips. It is not deleted: the complete three-ASR evidence remains below.
Open the complete three-ASR audit
![Semantic WER across Qwen3-ASR, Nemotron 3.5, and Whisper large-v3](assets/evidence/modern400-three-asr.svg)
For Inflect-Micro-v2, the individual results are **2.52% Qwen3-ASR**, **5.45% Nemotron 3.5**, and **2.73% Whisper large-v3**. The former three-model mean, **3.57%**, is retained only as a descriptive audit value and is not used as the headline score.
Open evaluator robustness and error-category diagnostics
![ASR evaluator robustness](assets/evidence/asr-robustness.svg)
![Semantic WER by prompt category](assets/evidence/category-semantic-wer.svg)
These views are diagnostics, not additional leaderboards. They show where the
recognizers disagree and which prompt categories still produce recoverable
Both Inflect releases synthesize comfortably faster than real time on CPU. The
managed reference run used a Hugging Face **CPU Upgrade** instance (8 vCPU,
32 GB RAM) with **four framework threads**, end-to-end text-to-waveform timing,
and 100 fixed Modern400 prompts. Three complete passes were recorded; the first
cache-building pass was excluded and the table pools passes two and three.
These are package-level results from the public PyTorch runtime, not a claim
that Inflect is the fastest compact TTS system. Hardware, frontend behavior,
framework, compilation, and thread policy all affect small-model measurements.
Open directional compact-system speed context
The same managed CPU and four-thread policy were used for a shorter comparator
pass: the identical 50-prompt prefix, repeated twice. KittenTTS and Piper are
equal-work pooled across their two tested voices.
Because Inflect uses the larger 100-prompt steady-state run while comparator
rows use the shorter 50-prompt confirmation pass, this table is deployment
context rather than a perfectly matched speed leaderboard. Several comparators
also use optimized ONNX runtimes, while the published Inflect benchmark above
uses the canonical PyTorch runtime. The separately released Inflect ONNX path
has not been substituted into those benchmark numbers.
### 5. Complete weight footprint
![Complete deployable model footprint](assets/evidence/model-footprint.svg)
Voice variants sharing the same weights are merged. Inflect totals include the integrated waveform decoder.
Open the frozen evaluation protocol
- Modern400 uses 400 identical unseen English prompts per system: 200 fixed modern/stress prompts plus 200 deterministic FLEURS `en_us` test prompts.
- Exact-text exclusion was checked against 87,362 training transcripts.
- All ASR inputs are resampled to 16 kHz and scored with the same disclosed English normalizer.
- UTMOS22 uses `tarepan/SpeechMOS` v1.2.0 on a separate 500-prompt generation set.
- Headline intervals use 10,000 bootstrap samples.
- The Modern400 corpus SHA-256 is `b7504ce2dce44a2da82770a6a5dfd2a034fe17e2113980f8a69663ade417a34c`.
- Prompts, hypotheses, compressed row-level reports, and summaries ship under `evaluation/final/`.
- Runtime is evaluated separately because framework, thread policy, compilation,
  and host load can dominate small-model comparisons.
**Inflect-Micro-v2** is the quality-focused member of the family. Both models use the same public API and complete text-to-waveform packaging.
python -m pip install --upgrade huggingface_hub
hf download owensong/Inflect-Micro-v2 --local-dir Inflect-Micro-v2
python -m pip install -r requirements.txt
This uses the Hub's version-aware downloader and retrieves the complete
repository. A Git clone also works, but `hf download` is the recommended path
for ordinary model installation.
from inference import InflectTTS
tts = InflectTTS(".", device="cpu")
    "A small voice can still have something meaningful to say.",
from huggingface_hub import snapshot_download
model_dir = snapshot_download("owensong/Inflect-Micro-v2")
from inference import InflectTTS
tts = InflectTTS(model_dir, device="cpu")
sample_rate, waveform = tts.synthesize("The complete model runs locally.")
The result is a 24 kHz mono `float32` waveform. Long input is split at punctuation-aware boundaries, synthesized chunk by chunk, and joined with controlled pauses.
The official verified FP32 export is published separately as
[`Inflect-Micro-v2-ONNX`](https://huggingface.co/owensong/Inflect-Micro-v2-ONNX).
It supports dynamic lengths, CPU/CUDA/DirectML provider selection,
deterministic seeds, and the same long-text wrapper without importing PyTorch:
git clone https://huggingface.co/owensong/Inflect-Micro-v2-ONNX
python -m pip install -r onnx/requirements.txt
python onnx/inference_onnx.py \
  --text "The complete model now runs through ONNX Runtime." \
The neural model is split into `duration.onnx` and `decode.onnx`; together they
contain the complete learned text-to-waveform path. The English eSpeak-ng
frontend remains CPU-side code. See the
[`ONNX repository`](https://huggingface.co/owensong/Inflect-Micro-v2-ONNX)
for graph contracts, provenance, parity measurements, browser deployment, and
Architecture and parameter budget
Inflect v2 is a parameter-efficient VITS-family end-to-end text-to-waveform generator with an English phoneme frontend, monotonic alignment, stochastic latent synthesis, residual coupling flow, and an integrated alias-reduced neural waveform decoder.
The release describes the deployable architecture. Private corpus-construction and optimization details are not part of this open-weight package.
Controls, determinism, and long text
Long passages are punctuation-aware chunks, not one unlimited autoregressive pass. Chunk boundaries receive short pauses and edge fades. See [`docs/API.md`](https://huggingface.co/owensong/Inflect-Micro-v2/blob/main/docs/API.md) for waveform contracts and concurrency notes.
Data, voice, and adaptation status
The release contains one fixed synthetic English voice. The package does not redistribute a real-speaker recording corpus, does not claim the voice as the identity of a real person, and requires no reference audio or external model at inference.
The base release remains inference-first, but a public **experimental fixed-voice and language adaptation workflow** is now available. A new voice replaces the built-in speaker rather than adding runtime voice cloning. A new language requires owned or licensed speech data, a compatible phoneme frontend, symbol migration, retraining, and fluent-speaker evaluation. Start with the [Inflect adaptation toolkit](https://github.com/owenawsong/Inflect/tree/main/finetune), then review [`docs/DATA_AND_VOICE.md`](https://huggingface.co/owensong/Inflect-Micro-v2/blob/main/docs/DATA_AND_VOICE.md).
- English only, with one fixed male voice. This is not zero-shot voice cloning.
- Unfamiliar phrasing can become flatter, less expressive, or less stable.
- Numbers, abbreviations, homographs, and uncommon names remain frontend- and context-sensitive.
- Long passages use punctuation-aware chunking; transitions can differ from a native long-form model pass.
- Stochastic variation can alter timing and pronunciation. Fix the seed for comparisons.
- UTMOS22 and ASR scores do not replace controlled human MOS or MUSHRA-style evaluation.
- Not validated for medical, legal, emergency, or accessibility-critical communication.
Do not use the included voice to impersonate a real person, deceive listeners, or create fraudulent content. Disclose synthetic speech where the context could otherwise mislead. Users are responsible for applicable laws and the Apache-2.0 license.
## License, integrity, and attribution
Original Inflect code and weights are released under Apache-2.0. Bundled third-party components retain their own notices in [`THIRD_PARTY_NOTICES.md`](https://huggingface.co/owensong/Inflect-Micro-v2/blob/main/THIRD_PARTY_NOTICES.md). `release_manifest.json` records packaged file sizes and SHA-256 hashes.
### Private training scope and contact
Inflect v2 is an **open-weight** release. Deployable weights, inference code, frontend code, evaluation prompts, and release reports are public. The training corpus-generation pipeline, private filtering infrastructure, and full optimization recipe are not part of the public package.
Owen Song may share additional technical context privately for credible research, collaboration, reproducibility, or deployment inquiries when the request has a clear purpose and does not conflict with licensing or data-provenance constraints.
- **Discord:** `b111ue` — fastest for informal technical questions
- **Community server:** [discord.gg/CVJYedvzvp](https://discord.gg/CVJYedvzvp)
- **Email:** [owen.aw.song@gmail.com](mailto:owen.aw.song@gmail.com) — preferred for professional inquiries
@software{song2026inflectmicrov2,
  title = {Inflect-Micro-v2: Complete Local Text-to-Waveform TTS Under 10M Parameters},
  url = {https://huggingface.co/owensong/Inflect-Micro-v2}
Designed and developed independently by Owen Song · open weights · Apache-2.0 · complete local text-to-waveform inference