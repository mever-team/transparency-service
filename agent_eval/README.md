# Agent Evaluation Report 

## 🔥 Latest 

Classification accuracy: 30.34% (30/89)

with more tolerance (for example, bias content misclassified as ethics or caveats we count as correct prediction. Also short senteces that can go anywhere we also count as correct)

Classification accuracy: 61% (55/89)
pre-manual inspection results in [here](./evaluation_results/evaluation.html)

* 7 times evaluation results got misclassified as overview.description they all had either `*results*` or `*evaluation*` included in the beginging.
examples:
<pre>
                        *DeepSeek-R1-Evaluation*
For all our models, the maximum generation length is set to 32,768 tokens. For benchmarks requiring sampling, we use a temperature of $0.6$, a top-p value of $0.95$, and generate 64 responses per query to estimate pass@1.
</pre>
<pre>
                        *3. Evaluation Results*
- **OfficeQA Pro and SpreadsheetBench 2.** Kimi K3, GLM-5.2, Claude Opus 4.8, and Claude Fable 5 are evaluated with the Claude Code harness; GPT-5.5 and GPT-5.6 Sol are evaluated with the Codex harness.
</pre>
<pre>
                        *3. Evaluation Results*
- **MCP-Atlas.** All models are evaluated on the 500-task public subset with a 100-turn limit, using Gemini 3.1 Pro as the judge.
</pre>

* 4 cases performance.analysis misclassified as overview.description
examples:

<pre>
                        *Evaluated Use*
The primary intended users of these models are AI researchers studying robustness, generalization, capabilities, biases, and constraints of the current model. However, Whisper is also potentially quite useful as an ASR solution for developers, especially for English speech recognition. We recognize that once models are released, it is impossible to restrict access to only “intended” uses or to draw reasonable guidelines around what is or is not research.
</pre>
</pre>

                        *Performance and Limitations*
Our studies show that, over many existing ASR systems, the models exhibit improved robustness to accents, background noise, technical language, as well as zero shot translation from multiple languages into English; and that accuracy on speech recognition and translation is near the state-of-the-art level.
</pre>
<pre>
                        *Performance and Limitations*
However, because the models are trained in a weakly supervised manner using large-scale noisy data, the predictions may include texts that are not actually spoken in the audio input (i.e. hallucination). We hypothesize that this happens because, given their general knowledge of language, the models combine trying to predict the next word in audio with trying to transcribe the audio itself.
</pre>
<pre>

                        *Performance and Limitations*
