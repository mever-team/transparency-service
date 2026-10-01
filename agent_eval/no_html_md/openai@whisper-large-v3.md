Whisper is a state-of-the-art model for automatic speech recognition (ASR) and speech translation, proposed in the paper 
[Robust Speech Recognition via Large-Scale Weak Supervision](https://huggingface.co/papers/2212.04356) by Alec Radford 
et al. from OpenAI. Trained on >5M hours of labeled data, Whisper demonstrates a strong ability to generalise to many 
datasets and domains in a zero-shot setting.
Whisper large-v3 has the same architecture as the previous [large](https://huggingface.co/openai/whisper-large) and [large-v2](https://huggingface.co/openai/whisper-large-v2) 
models, except for the following minor differences:
1. The spectrogram input uses 128 Mel frequency bins instead of 80
2. A new language token for Cantonese
The Whisper large-v3 model was trained on 1 million hours of weakly labeled audio and 4 million hours of pseudo-labeled 
audio collected using Whisper [large-v2](https://huggingface.co/openai/whisper-large-v2) . The model was trained for 2.0 epochs over this mixture dataset.
The large-v3 model shows improved performance over a wide variety of languages, showing 10% to 20% reduction of errors 
compared to Whisper [large-v2](https://huggingface.co/openai/whisper-large-v2) . For more details on the different checkpoints available, refer to the section [Model details](#model-details).
**Disclaimer**: Content for this model card has partly been written by the 🤗 Hugging Face team, and partly copied and 
pasted from the original model card.
Whisper large-v3 is supported in Hugging Face 🤗 Transformers. To run the model, first install the Transformers 
library. For this example, we'll also install 🤗 Datasets to load toy audio dataset from the Hugging Face Hub, and 
🤗 Accelerate to reduce the model loading time:
pip install --upgrade transformers datasets[audio] accelerate
The model can be used with the [`pipeline`](https://huggingface.co/docs/transformers/main_classes/pipelines#transformers.AutomaticSpeechRecognitionPipeline)
class to transcribe audios of arbitrary length:
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
model_id = "openai/whisper-large-v3"
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
processor = AutoProcessor.from_pretrained(model_id)
    "automatic-speech-recognition",
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
To transcribe a local audio file, simply pass the path to your audio file when you call the pipeline:
Multiple audio files can be transcribed in parallel by specifying them as a list and setting the `batch_size` parameter:
result = pipe(["audio_1.mp3", "audio_2.mp3"], batch_size=2)
Transformers is compatible with all Whisper decoding strategies, such as temperature fallback and condition on previous 
tokens. The following example demonstrates how to enable these heuristics:
    "condition_on_prev_tokens": False,
    "compression_ratio_threshold": 1.35,  # zlib compression ratio threshold (in token space)
    "temperature": (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
result = pipe(sample, generate_kwargs=generate_kwargs)
Whisper predicts the language of the source audio automatically. If the source audio language is known *a-priori*, it 
can be passed as an argument to the pipeline:
result = pipe(sample, generate_kwargs={"language": "english"})
By default, Whisper performs the task of *speech transcription*, where the source audio language is the same as the target
text language. To perform *speech translation*, where the target text is in English, set the task to `"translate"`:
result = pipe(sample, generate_kwargs={"task": "translate"})
Finally, the model can be made to predict timestamps. For sentence-level timestamps, pass the `return_timestamps` argument:
result = pipe(sample, return_timestamps=True)
And for word-level timestamps:
result = pipe(sample, return_timestamps="word")
The above arguments can be used in isolation or in combination. For example, to perform the task of speech transcription 
where the source audio is in French, and we want to return sentence-level timestamps, the following can be used:
result = pipe(sample, return_timestamps=True, generate_kwargs={"language": "french", "task": "translate"})
 For more control over the generation parameters, use the model + processor API directly: 
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
from datasets import Audio, load_dataset
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
model_id = "openai/whisper-large-v3"
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True
processor = AutoProcessor.from_pretrained(model_id)
dataset = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation")
dataset = dataset.cast_column("audio", Audio(processor.feature_extractor.sampling_rate))
    sampling_rate=sample["sampling_rate"],
inputs = inputs.to(device, dtype=torch_dtype)
    "condition_on_prev_tokens": False,
    "compression_ratio_threshold": 1.35,  # zlib compression ratio threshold (in token space)
    "temperature": (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
pred_ids = model.generate(**inputs, **gen_kwargs)
pred_text = processor.batch_decode(pred_ids, skip_special_tokens=True, decode_with_timestamps=False)
## Additional Speed & Memory Improvements
You can apply additional speed and memory improvements to Whisper to further reduce the inference speed and VRAM 
Whisper has a receptive field of 30-seconds. To transcribe audios longer than this, one of two long-form algorithms are
1. **Sequential:** uses a "sliding window" for buffered inference, transcribing 30-second slices one after the other
2. **Chunked:** splits long audio files into shorter ones (with a small overlap between segments), transcribes each segment independently, and stitches the resulting transcriptions at the boundaries
The sequential long-form algorithm should be used in either of the following scenarios:
1. Transcription accuracy is the most important factor, and speed is less of a consideration
2. You are transcribing **batches** of long audio files, in which case the latency of sequential is comparable to chunked, while being up to 0.5% WER more accurate
Conversely, the chunked algorithm should be used when:
1. Transcription speed is the most important factor
2. You are transcribing a **single** long audio file
By default, Transformers uses the sequential algorithm. To enable the chunked algorithm, pass the `chunk_length_s` 
parameter to the `pipeline`. For large-v3, a chunk length of 30-seconds is optimal. To activate batching over long 
audio files, pass the argument `batch_size`:
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
model_id = "openai/whisper-large-v3"
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True
processor = AutoProcessor.from_pretrained(model_id)
    "automatic-speech-recognition",
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    batch_size=16,  # batch size for inference - set based on your device
dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
The Whisper forward pass is compatible with [`torch.compile`](https://pytorch.org/docs/stable/generated/torch.compile.html)
**Note:** `torch.compile` is currently not compatible with the Chunked long-form algorithm or Flash Attention 2 ⚠️
from torch.nn.attention import SDPBackend, sdpa_kernel
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
torch.set_float32_matmul_precision("high")
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
model_id = "openai/whisper-large-v3"
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True
# Enable static cache and compile the forward pass
model.generation_config.cache_implementation = "static"
model.generation_config.max_new_tokens = 256
model.forward = torch.compile(model.forward, mode="reduce-overhead", fullgraph=True)
processor = AutoProcessor.from_pretrained(model_id)
    "automatic-speech-recognition",
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
for _ in tqdm(range(2), desc="Warm-up step"):
    with sdpa_kernel(SDPBackend.MATH):
        result = pipe(sample.copy(), generate_kwargs={"min_new_tokens": 256, "max_new_tokens": 256})
with sdpa_kernel(SDPBackend.MATH):
We recommend using [Flash-Attention 2](https://huggingface.co/docs/transformers/main/en/perf_infer_gpu_one#flashattention-2) if your GPU supports it and you are not using [torch.compile](#torch-compile). 
To do so, first install [Flash Attention](https://github.com/Dao-AILab/flash-attention):
pip install flash-attn --no-build-isolation
Then pass `attn_implementation="flash_attention_2"` to `from_pretrained`:
model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, attn_implementation="flash_attention_2")
#### Torch Scale-Product-Attention (SDPA)
If your GPU does not support Flash Attention, we recommend making use of PyTorch [scaled dot-product attention (SDPA)](https://pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html). 
This attention implementation is activated **by default** for PyTorch versions 2.1.1 or greater. To check 
whether you have a compatible PyTorch version, run the following Python code snippet:
from transformers.utils import is_torch_sdpa_available
print(is_torch_sdpa_available())
If the above returns `True`, you have a valid version of PyTorch installed and SDPA is activated by default. If it 
returns `False`, you need to upgrade your PyTorch version according to the [official instructions](https://pytorch.org/get-started/locally/)
Once a valid PyTorch version is installed, SDPA is activated by default. It can also be set explicitly by specifying 
`attn_implementation="sdpa"` as follows:
model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, attn_implementation="sdpa")
For more information about how to use the SDPA refer to the [Transformers SDPA documentation](https://huggingface.co/docs/transformers/en/perf_infer_gpu_one#pytorch-scaled-dot-product-attention).
Whisper is a Transformer based encoder-decoder model, also referred to as a _sequence-to-sequence_ model. There are two
flavours of Whisper model: English-only and multilingual. The English-only models were trained on the task of English 
speech recognition. The multilingual models were trained simultaneously on multilingual speech recognition and speech 
translation. For speech recognition, the model predicts transcriptions in the *same* language as the audio. For speech 
translation, the model predicts transcriptions to a *different* language to the audio.
Whisper checkpoints come in five configurations of varying model sizes. The smallest four are available as English-only 
and multilingual. The largest checkpoints are multilingual only. All ten of the pre-trained checkpoints 
are available on the [Hugging Face Hub](https://huggingface.co/models?search=openai/whisper). The 
checkpoints are summarised in the following table with links to the models on the Hub:
The pre-trained Whisper model demonstrates a strong ability to generalise to different datasets and domains. However, 
its predictive capabilities can be improved further for certain languages and tasks through *fine-tuning*. The blog 
post [Fine-Tune Whisper with 🤗 Transformers](https://huggingface.co/blog/fine-tune-whisper) provides a step-by-step 
guide to fine-tuning the Whisper model with as little as 5 hours of labelled data.
The primary intended users of these models are AI researchers studying robustness, generalization, capabilities, biases, and constraints of the current model. However, Whisper is also potentially quite useful as an ASR solution for developers, especially for English speech recognition. We recognize that once models are released, it is impossible to restrict access to only “intended” uses or to draw reasonable guidelines around what is or is not research.
The models are primarily trained and evaluated on ASR and speech translation to English tasks. They show strong ASR results in ~10 languages. They may exhibit additional capabilities, particularly if fine-tuned on certain tasks like voice activity detection, speaker classification, or speaker diarization but have not been robustly evaluated in these areas. We strongly recommend that users perform robust evaluations of the models in a particular context and domain before deploying them.
In particular, we caution against using Whisper models to transcribe recordings of individuals taken without their consent or purporting to use these models for any kind of subjective classification. We recommend against use in high-risk domains like decision-making contexts, where flaws in accuracy can lead to pronounced flaws in outcomes. The models are intended to transcribe and translate speech, use of the model for classification is not only not evaluated but also not appropriate, particularly to infer human attributes.
The large-v3 checkpoint is trained on 1 million hours of weakly labeled audio and 4 million hours of pseudo-labeled audio collected using Whisper large-v2. 
As discussed in [the accompanying paper](https://cdn.openai.com/papers/whisper.pdf), we see that performance on transcription in a given language is directly correlated with the amount of training data we employ in that language.
## Performance and Limitations
Our studies show that, over many existing ASR systems, the models exhibit improved robustness to accents, background noise, technical language, as well as zero shot translation from multiple languages into English; and that accuracy on speech recognition and translation is near the state-of-the-art level. 
However, because the models are trained in a weakly supervised manner using large-scale noisy data, the predictions may include texts that are not actually spoken in the audio input (i.e. hallucination). We hypothesize that this happens because, given their general knowledge of language, the models combine trying to predict the next word in audio with trying to transcribe the audio itself.
Our models perform unevenly across languages, and we observe lower accuracy on low-resource and/or low-discoverability languages or languages where we have less training data. The models also exhibit disparate performance on different accents and dialects of particular languages, which may include higher word error rate across speakers of different genders, races, ages, or other demographic criteria. Our full evaluation results are presented in [the paper accompanying this release](https://cdn.openai.com/papers/whisper.pdf). 
In addition, the sequence-to-sequence architecture of the model makes it prone to generating repetitive texts, which can be mitigated to some degree by beam search and temperature scheduling but not perfectly. Further analysis on these limitations are provided in [the paper](https://cdn.openai.com/papers/whisper.pdf). It is likely that this behavior and hallucinations may be worse on lower-resource and/or lower-discoverability languages.
We anticipate that Whisper models’ transcription capabilities may be used for improving accessibility tools. While Whisper models cannot be used for real-time transcription out of the box – their speed and size suggest that others may be able to build applications on top of them that allow for near-real-time speech recognition and translation. The real value of beneficial applications built on top of Whisper models suggests that the disparate performance of these models may have real economic implications.
There are also potential dual use concerns that come with releasing Whisper. While we hope the technology will be used primarily for beneficial purposes, making ASR technology more accessible could enable more actors to build capable surveillance technologies or scale up existing surveillance efforts, as the speed and accuracy allow for affordable automatic transcription and translation of large volumes of audio communication. Moreover, these models may have some capabilities to recognize specific individuals out of the box, which in turn presents safety concerns related both to dual use and disparate performance. In practice, we expect that the cost of transcription is not the limiting factor of scaling up surveillance projects.
### BibTeX entry and citation info
  doi = {10.48550/ARXIV.2212.04356},
  url = {https://arxiv.org/abs/2212.04356},
  author = {Radford, Alec and Kim, Jong Wook and Xu, Tao and Brockman, Greg and McLeavey, Christine and Sutskever, Ilya},
  title = {Robust Speech Recognition via Large-Scale Weak Supervision},
  copyright = {arXiv.org perpetual, non-exclusive license}