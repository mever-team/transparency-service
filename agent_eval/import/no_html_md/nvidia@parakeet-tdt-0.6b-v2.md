# **🦜 Parakeet TDT 0.6B V2 (En)**
[![Model architecture](https://img.shields.io/badge/Model_Arch-FastConformer--TDT-blue#model-badge)](#model-architecture)
| [![Model size](https://img.shields.io/badge/Params-0.6B-green#model-badge)](#model-architecture)
| [![Language](https://img.shields.io/badge/Language-en-orange#model-badge)](#datasets)
> **🎉 NEW: Multilingual Parakeet TDT 0.6B V3 is now available!**  
> 🌍 **25 European Languages** | 🚀 **Enhanced Performance** | 🔗 **[Try it here: nvidia/parakeet-tdt-0.6b-v3](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3)**
`parakeet-tdt-0.6b-v2` is a 600-million-parameter automatic speech recognition (ASR) model designed for high-quality English transcription, featuring support for punctuation, capitalization, and accurate timestamp prediction. Try Demo here: https://huggingface.co/spaces/nvidia/parakeet-tdt-0.6b-v2 
This XL variant of the FastConformer [1] architecture integrates the TDT [2] decoder and is trained with full attention, enabling efficient transcription of audio segments up to 24 minutes in a single pass. The model achieves an RTFx of 3380 on the HF-Open-ASR leaderboard with a batch size of 128. Note: *RTFx Performance may vary depending on dataset audio duration and batch size.*  
- Accurate word-level timestamp predictions  
- Automatic punctuation and capitalization  
- Robust performance on spoken numbers, and song lyrics transcription 
For more information, refer to the [Model Architecture](#model-architecture) section and the [NeMo documentation](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/asr/models.html#fast-conformer).
This model is ready for commercial/non-commercial use.
GOVERNING TERMS: Use of this model is governed by the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode.en) license.
### Discover more from NVIDIA: 
For documentation, deployment guides, enterprise-ready APIs, and the latest open models—including Nemotron and other cutting-edge speech, translation, and generative AI—visit the NVIDIA Developer Portal at developer.nvidia.com.
Join the community to access tools, support, and resources to accelerate your development with NVIDIA’s NeMo, Riva, NIM, and foundation models.
#### Explore more from NVIDIA:
What is [Nemotron](https://www.nvidia.com/en-us/ai-data-science/foundation-models/nemotron/)?
NVIDIA Developer [Nemotron](https://developer.nvidia.com/nemotron)
[NVIDIA Riva Speech](https://developer.nvidia.com/riva?sortBy=developer_learning_library%2Fsort%2Ffeatured_in.riva%3Adesc%2Ctitle%3Aasc#demos)
[NeMo Documentation](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/asr/models.html)
This model serves developers, researchers, academics, and industries building applications that require speech-to-text capabilities, including but not limited to: conversational AI, voice assistants, transcription services, subtitle generation, and voice analytics platforms.
* This model was developed based on [FastConformer encoder](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/asr/models.html#fast-conformer) architecture[1] and TDT decoder[2]
* This model has 600 million model parameters.
- **Input Type(s):** 16kHz Audio
- **Input Format(s):** `.wav` and `.flac` audio formats
- **Input Parameters:** 1D (audio signal)
- **Other Properties Related to Input:**  Monochannel audio
- **Output Parameters:**  1D (text)
- **Other Properties Related to Output:** Punctuations and Capitalizations included.
Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA's hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions. 
To train, fine-tune or play with the model you will need to install [NVIDIA NeMo](https://github.com/NVIDIA/NeMo). We recommend you install it after you've installed latest PyTorch version.
pip install -U nemo_toolkit["asr"]
The model is available for use in the NeMo toolkit [3], and can be used as a pre-trained checkpoint for inference or for fine-tuning on another dataset.
#### Automatically instantiate the model
import nemo.collections.asr as nemo_asr
asr_model = nemo_asr.models.ASRModel.from_pretrained(model_name="nvidia/parakeet-tdt-0.6b-v2")
#### Transcribing using Python
wget https://dldata-public.s3.us-east-2.amazonaws.com/2086-149220-0033.wav
output = asr_model.transcribe(['2086-149220-0033.wav'])
#### Transcribing with timestamps
To transcribe with timestamps:
output = asr_model.transcribe(['2086-149220-0033.wav'], timestamps=True)
# by default, timestamps are enabled for char, word and segment level
word_timestamps = output[0].timestamp['word'] # word level timestamps for first sample
segment_timestamps = output[0].timestamp['segment'] # segment level timestamps
char_timestamps = output[0].timestamp['char'] # char level timestamps
for stamp in segment_timestamps:
    print(f"{stamp['start']}s - {stamp['end']}s : {stamp['segment']}")
## Try via API — No Setup Required
Transcribe audio instantly using the free hosted API on [build.nvidia.com](https://build.nvidia.com/nvidia/parakeet-tdt-0_6b-v2) — no GPU, no Docker, no model download needed.
**1. Get a free API key:** Visit [build.nvidia.com/nvidia/parakeet-tdt-0_6b-v2](https://build.nvidia.com/nvidia/parakeet-tdt-0_6b-v2) and click **Get API Key**
**2. Install the Riva client:**
pip install nvidia-riva-client
**3. Transcribe an audio file:**
    uri="grpc.nvcf.nvidia.com:443",
        ["function-id", "d3fe9151-442b-4204-a70d-5fcc597fd610"],
        ["authorization", "Bearer nvapi-YOUR_API_KEY"]
asr_service = riva.client.ASRService(auth)
with open("audio.wav", "rb") as f:
config = riva.client.RecognitionConfig(
    enable_automatic_punctuation=True,
    enable_word_time_offsets=True,
response = asr_service.offline_recognize(audio, config)
print(response.results[0].alternatives[0].transcript)
git clone https://github.com/nvidia-riva/python-clients.git
export NVIDIA_API_KEY="nvapi-YOUR_API_KEY"
python python-clients/scripts/asr/transcribe_file_offline.py \
    --server grpc.nvcf.nvidia.com:443 --use-ssl \
    --metadata function-id "d3fe9151-442b-4204-a70d-5fcc597fd610" \
    --metadata "authorization" "Bearer $NVIDIA_API_KEY" \
    --word-time-offsets --automatic-punctuation \
> **Note:** The hosted API accepts 16-bit mono audio in WAV, OGG, or OPUS format. See the [API Reference](https://docs.nvidia.com/nim/riva/asr/latest/protos.html) for streaming and advanced options.
**Supported Hardware Microarchitecture Compatibility:** 
**[Preferred/Supported] Operating System(s):**
**Hardware Specific Requirements:**
Atleast 2GB RAM for model to load. The bigger the RAM, the larger audio input it supports.
Current version: parakeet-tdt-0.6b-v2. Previous versions can be [accessed](https://huggingface.co/collections/nvidia/parakeet-659711f49d1469e51546e021) here. 
## Training and Evaluation Datasets:
This model was trained using the NeMo toolkit [3], following the strategies below:
- Initialized from a FastConformer SSL checkpoint that was pretrained with a wav2vec method on the LibriLight dataset[7].  
- Trained for 150,000 steps on 64 A100 GPUs. 
- Dataset corpora were balanced using a temperature sampling value of 0.5.  
- Stage 2 fine-tuning was performed for 2,500 steps on 4 A100 GPUs using approximately 500 hours of high-quality, human-transcribed data of NeMo ASR Set 3.0.  
Training was conducted using this [example script](https://github.com/NVIDIA/NeMo/blob/main/examples/asr/asr_transducer/speech_to_text_rnnt_bpe.py) and [TDT configuration](https://github.com/NVIDIA/NeMo/blob/main/examples/asr/conf/fastconformer/hybrid_transducer_ctc/fastconformer_hybrid_tdt_ctc_bpe.yaml).
The tokenizer was constructed from the training set transcripts using this [script](https://github.com/NVIDIA/NeMo/blob/main/scripts/tokenizers/process_asr_text_tokenizer.py).
The model was trained on the Granary dataset[8], consisting of approximately 120,000 hours of English speech data:
- 10,000 hours from human-transcribed NeMo ASR Set 3.0, including:
  - National Speech Corpus Part 1 
  - Multilingual LibriSpeech (MLS English) – 2,000-hour subset
- 110,000 hours of pseudo-labeled data from:
  - YTC (YouTube-Commons) dataset[4]
All transcriptions preserve punctuation and capitalization. The Granary dataset[8] will be made publicly available after presentation at Interspeech 2025.
**Data Collection Method by dataset**
**Labeling Method by dataset**
* Noise robust data from various sources
* Single channel, 16kHz sampled data
Huggingface Open ASR Leaderboard datasets are used to evaluate the performance of this model. 
**Data Collection Method by dataset**
**Labeling Method by dataset**
* All are commonly used for benchmarking English ASR systems.
* Audio data is typically processed into a 16kHz mono channel format for ASR evaluation, consistent with benchmarks like the [Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard).
#### Huggingface Open-ASR-Leaderboard Performance
The performance of Automatic Speech Recognition (ASR) models is measured using Word Error Rate (WER). Given that this model is trained on a large and diverse dataset spanning multiple domains, it is generally more robust and accurate across various types of audio.
The table below summarizes the WER (%) using a Transducer decoder with greedy decoding (without an external language model):
Performance across different Signal-to-Noise Ratios (SNR) using MUSAN music and noise samples:
### Telephony Audio Performance 
Performance comparison between standard 16kHz audio and telephony-style audio (using μ-law encoding with 16kHz→8kHz→16kHz conversion):
These WER scores were obtained using greedy decoding without an external language model. Additional evaluation details are available on the [Hugging Face ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard).[6]
[1] [Fast Conformer with Linearly Scalable Attention for Efficient Speech Recognition](https://arxiv.org/abs/2305.05084)
[2] [Efficient Sequence Transduction by Jointly Predicting Tokens and Durations](https://arxiv.org/abs/2304.06795)
[3] [NVIDIA NeMo Toolkit](https://github.com/NVIDIA/NeMo)
[4] [Youtube-commons: A massive open corpus for conversational and multimodal data](https://huggingface.co/blog/Pclanglais/youtube-commons)
[5] [Yodas: Youtube-oriented dataset for audio and speech](https://arxiv.org/abs/2406.00899)
[6] [HuggingFace ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard)
[7] [MOSEL: 950,000 Hours of Speech Data for Open-Source Speech Foundation Model Training on EU Languages](https://arxiv.org/abs/2410.01036) 
[8] [Granary: Speech Recognition and Translation Dataset in 25 European Languages](https://arxiv.org/pdf/2505.13404)
NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. When downloaded or used in accordance with our terms of service, developers should work with their supporting model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.
For more detailed information on ethical considerations for this model, please see the Model Card++ Explainability, Bias, Safety & Security, and Privacy Subcards [here](https://developer.nvidia.com/blog/enhancing-ai-transparency-and-ethical-considerations-with-model-card/).
Please report security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).