Our models perform unevenly across languages, and we observe lower accuracy on low-resource and/or low-discoverability languages or languages where we have less training data. The models also exhibit disparate performance on different accents and dialects of particular languages, which may include higher word error rate across speakers of different genders, races, ages, or other demographic criteria. Our full evaluation results are presented in [the paper accompanying this release](https://cdn.openai.com/papers/whisper.pdf).
</pre>

Also some misclassified inputs are individual sentences. I don’t know how the process works but if the model has no context, it makes sense that they get misclassified. 
Exmples for:
use.out_of_scope_use classified as safety.caveats
>Impersonating individuals without their consent.

> Sexual content without consent of the people who might see it.

training.preprocessing classified as use.out_of_scope_use
>We slightly change their configs and tokenizers. Please use our setting to run these models.

some results are just misclassifications. for example:
performance.methodology
classified as
safety.caveats
<pre>
                        *3. Evaluation Results*
- **Kimi Code Bench 2.0 (in-house).** Kimi K3 is evaluated with the Kimi Code harness (it attains 73.7 with the Claude Code harness); GLM-5.2, Claude Opus 4.8, and Claude Fable 5 with the Claude Code harness; GPT-5.5 and GPT-5.6 Sol with the Codex harness. All models are evaluated at maximum reasoning effort, except GPT-5.5, which uses the "xhigh" setting. As the benchmark includes cybersecurity and safety-related tasks, we also disclose the fraction of refused or fallback tasks: Claude Fable 5 hit 13 fallbacks and 1 refusal out of 80 tasks; 10 refusals out of 80 tasks entered GPT-5.6 Sol's cyber guard; GPT-5.5 had 3 refusals out of 80 tasks.
</pre>
safety.caveats
classified as
overview.description
<pre>
                        *Broader Implications*
We anticipate that Whisper models’ transcription capabilities may be used for improving accessibility tools. While Whisper models cannot be used for real-time transcription out of the box – their speed and size suggest that others may be able to build applications on top of them that allow for near-real-time speech recognition and translation. The real value of beneficial applications built on top of Whisper models suggests that the disparate performance of these models may have real economic implications.
</pre>
performance.methodology
classified as
use.use_cases
<pre>
                        *3. Evaluation Results*
- **MLS-Bench-Lite.** Kimi K3 is evaluated with the Kimi Code harness; GLM-5.2 and the Claude models with the Claude Code harness; GPT-5.5 and GPT-5.6 Sol with the Codex harness.
</pre>
performance.environmental_impact
classified as
safety.risks
<pre>
                        *Environmental Impact*
- **Hardware Type:** A100 PCIe 40GB
- **Hours used:** 150000
- **Cloud Provider:** AWS
- **Compute Region:** US-east
- **Carbon Emitted (Power consumption x Time x Carbon produced based on location of power grid):** 11250 kg CO2 eq.
</pre>

## 🗄️ Data gethering
A list of 66 text-rich Hugging Face repos has been gathered by following similar steps to [Tajkia et al](https://arxiv.org/abs/2608.24807). The full list is available in [repos_urls.txt](./repos_urls.txt). 5 of them were used to evaluate the import for classification accuracy. I planned to use all of them with more metrics and in-depth  analysis, but flaws of the system were revealed early on so there was no need to continue further. The list of the repos used are:
1. https://huggingface.co/Qwen/Qwen3.8-27B
2. https://huggingface.co/deepseek-ai/DeepSeek-R1
3. https://huggingface.co/moonshotai/Kimi-K3
4. https://huggingface.co/CompVis/stable-diffusion-v1-4
5. https://huggingface.co/openai/whisper-large-v3

## 🧭 Methodology
Inside the import pipeline a `<span id='agent-eval-mark'></span>` was placed between each matcher prediction to mark individual predictions. 
 A ground truth was created by asking ChatGPT:

>I have a very important mission for you. I am going to give you hugging face url model card and I want you to reorganize it in a JSON with this format. Do not make any additions or omitions. Just copy paste the content to the correct field. Also keep all code instructions intact and copy them exactly as they are. this is the JSON schema:   
>  
>{JSON schema}
>  
>and here is the model:  
>{Hugging Face link }

The ChatGPT ground truth was used only for reference. Manual checks and corrections were done to obtain the final accuracy. 
To determine if a prediction is correctly classified the `fuzz.partial_ratio(pred, gt)` with a threshold of 80 was used to compensate for the differences that ChatGPT introduced. The precision of this process is irrelevant as manual checks were made before calculating the accuracy. The comparisson between ChatGPT and matcher can be seen in an HTML file [here](./evaluation_results/evaluation.html).


## 📊 Results
Results before manual corrections
```
--- COUNTS ---
Predictions:             54
Correct predictions:     8
Misclassified:           19
Extra/unmatched:         27
```

Results after manual corrections

```
--- COUNTS ---
Predictions:             54
Correct predictions:     16
Misclassified:           38

--- RATES ---
Classification accuracy: 29.63%
```

>#### TLDR
>The results strongly suggest that the preprocessing is insufficient for correct sematic matching. Input texts sometimes are too short to be meaningful. Sometimes they contain several conceptual contents that must be split into several fields.  Formatting of text sometimes is weird with extra spaces and break lines, while tables are converted into consecutive numbers without context. 

#### Examples
Original text that are meant as overview description of the model contains several information. As a result, the matcher gets confused and misclassifies the text. For example, this was classified as `performance.methodology` while it is clearly the overview of the model:
>Kimi K3 is an open-weight, native multimodal agentic model and our most capable model to date. It is a 2.8T-parameter model built on Kimi Delta Attention (KDA) and Attention Residuals (AttnRes), with native vision capabilities and a 1-million-token context window. It is the world's first open 3T-class model, designed for frontier intelligence across long-horizon coding, knowledge work, and reasoning. New Architecture
: Kimi K3 is built on Kimi Delta Attention (KDA) and Attention Residuals (AttnRes), and scales up MoE sparsity with a Stable LatentMoE framework that activates 16 out of 896 experts â yielding an approximate 2.5Ã improvement in overall scaling efficiency over Kimi K2. Long-Horizon Coding
: Operating with minimal human oversight, Kimi K3 sustains long engineering sessions, navigates massive repositories, and orchestrates terminal tools â from GPU kernel optimization and compiler development to vision-in-the-loop game dev, CAD, and even chip design. Agentic Knowledge Work
: Kimi K3 advances end-to-end knowledge work, producing deep research with interactive visualizations, widgets and dashboards, and motion design and video editing, powered by its native multimodal architecture. Open Frontier Weights
: We release the full Kimi K3 model weights under the Kimi K3 License, making frontier intelligence openly available for research, deployment, and further innovation. Except for ZeroBench, which follows the official setting and is run five times, all multimodal scores are averaged over three runs. MMMU-Pro is evaluated following the official protocol, preserving the original input order and prepending images to the text input.

Some input text contains several information that must be classified in different parts of the model card. Instead it is treaded as one block of text and it gets misclassified. For example, this input text has information for several sections like training, performance, and safety caveats. Instead it was classified as training dataset:
>The models are primarily trained and evaluated on ASR and speech translation to English tasks. They show strong ASR results in ~10 languages. They may exhibit additional capabilities, particularly if fine-tuned on certain tasks like voice activity detection, speaker classification, or speaker diarization but have not been robustly evaluated in these areas. We strongly recommend that users perform robust evaluations of the models in a particular context and domain before deploying them. However, because the models are trained in a weakly supervised manner using large-scale noisy data, the predictions may include texts that are not actually spoken in the audio input (i.e. hallucination). We hypothesize that this happens because, given their general knowledge of language, the models combine trying to predict the next word in audio with trying to transcribe the audio itself.

Some text have weird formats and symbols:
>MathVision, BabyVision, and CharXiv (RQ): Where both settings are available, cells report âWithout CIâ and âWith CIâ separately

or
<pre>
                    Whisper is a Transformer based encoder-decoder model, also referred to as a 
sequence-to-sequence
 model. There are two
flavours of Whisper model: English-only and multilingual. The English-only models were trained on the task of English 
speech recognition. The multilingual models were trained simultaneously on multilingual speech recognition and speech 
translation. For speech recognition, the model predicts transcriptions in the 
same
 language as the audio. For speech 
translation, the model predicts transcriptions to a 
different
 language to the audio.
</pre>
Another problem is that some input texts are too short to get classified and have a coherent meaning while combined with other text blocks. Example:
> Research on generative models.

or
>Probing and understanding the limitations and biases of generative models.

or
>Excluded uses are described below.
 
Some input texts contained blocks of code and metric tables at the same time. In all cases metric tables are unformatted and improper for a reader to comprehend.

An example of a text that contains eval dataset info but is meant for methodology are misclassified as eval dataset:
>MathVision, BabyVision, and CharXiv (RQ): Where both settings are available, cells report âWithout CIâ and âWith CIâ separately; otherwise, only the available setting is shown. A small number of incorrect ground-truth annotations in MathVision and CharXiv (RQ) were corrected following manual verification, and all reported scores on those benchmarks were computed using the corrected annotations.

There was also one case with a short text that was not present in the visible content of the model card in HF but it was inside the HTML and it was classified by matcher:
>Duplicated fromÂ sanchit-gandhi

