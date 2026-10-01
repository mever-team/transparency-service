dots.ocr: Multilingual Document Layout Parsing in a Single Vision-Language Model
[![Blog](https://img.shields.io/badge/Blog-View_on_GitHub-333.svg?logo=github)](https://github.com/rednote-hilab/dots.ocr/blob/master/assets/blog.md)
[![HuggingFace](https://img.shields.io/badge/HuggingFace%20Weights-black.svg?logo=HuggingFace)](https://huggingface.co/rednote-hilab/dots.ocr)
**dots.ocr** is a powerful, multilingual document parser that unifies layout detection and content recognition within a single vision-language model while maintaining good reading order. Despite its compact 1.7B-parameter LLM foundation, it achieves state-of-the-art(SOTA) performance.
1. **Powerful Performance:** **dots.ocr** achieves SOTA performance for text, tables, and reading order on [OmniDocBench](https://github.com/opendatalab/OmniDocBench), while delivering formula recognition results comparable to much larger models like Doubao-1.5 and gemini2.5-pro.
2. **Multilingual Support:** **dots.ocr** demonstrates robust parsing capabilities for low-resource languages, achieving decisive advantages across both layout detection and content recognition on our in-house multilingual documents benchmark.
3. **Unified and Simple Architecture:** By leveraging a single vision-language model, **dots.ocr** offers a significantly more streamlined architecture than conventional methods that rely on complex, multi-model pipelines. Switching between tasks is accomplished simply by altering the input prompt, proving that a VLM can achieve competitive detection results compared to traditional detection models like DocLayout-YOLO.
4.  **Efficient and Fast Performance:** Built upon a compact 1.7B LLM, **dots.ocr** provides faster inference speeds than many other high-performing models based on larger foundations.
from transformers import AutoModelForCausalLM, AutoProcessor, AutoTokenizer
from qwen_vl_utils import process_vision_info
from dots_ocr.utils import dict_promptmode_to_prompt
model_path = "./weights/DotsOCR"
model = AutoModelForCausalLM.from_pretrained(
    attn_implementation="flash_attention_2",
processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)
image_path = "demo/demo_image1.jpg"
prompt = """Please output the layout information from the PDF image, including each layout element's bbox, its category, and the corresponding text content within the bbox.
1. Bbox format: [x1, y1, x2, y2]
2. Layout Categories: The possible categories are ['Caption', 'Footnote', 'Formula', 'List-item', 'Page-footer', 'Page-header', 'Picture', 'Section-header', 'Table', 'Text', 'Title'].
3. Text Extraction & Formatting Rules:
    - Picture: For the 'Picture' category, the text field should be omitted.
    - Formula: Format its text as LaTeX.
    - Table: Format its text as HTML.
    - All Others (Text, Title, etc.): Format their text as Markdown.
    - The output text must be the original text from the image, with no translation.
    - All layout elements must be sorted according to human reading order.
5. Final Output: The entire output must be a single JSON object.
                {"type": "text", "text": prompt}
text = processor.apply_chat_template(
image_inputs, video_inputs = process_vision_info(messages)
# Inference: Generation of the output
generated_ids = model.generate(**inputs, max_new_tokens=24000)
    out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
output_text = processor.batch_decode(
    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
### Performance Comparison: dots.ocr vs. Competing Models
> - The EN, ZH metrics are the end2end evaluation results of [OmniDocBench](https://github.com/opendatalab/OmniDocBench), and Multilingual metric is the end2end evaluation results of dots.ocr-bench.
* ```2025.07.30 ``` 🚀 We release [dots.ocr](https://github.com/rednote-hilab/dots.ocr), — a multilingual documents parsing model based on 1.7b llm, with SOTA performance.
#### The end-to-end evaluation results of different tasks.
doubao-1-5-thinking-vision-pro-250428
#### The end-to-end text recognition performance across 9 PDF page types.
doubao-1-5-thinking-vision-pro-250428
> - The metrics are from [MonkeyOCR](https://github.com/Yuliang-Liu/MonkeyOCR), [OmniDocBench](https://github.com/opendatalab/OmniDocBench), and our own internal evaluations.
> - We delete the Page-header and Page-footer cells in the result markdown.
> - We use tikz_preprocess pipeline to upsample the images to dpi 200.
This is an inhouse benchmark which contain 1493 pdf images with 100 languages.
#### The end-to-end evaluation results of different tasks.
doubao-1-5-thinking-vision-pro-250428
> - We use the same metric calculation pipeline of [OmniDocBench](https://github.com/opendatalab/OmniDocBench).
> - We delete the Page-header and Page-footer cells in the result markdown.
> - prompt_layout_all_en for **parse all**, prompt_layout_only_en for **detection only**, please refer to [prompts](https://github.com/rednote-hilab/dots.ocr/blob/master/dots_ocr/utils/prompts.py)
> - The metrics are from [MonkeyOCR](https://github.com/Yuliang-Liu/MonkeyOCR), 
[olmocr](https://github.com/allenai/olmocr), and our own internal evaluations.
> - We delete the Page-header and Page-footer cells in the result markdown.
conda create -n dots_ocr python=3.12
git clone https://github.com/rednote-hilab/dots.ocr.git
# Install pytorch, see https://pytorch.org/get-started/previous-versions/ for your cuda version
pip install torch==2.7.0 torchvision==0.22.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/cu128
If you have trouble with the installation, try our [Docker Image](https://hub.docker.com/r/rednotehilab/dots.ocr) for an easier setup, and follow these steps:
git clone https://github.com/rednote-hilab/dots.ocr.git
> 💡**Note:** Please use a directory name without periods (e.g., `DotsOCR` instead of `dots.ocr`) for the model save path. This is a temporary workaround pending our integration with Transformers.
python3 tools/download_model.py
We highly recommend using vllm for deployment and inference. All of our evaluations results are based on vllm version 0.9.1.
The [Docker Image](https://hub.docker.com/r/rednotehilab/dots.ocr) is based on the official vllm image. You can also follow [Dockerfile](https://github.com/rednote-hilab/dots.ocr/blob/master/docker/Dockerfile) to build the deployment environment by yourself. 
# You need to register model to vllm at first
python3 tools/download_model.py
export hf_model_path=./weights/DotsOCR  # Path to your downloaded model weights, Please use a directory name without periods (e.g., `DotsOCR` instead of `dots.ocr`) for the model save path. This is a temporary workaround pending our integration with Transformers.
export PYTHONPATH=$(dirname "$hf_model_path"):$PYTHONPATH
sed -i '/^from vllm\.entrypoints\.cli\.main import main$/a\
from DotsOCR import modeling_dots_ocr_vllm' `which vllm`  # If you downloaded model weights by yourself, please replace `DotsOCR` by your model saved directory name, and remember to use a directory name without periods (e.g., `DotsOCR` instead of `dots.ocr`) 
CUDA_VISIBLE_DEVICES=0 vllm serve ${hf_model_path} --tensor-parallel-size 1 --gpu-memory-utilization 0.95  --chat-template-content-format string --served-model-name model --trust-remote-code
# If you get a ModuleNotFoundError: No module named 'DotsOCR', please check the note above on the saved model directory name.
python3 ./demo/demo_vllm.py --prompt_mode prompt_layout_all_en
from transformers import AutoModelForCausalLM, AutoProcessor, AutoTokenizer
from qwen_vl_utils import process_vision_info
from dots_ocr.utils import dict_promptmode_to_prompt
model_path = "./weights/DotsOCR"
model = AutoModelForCausalLM.from_pretrained(
    attn_implementation="flash_attention_2",
processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)
image_path = "demo/demo_image1.jpg"
prompt = """Please output the layout information from the PDF image, including each layout element's bbox, its category, and the corresponding text content within the bbox.
1. Bbox format: [x1, y1, x2, y2]
2. Layout Categories: The possible categories are ['Caption', 'Footnote', 'Formula', 'List-item', 'Page-footer', 'Page-header', 'Picture', 'Section-header', 'Table', 'Text', 'Title'].
3. Text Extraction & Formatting Rules:
    - Picture: For the 'Picture' category, the text field should be omitted.
    - Formula: Format its text as LaTeX.
    - Table: Format its text as HTML.
    - All Others (Text, Title, etc.): Format their text as Markdown.
    - The output text must be the original text from the image, with no translation.
    - All layout elements must be sorted according to human reading order.
5. Final Output: The entire output must be a single JSON object.
                {"type": "text", "text": prompt}
text = processor.apply_chat_template(
image_inputs, video_inputs = process_vision_info(messages)
# Inference: Generation of the output
generated_ids = model.generate(**inputs, max_new_tokens=24000)
    out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
output_text = processor.batch_decode(
    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
**Based on vLLM server**, you can parse an image or a pdf file using the following commands:
# Parse all layout info, both detection and recognition
python3 dots_ocr/parser.py demo/demo_image1.jpg
python3 dots_ocr/parser.py demo/demo_pdf1.pdf  --num_threads 64  # try bigger num_threads for pdf with a large number of pages
python3 dots_ocr/parser.py demo/demo_image1.jpg --prompt prompt_layout_only_en
# Parse text only, except Page-header and Page-footer
python3 dots_ocr/parser.py demo/demo_image1.jpg --prompt prompt_ocr
python3 dots_ocr/parser.py demo/demo_image1.jpg --prompt prompt_grounding_ocr --bbox 163 241 1536 705
1.  **Structured Layout Data** (`demo_image1.json`): A JSON file containing the detected layout elements, including their bounding boxes, categories, and extracted text.
2.  **Processed Markdown File** (`demo_image1.md`): A Markdown file generated from the concatenated text of all detected cells.
    *   An additional version, `demo_image1_nohf.md`, is also provided, which excludes page headers and footers for compatibility with benchmarks like Omnidocbench and olmOCR-bench.
3.  **Layout Visualization** (`demo_image1.jpg`): The original image with the detected layout bounding boxes drawn on it.
You can run the demo with the following command, or try directly at [live demo](https://dotsocr.xiaohongshu.com/)
We also provide a demo for grounding ocr:
python demo/demo_gradio_annotion.py
### Example for formula document
### Example for table document
### Example for multilingual document
We would like to thank [Qwen2.5-VL](https://github.com/QwenLM/Qwen2.5-VL), [aimv2](https://github.com/apple/ml-aim), [MonkeyOCR](https://github.com/Yuliang-Liu/MonkeyOCR), 
[OmniDocBench](https://github.com/opendatalab/OmniDocBench), [PyMuPDF](https://github.com/pymupdf/PyMuPDF), for providing code and models. 
We also thank [DocLayNet](https://github.com/DS4SD/DocLayNet), [M6Doc](https://github.com/HCIILAB/M6Doc), [CDLA](https://github.com/buptlihang/CDLA), [D4LA](https://github.com/AlibabaResearch/AdvancedLiterateMachinery) for providing valuable datasets. 
- **Complex Document Elements:**
  - **Table&Formula**: dots.ocr is not yet perfect for high-complexity tables and formula extraction.
  - **Picture**: Pictures in documents are currently not parsed.
- **Parsing Failures:** The model may fail to parse under certain conditions:
  - When the character-to-pixel ratio is excessively high. Try enlarging the image or increasing the PDF parsing DPI (a setting of 200 is recommended). However, please note that the model performs optimally on images with a resolution under 11289600 pixels.
  - Continuous special characters, such as ellipses (`...`) and underscores (`_`), may cause the prediction output to repeat endlessly. In such scenarios, consider using alternative prompts like `prompt_layout_only_en`, `prompt_ocr`, or `prompt_grounding_ocr` ([details here](https://github.com/rednote-hilab/dots.ocr/blob/master/dots_ocr/utils/prompts.py)).
- **Performance Bottleneck:** Despite its 1.7B parameter LLM foundation, **dots.ocr** is not yet optimized for high-throughput processing of large PDF volumes. 
We are committed to achieving more accurate table and formula parsing, as well as enhancing the model's OCR capabilities for broader generalization, all while aiming for **a more powerful, more efficient model**. Furthermore, we are actively considering the development of **a more general-purpose perception model** based on Vision-Language Models (VLMs), which would integrate general detection, image captioning, and OCR tasks into a unified framework. **Parsing the content of the pictures in the documents** is also a key priority for our future work.
We believe that collaboration is the key to tackling these exciting challenges. If you are passionate about advancing the frontiers of document intelligence and are interested in contributing to these future endeavors, we would love to hear from you. Please reach out to us via email at: [yanqing4@xiaohongshu.com].