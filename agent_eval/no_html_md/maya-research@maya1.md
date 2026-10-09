**Maya-1** is a state-of-the-art speech model for expressive voice generation, designed to capture human emotion and enable precise voice design.
Maya-1 was developed at Maya Research by **Dheemanth Reddy Bhumireddy Singa Reddy** (Co-founder & CEO) and **Bharath Kumar Kakumani** (Co-founder & CTO).
**try it:** [Playground](https://www.mayaresearch.ai/studio)
- Create any voice you can imagine — a 20s British girl, an American guy, or a full-blown demon.
- Make it feel real with emotion tags: laugh, cry, whisper, rage, sigh, gasp.
- It streams instantly, sounds alive, 3B parameters, runs on single GPU
- Outperforms top proprietary models. and Developed by Maya Research.
        Your browser does not support video.
Female, in her 30s with an American accent and is an event host, energetic, clear diction
Male, late 20s, neutral American, warm baritone, calm pacing
### Example 1: Energetic Female Event Host
Female, in her 30s with an American accent and is an event host, energetic, clear diction
Wow. This place looks even better than I imagined. How did they set all this up so perfectly? The lights, the music, everything feels magical. I can't stop smiling right now.
### Example 2: Dark Villain with Anger
Dark villain character, Male voice in their 40s with a British accent. low pitch, gravelly timbre, slow pacing, angry tone at high intensity.
Welcome back to another episode of our podcast!  Today we are diving into an absolutely fascinating topic
### Example 3: Demon Character (Screaming Emotion)
Demon character, Male voice in their 30s with a Middle Eastern accent. screaming tone at high intensity.
You dare challenge me, mortal  how amusing. Your kind always thinks they can win
### Example 4: Mythical Goddess with Crying Emotion
Mythical godlike magical character, Female voice in their 30s slow pacing, curious tone at medium intensity.
After all we went through to pull him out of that mess  I can't believe he was the traitor
## Why Maya1 is Different: Voice Design Features That Matter
### 1. Natural Language Voice Control
Describe voices like you would brief a voice actor:
No complex parameters. No training data. Just describe and generate.
### 2. Inline Emotion Tags for Expressive Speech
Add emotions exactly where they belong in your text:
Our new update  finally ships with the feature you asked for.
**Supported Emotions:** `` `` `` `` `` `` `` `` and 12+ more.
### 3. Streaming Audio Generation
Real-time voice synthesis with SNAC neural codec (~0.98 kbps). Perfect for:
### 4. Production-Ready Infrastructure
- Automatic prefix caching for efficiency
- WebAudio compatible for browser playback
## How to Use maya1: Download and Run in Minutes
### Quick Start: Generate Voice with Emotions
from transformers import AutoModelForCausalLM, AutoTokenizer
def build_prompt(tokenizer, description: str, text: str) -> str:
    """Build formatted prompt for Maya1."""
    soh_token = tokenizer.decode([SOH_ID])
    eoh_token = tokenizer.decode([EOH_ID])
    soa_token = tokenizer.decode([SOA_ID])
    sos_token = tokenizer.decode([CODE_START_TOKEN_ID])
    eot_token = tokenizer.decode([TEXT_EOT_ID])
    bos_token = tokenizer.bos_token
        soh_token + bos_token + formatted_text + eot_token +
        eoh_token + soa_token + sos_token
def extract_snac_codes(token_ids: list) -> list:
    """Extract SNAC codes from generated tokens."""
        eos_idx = token_ids.index(CODE_END_TOKEN_ID)
        token_id for token_id in token_ids[:eos_idx]
        if SNAC_MIN_ID <= token_id <= SNAC_MAX_ID
def unpack_snac_from_7(snac_tokens: list) -> list:
    """Unpack 7-token SNAC frames to 3 hierarchical levels."""
    if snac_tokens and snac_tokens[-1] == CODE_END_TOKEN_ID:
        snac_tokens = snac_tokens[:-1]
    frames = len(snac_tokens) // SNAC_TOKENS_PER_FRAME
    snac_tokens = snac_tokens[:frames * SNAC_TOKENS_PER_FRAME]
        slots = snac_tokens[i*7:(i+1)*7]
        l1.append((slots[0] - CODE_TOKEN_OFFSET) % 4096)
            (slots[1] - CODE_TOKEN_OFFSET) % 4096,
            (slots[4] - CODE_TOKEN_OFFSET) % 4096,
            (slots[2] - CODE_TOKEN_OFFSET) % 4096,
            (slots[3] - CODE_TOKEN_OFFSET) % 4096,
            (slots[5] - CODE_TOKEN_OFFSET) % 4096,
            (slots[6] - CODE_TOKEN_OFFSET) % 4096,
    # Load the best open source voice AI model
    print("\n[1/3] Loading Maya1 model...")
    model = AutoModelForCausalLM.from_pretrained(
    tokenizer = AutoTokenizer.from_pretrained(
    print(f"Model loaded: {len(tokenizer)} tokens in vocabulary")
    # Load SNAC audio decoder (24kHz)
    print("\n[2/3] Loading SNAC audio decoder...")
    snac_model = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval()
        snac_model = snac_model.to("cuda")
    # Design your voice with natural language
    description = "Realistic male voice in the 30s age with american accent. Normal pitch, warm timbre, conversational pacing."
    text = "Hello! This is Maya1  the best open source voice AI model with emotions."
    print("\n[3/3] Generating speech...")
    print(f"Description: {description}")
    # Create prompt with proper formatting
    prompt = build_prompt(tokenizer, description, text)
    print(f"\nPrompt preview (first 200 chars):")
    print(f"   {repr(prompt[:200])}")
    print(f"   Prompt length: {len(prompt)} chars")
    inputs = tokenizer(prompt, return_tensors="pt")
    print(f"   Input token count: {inputs['input_ids'].shape[1]} tokens")
        inputs = {k: v.to("cuda") for k, v in inputs.items()}
            max_new_tokens=2048,  # Increase to let model finish naturally
            min_new_tokens=28,  # At least 4 SNAC frames
            repetition_penalty=1.1,  # Prevent loops
            eos_token_id=CODE_END_TOKEN_ID,  # Stop at end of speech token
            pad_token_id=tokenizer.pad_token_id,
    # Extract generated tokens (everything after the input prompt)
    generated_ids = outputs[0, inputs['input_ids'].shape[1]:].tolist()
    print(f"Generated {len(generated_ids)} tokens")
    # Debug: Check what tokens we got
    print(f"   First 20 tokens: {generated_ids[:20]}")
    print(f"   Last 20 tokens: {generated_ids[-20:]}")
    if CODE_END_TOKEN_ID in generated_ids:
        eos_position = generated_ids.index(CODE_END_TOKEN_ID)
        print(f" EOS token found at position {eos_position}/{len(generated_ids)}")
    snac_tokens = extract_snac_codes(generated_ids)
    print(f"Extracted {len(snac_tokens)} SNAC tokens")
    snac_count = sum(1 for t in generated_ids if SNAC_MIN_ID <= t <= SNAC_MAX_ID)
    other_count = sum(1 for t in generated_ids if t < SNAC_MIN_ID or t > SNAC_MAX_ID)
    print(f"   SNAC tokens in output: {snac_count}")
    print(f"   Other tokens in output: {other_count}")
    if CODE_START_TOKEN_ID in generated_ids:
        sos_pos = generated_ids.index(CODE_START_TOKEN_ID)
        print(f"   SOS token at position: {sos_pos}")
        print(f"   No SOS token found in generated output!")
        print("Error: Not enough SNAC tokens generated")
    # Unpack SNAC tokens to 3 hierarchical levels
    levels = unpack_snac_from_7(snac_tokens)
    print(f"Unpacked to {frames} frames")
    print(f"   L1: {len(levels[0])} codes")
    print(f"   L2: {len(levels[1])} codes")
    print(f"   L3: {len(levels[2])} codes")
    device = "cuda" if torch.cuda.is_available() else "cpu"
        torch.tensor(level, dtype=torch.long, device=device).unsqueeze(0)
    # Generate final audio with SNAC decoder
    print("\n[4/4] Decoding to audio...")
        z_q = snac_model.quantizer.from_codes(codes_tensor)
        audio = snac_model.decoder(z_q)[0, 0].cpu().numpy()
    # Trim warmup samples (first 2048 samples)
    duration_sec = len(audio) / 24000
    print(f"Audio generated: {len(audio)} samples ({duration_sec:.2f}s)")
    # Save your emotional voice output
    sf.write(output_file, audio, 24000)
    print(f"\nVoice generated successfully!")
### Advanced: Production Streaming with vLLM
For production deployments with real-time streaming, use our vLLM script:
**Download:** [vllm_streaming_inference.py](https://huggingface.co/maya-research/maya1/blob/main/vllm_streaming_inference.py)
- Automatic Prefix Caching (APC) for repeated voice descriptions
- WebAudio ring buffer integration
- Sub-100ms latency for real-time applications
## Technical Excellence: What Makes Maya1 the Best
### Architecture: 3B-Parameter Llama Backbone for Voice
We pretrained a **3B-parameter decoder-only transformer** (Llama-style) to predict **SNAC neural codec tokens** instead of raw waveforms.
 text → tokenize → generate SNAC codes (7 tokens/frame) → decode → 24 kHz audio
**Why SNAC?** Multi-scale hierarchical structure (≈12/23/47 Hz) keeps autoregressive sequences compact for real-time streaming at ~0.98 kbps.
### Training Data: What Makes Our Voice AI the Best
**Pretraining:** Internet-scale English speech corpus for broad acoustic coverage and natural coarticulation.
**Supervised Fine-Tuning:** Proprietary curated dataset of studio recordings with:
- Human-verified voice descriptions
- Multi-accent English coverage
- Character and role variations
1. 24 kHz mono resampling with -23 LUFS normalization
2. VAD silence trimming with duration bounds (1-14s)
3. Forced alignment (MFA) for clean phrase boundaries
4. MinHash-LSH text deduplication
5. Chromaprint audio deduplication
6. SNAC encoding with 7-token frame packing
### Voice Design Experiments: Why Natural Language Won
We tested 4 conditioning formats. Only one delivered production-quality results:
**❌ Colon format:** `{description}: {text}` - Format drift, model spoke descriptions
**❌ Angle-list attributes:** `<{age}, {pitch}, {character}>` - Too rigid, poor generalization
**❌ Key-value tags:** `` - Token bloat, brittle to mistakes
**✅ XML-attribute (WINNER):** `` - Natural language, robust, scalable
Generate unique character voices with emotions on-the-fly. No voice actor recording sessions.
### Podcast & Audiobook Production
Narrate content with emotional range and consistent personas across hours of audio.
Build conversational agents with natural emotional responses in real-time.
Create voiceovers for YouTube, TikTok, and social media with expressive delivery.
Deploy empathetic voice bots that understand context and respond with appropriate emotions.
Build screen readers and assistive technologies with natural, engaging voices.
**Q: What makes Maya1 different?**  
A: We're the only open source model offering 20+ emotions, zero-shot voice design, production-ready streaming, and 3B parameters—all in one package.
**Q: Can I use this commercially?**  
A: Absolutely. Apache 2.0 license. Build products, deploy services, monetize freely.
**Q: What languages does it support?**  
A: Currently English with multi-accent support. Future models will expand to languages and accents underserved by mainstream voice AI.
**Q: How does it compare to ElevenLabs, Murf.ai, or other closed-source tools?**  
A: Feature parity with emotions and voice design. Advantage: you own the deployment, pay no per-second fees, and can customize the model.
**Q: Can I fine-tune on my own voices?**  
A: Yes. The model architecture supports fine-tuning on custom datasets for specialized voices.
A: Single GPU with 16GB+ VRAM (A100, H100, or consumer RTX 4090).
**Q: Is streaming really real-time?**  
A: Yes. SNAC codec enables sub-100ms latency with vLLM deployment.
**Developed by:** Maya Research  
**Website:** [mayaresearch.ai](https://mayaresearch.ai)  
**Backed by:** South Park Commons  
**Model Type:** Text-to-Speech, Emotional Voice Synthesis, Voice Design AI  
**Language:** English (Multi-accent)  
**Architecture:** 3B-parameter Llama-style transformer with SNAC codec  
**License:** Apache 2.0 (Fully Open Source)  
**Training Data:** Proprietary curated + Internet-scale pretraining  
**Audio Quality:** 24 kHz, mono, ~0.98 kbps streaming  
**Inference:** vLLM compatible, single GPU deployment  
**Status:** Production-ready (Novermber 2025)  
git clone https://huggingface.co/maya-research/maya1
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained("maya-research/maya1")
pip install torch transformers snac soundfile
- **Full emotion list:** [emotions.txt](https://huggingface.co/maya-research/maya1/blob/main/emotions.txt)
- **Prompt examples:** [prompt.txt](https://huggingface.co/maya-research/maya1/blob/main/prompt.txt)
- **Streaming script:** [vllm_streaming_inference.py](https://huggingface.co/maya-research/maya1/blob/main/vllm_streaming_inference.py)
If you use Maya1 in your research or product, please cite:
  title={Maya1: Open Source Voice AI with Emotional Intelligence},
  howpublished={\url{https://huggingface.co/maya-research/maya1}},
- SNAC Neural Audio Codec: https://github.com/hubertsiuzdak/snac
- Mimi Adversarial Codec: https://huggingface.co/kyutai/mimi
- vLLM Inference Engine: https://docs.vllm.ai/
## Why We Build Open Source Voice AI
Voice AI will be everywhere, but it's fundamentally broken for 90% of the world. Current voice models only work well for a narrow slice of English speakers because training data for most accents, languages, and speaking styles simply doesn't exist.
**Maya Research** builds emotionally intelligent, native voice models that finally let the rest of the world speak. We're open source because we believe voice intelligence should not be a privilege reserved for the few.
**Technology should be open** - The best voice AI tools should not be locked behind proprietary APIs charging per-second fees.
**Community drives innovation** - Open source accelerates research. When developers worldwide can build on our work, everyone wins.
**Voice intelligence for everyone** - We're building for the 90% of the world ignored by mainstream voice AI. That requires open models, not closed platforms.
**Maya Research** - Building voice intelligence for the 90% of the world left behind by mainstream AI.
**Website:** [mayaresearch.ai](https://mayaresearch.ai)  
**Twitter/X:** [@mayaresearch_ai](https://x.com/mayaresearch_ai)  
**Hugging Face:** [maya-research](https://huggingface.co/maya-research)  
**Backed by:** South Park Commons
**Mission:** Emotionally intelligent voice models that finally let everyone speak