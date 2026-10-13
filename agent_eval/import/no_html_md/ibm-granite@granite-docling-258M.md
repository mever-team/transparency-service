Granite Docling is a multimodal Image-Text-to-Text model engineered for efficient document conversion. It preserves the core features of Docling while maintaining seamless integration with DoclingDocuments to ensure full compatibility. 
Granite Docling 258M builds upon the Idefics3 architecture, but introduces two key modifications: it replaces the vision encoder with siglip2-base-patch16-512 and substitutes the language model with a Granite 165M LLM. Try out our [Granite-Docling-258](https://huggingface.co/spaces/ibm-granite/granite-docling-258m-demo) demo today.
- **Developed by**: IBM Research
- **Model type**: Multi-modal model (image+text-to-text)
- **Language(s)**: English (NLP)
- **License**: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **Release Date**: September 17, 2025
Granite-docling-258M is fully integrated into the Docling pipelines, carrying over existing [features](https://huggingface.co/ds4sd/SmolDocling-256M-preview) while introducing a number of powerful new features, including:
- 🔢 Enhanced Equation Recognition: More accurate detection and formatting of mathematical formulas
- 🧩 Flexible Inference Modes: Choose between full-page inference, bbox-guided region inference
- 🧘 Improved Stability: Tends to avoid infinite loops more effectively
- 🧮 Enhanced Inline Equations: Better inline math recognition
- 🧾 Document Element QA: Answer questions about a document’s structure such as the presence and order of document elements
- 🌍 Japanese, Arabic and Chinese support (_experimental_)
The easiest way to use this model is through the [🐥Docling](https://github.com/docling-project/docling) library. It will automatically download this model and convert documents to various formats for you. 
Install the latest version of `docling` through pip, then use the following CLI command:
# Convert to HTML and Markdown:
docling --to html --to md --pipeline vlm --vlm-model granite_docling "https://arxiv.org/pdf/2501.17887" # accepts files, urls or directories
# Convert to HTML including layout visualization:
docling --to html_split_page --show-layout --pipeline vlm --vlm-model granite_docling "https://arxiv.org/pdf/2501.17887"
You can also set this model up within the Docling SDK:
from docling.datamodel import vlm_model_specs
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.vlm_pipeline import VlmPipeline
source = "https://arxiv.org/pdf/2501.17887"
###### USING SIMPLE DEFAULT VALUES
# - Using the transformers framework
converter = DocumentConverter(
        InputFormat.PDF: PdfFormatOption(
doc = converter.convert(source=source).document
print(doc.export_to_markdown())
###### USING MACOS MPS ACCELERATOR
# For more options see the compare_vlm_models.py example.
pipeline_options = VlmPipelineOptions(
    vlm_options=vlm_model_specs.GRANITEDOCLING_MLX,
converter = DocumentConverter(
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options,
doc = converter.convert(source=source).document
print(doc.export_to_markdown())
Alternatively, you can use bare **transformers**, **vllm**, **onnx** or **mlx-vlm** to perform inference, and [docling-core](https://github.com/docling-project/docling-core) APIs to convert results to variety of output formats (md, html, etc.):
📄 Single page image inference using plain 🤗 tranformers 🤖
from docling_core.types.doc import DoclingDocument
from docling_core.types.doc.document import DocTagsDocument
from transformers import AutoProcessor, AutoModelForVision2Seq
from transformers.image_utils import load_image
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
image = load_image("https://huggingface.co/ibm-granite/granite-docling-258M/resolve/main/assets/new_arxiv.png")
# Initialize processor and model
processor = AutoProcessor.from_pretrained("ibm-granite/granite-docling-258M")
model = AutoModelForVision2Seq.from_pretrained(
    "ibm-granite/granite-docling-258M",
    _attn_implementation="flash_attention_2" if DEVICE == "cuda" else "sdpa",
            {"type": "text", "text": "Convert this page to docling."}
prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
inputs = processor(text=prompt, images=[image], return_tensors="pt")
generated_ids = model.generate(**inputs, max_new_tokens=8192)
prompt_length = inputs.input_ids.shape[1]
trimmed_generated_ids = generated_ids[:, prompt_length:]
doctags = processor.batch_decode(
print(f"DocTags: \n{doctags}\n")
doctags_doc = DocTagsDocument.from_doctags_and_image_pairs([doctags], [image])
doc = DoclingDocument.load_from_doctags(doctags_doc, document_name="Document")
print(f"Markdown:\n{doc.export_to_markdown()}\n")
# Path("out/").mkdir(parents=True, exist_ok=True)
# output_path_html = Path("out/") / "example.html"
# doc.save_as_html(output_path_html)
# output_path_md = Path("out/") / "example.md"
# doc.save_as_markdown(output_path_md)
 🚀 Fast Batch Inference with VLLM
# place page images you want to convert into "img/" dir
from vllm import LLM, SamplingParams
from transformers import AutoProcessor
from docling_core.types.doc import DoclingDocument
from docling_core.types.doc.document import DocTagsDocument
MODEL_PATH = "ibm-granite/granite-docling-258M"
IMAGE_DIR = "img/"  # Place your page images here
PROMPT_TEXT = "Convert this page to docling."
            {"type": "text", "text": PROMPT_TEXT},
# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
llm = LLM(model=MODEL_PATH, revision="untied", limit_mm_per_prompt={"image": 1})
processor = AutoProcessor.from_pretrained(MODEL_PATH)
sampling_params = SamplingParams(
# Load and prepare all images and prompts up front
for img_file in sorted(os.listdir(IMAGE_DIR)):
    if img_file.lower().endswith((".png", ".jpg", ".jpeg")):
        img_path = os.path.join(IMAGE_DIR, img_file)
        with Image.open(img_path) as im:
        prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
        batched_inputs.append({"prompt": prompt, "multi_modal_data": {"image": image}})
        image_names.append(os.path.splitext(img_file)[0])
outputs = llm.generate(batched_inputs, sampling_params=sampling_params)
for img_fn, output, input_data in zip(image_names, outputs, batched_inputs):
    doctags = output.outputs[0].text
    output_path_dt = Path(OUTPUT_DIR) / f"{img_fn}.dt"
    output_path_md = Path(OUTPUT_DIR) / f"{img_fn}.md"
    with open(output_path_dt, "w", encoding="utf-8") as f:
    # Convert to DoclingDocument and save markdown
    doctags_doc = DocTagsDocument.from_doctags_and_image_pairs([doctags], [input_data["multi_modal_data"]["image"]])
    doc = DoclingDocument.load_from_doctags(doctags_doc, document_name="Document")
    doc.save_as_markdown(output_path_md)
print(f"Total time: {time.time() - start_time:.2f} sec")
💻 Local inference on Apple Silicon with MLX: [see here](https://huggingface.co/ibm-granite/granite-docling-258M-mlx)
ℹ️ If you see trouble running granite-docling with the codes above, check the troubleshooting section at the bottom ⬇️. 
Granite-Docling is designed to complement the Docling library, not replace it. It integrates as a component within larger Docling library, consolidating the functions of multiple single-purpose models into a single, compact VLM. 
However, Granite-Docling is **not** intended for general image understanding. For tasks focused solely on image-text input, we recommend using [Granite Vision models](https://huggingface.co/collections/ibm-granite/granite-vision-models-67b3bd4ff90c915ba4cd2800), which are purpose-built and optimized for image-text processing.
A comprehensive discussion of evaluation methods and findings has already been presented in our previous publication [[citation](https://arxiv.org/pdf/2503.11576)]. As this model is an update, we refer readers to that work for additional details.
The evaluation can be performed using the [docling-eval](https://github.com/docling-project/docling-eval) framework for the document related tasks, and [lmms-eval](https://github.com/EvolvingLMMs-Lab/lmms-eval) for MMStar and OCRBench.
0.1190.9470.9590.9410.8240.878
Table Recognition (FinTabNet 150dpi)
💻 Local inference on Apple Silicon with MLX: [see here](https://huggingface.co/ibm-granite/granite-docling-258M-mlx)
Convert table to OTSL. (Lysak et al., 2023)
OCR the text in a specific location: <loc_155><loc_233><loc_206><loc_237>
Identify element at: <loc_247><loc_482><loc_252><loc_486>
Find all 'text' elements on the page, retrieve all section headers.
Detect footer elements on the page.
The architecture of granite-docling-258m consists of the following components:
(1) Vision encoder: [siglip2-base-patch16-512](https://huggingface.co/google/siglip2-base-patch16-512).
(2) Vision-language connector: pixel shuffle projector (as in idefics3) 
(3) Large language model: Granite 165M.
We built upon [Idefics3](https://huggingface.co/docs/transformers/en/model_doc/idefics3) to train our model. We incorporated DocTags into our LLM’s supervised fine-tuning (SFT) data to help the model become familiar with the format, enabling faster convergence and mitigating issues previously observed with SmolDocling.
The model was trained using the [nanoVLM](https://github.com/huggingface/nanoVLM) framework, which provides a lightweight and efficient training setup for vision-language models
**Training Data**: Our training corpus consists of two principal sources: (1) publicly available datasets and (2) internally constructed synthetic datasets designed to elicit specific document understanding capabilities.
In particular, we incorporate:
* [**SynthCodeNet**](https://huggingface.co/datasets/ds4sd/SynthCodeNet) — a large-scale collection of synthetically rendered code snippets spanning over 50 programming languages
* [**SynthFormulaNet**](https://huggingface.co/datasets/ds4sd/SynthFormulaNet) — a dataset of synthetic mathematical expressions paired with ground-truth LaTeX representations
* [**SynthChartNet**](https://huggingface.co/datasets/ds4sd/SynthChartNet) — synthetic chart images annotated with structured table outputs
* [**DoclingMatix**](https://huggingface.co/datasets/HuggingFaceM4/DoclingMatix) — a curated corpus of real-world document pages sampled from diverse domains
**Infrastructure**: We train granite-docling-258m using IBM's super computing cluster, Blue Vela, which is outfitted with NVIDIA H100 GPUs. This cluster provides a scalable and efficient infrastructure for training our models over thousands of GPUs.
**Responsible Use and Limitations** Some use cases for Vision Language Models can trigger certain risks and ethical considerations, including but not limited to: bias and fairness, misinformation, and autonomous decision-making. 
Although our alignment processes include safety considerations, the model may in some cases produce inaccurate, biased, offensive or unwanted responses to user prompts. Additionally, whether smaller models may exhibit increased susceptibility 
to hallucination in generation scenarios due to their reduced sizes, which could limit their ability to generate coherent and contextually accurate responses, remains uncertain. This aspect is currently an active area of research, 
and we anticipate more rigorous exploration, comprehension, and mitigations in this domain. We urge the community to use granite-docling-258m in a responsible way and avoid any malicious utilization. We recommend using this model only as part of the Docling library.
More general vision tasks may pose higher inherent risks of triggering unwanted output. To enhance safety, we recommend using granite-docling-258m alongside Granite Guardian. Granite Guardian is a fine-tuned instruct model designed to detect and flag risks in prompts and responses across key dimensions outlined in the IBM AI Risk Atlas.
Its training, which includes both human-annotated and synthetic data informed by internal red-teaming, enables it to outperform similar open-source models on standard benchmarks, providing an additional layer of safety.
- ⭐️ Learn about the latest updates with Docling: https://docling-project.github.io/docling/#features
- 🚀 Get started with Docling concepts, integrations and tutorials: https://docling-project.github.io/docling/getting_started/
- 💡 Learn about the latest Granite learning resources: https://ibm.biz/granite-learning-resources
- 🖥️ Learn more about how to use Granite-Docling, explore the Docling library, and see what’s coming next for Docling in the release blog: https://ibm.com/new/announcements/granite-docling-end-to-end-document-conversion
1. You receive `AttributeError: 'LlamaModel' object has no attribute 'wte'` when launching the model through VLLM.
    With current versions of VLLM (including 0.10.2), support for tied weights as used in granite-docling is limited and breaks. We provide a version with untied weights on the `untied` branch of this model repo.
    To use the untied version, please pass the `revision` argument to VLLM:
    # Serve the model through VLLM
    $> vllm serve ibm-granite/granite-docling-258M --revision untied
    # If using the VLLM python SDK:
    llm = LLM(model=MODEL_PATH, revision="untied", limit_mm_per_prompt={"image": 1})
2. The model outputs only exclamation marks (i.e. "!!!!!!!!!!!!!!!").
   This is seen on older NVIDIA GPUs, such as the T4 GPU available in Google Colab, because it lacks support for `bfloat16` format.
   You can work around it by setting the `dtype` to `float32`.
    # Serve the model through VLLM
    $> vllm serve ibm-granite/granite-docling-258M --revision untied --dtype float32
    # If using the VLLM python SDK:
    llm = LLM(model=MODEL_PATH, revision="untied", limit_mm_per_prompt={"image": 1}, dtype="float32")