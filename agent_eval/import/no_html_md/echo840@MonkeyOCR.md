MonkeyOCR: Document Parsing with a Structure-Recognition-Relation Triplet Paradigm
[![arXiv](https://img.shields.io/badge/Arxiv-MonkeyOCR-b31b1b.svg?logo=arXiv)](https://arxiv.org/abs/2506.05218)
[![HuggingFace](https://img.shields.io/badge/HuggingFace%20Weights-black.svg?logo=HuggingFace)](https://huggingface.co/echo840/MonkeyOCR)
[![GitHub issues](https://img.shields.io/github/issues/Yuliang-Liu/MonkeyOCR?color=critical&label=Issues)](https://github.com/Yuliang-Liu/MonkeyOCR/issues?q=is%3Aopen+is%3Aissue)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/Yuliang-Liu/MonkeyOCR?color=success&label=Issues)](https://github.com/Yuliang-Liu/MonkeyOCR/issues?q=is%3Aissue+is%3Aclosed)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow)](https://github.com/Yuliang-Liu/MonkeyOCR/blob/main/LICENSE.txt)
[![GitHub views](https://komarev.com/ghpvc/?username=Yuliang-Liu&repo=MonkeyOCR&color=brightgreen&label=Views)](https://github.com/Yuliang-Liu/MonkeyOCR)
> **MonkeyOCR: Document Parsing with a Structure-Recognition-Relation Triplet Paradigm**
> Zhang Li, Yuliang Liu, Qiang Liu, Zhiyin Ma, Ziyang Zhang, Shuo Zhang, Zidun Guo, Jiarui Zhang, Xinyu Wang, Xiang Bai 
[![arXiv](https://img.shields.io/badge/Arxiv-b31b1b.svg?logo=arXiv)](https://arxiv.org/abs/2506.05218) 
[![Source_code](https://img.shields.io/badge/Code-Available-white)](README.md)
[![Model Weight](https://img.shields.io/badge/HuggingFace-gray)](https://huggingface.co/echo840/MonkeyOCR)
[![Model Weight](https://img.shields.io/badge/ModelScope-green)](https://modelscope.cn/models/l1731396519/MonkeyOCR)
[![Public Courses](https://img.shields.io/badge/Openbayes-yellow)](https://openbayes.com/console/public/tutorials/91ESrGvEvBq)
[![Demo](https://img.shields.io/badge/Demo-blue)](http://vlrlabmonkey.xyz:7685/)
MonkeyOCR adopts a Structure-Recognition-Relation (SRR) triplet paradigm, which simplifies the multi-tool pipeline of modular approaches while avoiding the inefficiency of using large multimodal models for full-page document processing.
1. MonkeyOCR-pro-1.2B surpasses MonkeyOCR-3B by 7.4% on Chinese documents.
2. MonkeyOCR-pro-1.2B delivers approximately a 36% speed improvement over MonkeyOCR-pro-3B, with approximately 1.6% drop in performance.
3. On olmOCR-Bench, MonkeyOCR-pro-1.2B outperforms Nanonets-OCR-3B by 7.3%.
4. On OmniDocBench, MonkeyOCR-pro-3B achieves the best overall performance on both English and Chinese documents, outperforming even closed-source and extra-large open-source VLMs such as Gemini 2.0-Flash, Gemini 2.5-Pro, Qwen2.5-VL-72B, GPT-4o, and InternVL3-78B.
### Comparing MonkeyOCR with closed-source and extra large open-source VLMs.
## Inference Speed (Pages/s) on Different GPUs and [PDF](https://drive.google.com/drive/folders/1geumlJmVY7UUKdr8324sYZ0FHSAElh7m?usp=sharing) Page Counts
## VLM OCR Speed (Pages/s) on Different GPUs and [PDF](https://drive.google.com/drive/folders/1geumlJmVY7UUKdr8324sYZ0FHSAElh7m?usp=sharing) Page Counts
Due to the limited types of GPUs available to us, we may not be able to provide highly accurate hardware specifications. We've tested the model on GPUs such as the 3090, 4090, A6000, H800, A100, and even the 4060 with 8GB of VRAM (suitable for deploying quantized 3B model and 1.2B model). We are very grateful for the feedback and contributions from the open-source community, who have also successfully run the model on [50-series GPUs](https://github.com/Yuliang-Liu/MonkeyOCR/issues/90), [H200](https://github.com/Yuliang-Liu/MonkeyOCR/issues/151), [L20](https://github.com/Yuliang-Liu/MonkeyOCR/issues/133), [V100](https://github.com/Yuliang-Liu/MonkeyOCR/issues/144), [2080 Ti](https://github.com/Yuliang-Liu/MonkeyOCR/pull/1) and [npu](https://github.com/Yuliang-Liu/MonkeyOCR/pull/226/files).
* ```2025.07.10 ``` 🚀 We release [MonkeyOCR-pro-1.2B](https://huggingface.co/echo840/MonkeyOCR-pro-1.2B), — a leaner and faster version model that outperforms our previous 3B version in accuracy, speed, and efficiency.
* ```2025.06.12 ``` 🚀 The model’s trending on [Hugging Face](https://huggingface.co/models?sort=trending). Thanks for the love!
* ```2025.06.05 ``` 🚀 We release [MonkeyOCR](https://huggingface.co/echo840/MonkeyOCR), an English and Chinese documents parsing model.
See the [installation guide](https://github.com/Yuliang-Liu/MonkeyOCR/blob/main/docs/install_cuda_pp.md#install-with-cuda-support) to set up your environment.
Download our model from Huggingface.
python tools/download_model.py -n MonkeyOCR-pro-3B  # or MonkeyOCR
You can also download our model from ModelScope.
python tools/download_model.py -t modelscope -n MonkeyOCR-pro-3B  # or MonkeyOCR
You can parse a file or a directory containing PDFs or images using the following commands:
# Replace input_path with the path to a PDF or image or directory
# Parse files in a dir with specific group page num
python parse.py input_path -g 20
# Single-task recognition (outputs markdown only)
python parse.py input_path -t text/formula/table
# Parse PDFs in input_path and split results by pages
# Specify output directory and model config file
python parse.py input_path -o ./output -c config.yaml
python parse.py input.pdf                           # Parse single PDF file
python parse.py input.pdf -o ./output               # Parse with custom output dir
python parse.py input.pdf -s                        # Parse PDF with page splitting
python parse.py image.jpg                           # Parse single image file
python parse.py image.jpg -t text                   # Text recognition from image
python parse.py image.jpg -t formula                # Formula recognition from image
python parse.py image.jpg -t table                  # Table recognition from image
python parse.py document.pdf -t text                # Text recognition from all PDF pages
# Folder processing (all files individually)
python parse.py /path/to/folder                     # Parse all files in folder
python parse.py /path/to/folder -s                  # Parse with page splitting
python parse.py /path/to/folder -t text             # Single task recognition for all files
# Multi-file grouping (batch processing by page count)
python parse.py /path/to/folder -g 5                # Group files with max 5 total pages
python parse.py /path/to/folder -g 10 -s            # Group files with page splitting
python parse.py /path/to/folder -g 8 -t text        # Group files for single task recognition
python parse.py input.pdf -c model_configs.yaml     # Custom model configuration
python parse.py /path/to/folder -g 15 -s -o ./out   # Group files, split pages, custom output
python parse.py input.pdf --pred-abandon            # Enable predicting abandon elements
  python parse.py /path/to/folder -g 10 -m            # Group files and merge text blocks in output
MonkeyOCR mainly generates three types of output files:
1. **Processed Markdown File** (`your.md`): The final parsed document content in markdown format, containing text, formulas, tables, and other structured elements.
2. **Layout Results** (`your_layout.pdf`): The layout results drawed on origin PDF.
2. **Intermediate Block Results** (`your_middle.json`): A JSON file containing detailed information about all detected blocks, including:
   - Block coordinates and positions
   - Block content and type information
   - Relationship information between blocks
These files provide both the final formatted output and detailed intermediate results for further analysis or processing.
Once the demo is running, you can access it at http://localhost:7860.
You can start the MonkeyOCR FastAPI service with the following command:
uvicorn api.main:app --port 8000
Once the API service is running, you can access the API documentation at http://localhost:8000/docs to explore available endpoints.
> To improve API concurrency performance, consider configuring the inference backend as `lmdeploy_queue` or `vllm_queue`.
1. Navigate to the `docker` directory:
2. **Prerequisite:** Ensure NVIDIA GPU support is available in Docker (via `nvidia-docker2`).
   If GPU support is not enabled, run the following to set up the environment:
   docker compose build monkeyocr
> If your GPU is from the 20/30/40-series, V100, L20/L40 or similar, please build the patched Docker image for LMDeploy compatibility:
> docker compose build monkeyocr-fix
> Otherwise, you may encounter the following error: `triton.runtime.errors.OutOfResources: out of resource: shared memory`
4. Run the container with the Gradio demo (accessible on port 7860):
   docker compose up monkeyocr-demo
   Alternatively, start an interactive development environment:
   docker compose run --rm monkeyocr-dev
5. Run the FastAPI service (accessible on port 7861):
   docker compose up monkeyocr-api
   Once the API service is running, you can access the API documentation at http://localhost:7861/docs to explore available endpoints.
See the [windows support guide](docs/windows_support.md) for details.
This model can be quantized using AWQ. Follow the instructions in the [quantization guide](docs/Quantization.md).
Here are the evaluation results of our model on OmniDocBench. MonkeyOCR-3B uses DocLayoutYOLO as the structure detection model, while MonkeyOCR-3B* uses our trained structure detection model with improved Chinese performance.
### 1. The end-to-end evaluation results of different tasks.
### 2. The end-to-end text recognition performance across 9 PDF page types.
### 3. The evaluation results of olmOCR-bench.
Get a Quick Hands-On Experience with Our Demo:  http://vlrlabmonkey.xyz:7685 (The latest model is available for selection)
> Our demo is simple and easy to use:
> 2. Click “Parse (解析)” to let the model perform structure detection, content recognition, and relationship prediction on the input document. The final output will be a markdown-formatted version of the document.
> 3. Select a prompt and click “Test by prompt” to let the model perform content recognition on the image based on the selected prompt.
### Example for formula document
### Example for table document
### Example for financial report
If you wish to refer to the baseline results published here, please use the following BibTeX entries:
@misc{li2025monkeyocrdocumentparsingstructurerecognitionrelation,
      title={MonkeyOCR: Document Parsing with a Structure-Recognition-Relation Triplet Paradigm}, 
      author={Zhang Li and Yuliang Liu and Qiang Liu and Zhiyin Ma and Ziyang Zhang and Shuo Zhang and Zidun Guo and Jiarui Zhang and Xinyu Wang and Xiang Bai},
      url={https://arxiv.org/abs/2506.05218}, 
We would like to thank [MinerU](https://github.com/opendatalab/MinerU), [DocLayout-YOLO](https://github.com/opendatalab/DocLayout-YOLO), [PyMuPDF](https://github.com/pymupdf/PyMuPDF), [layoutreader](https://github.com/ppaanngggg/layoutreader), [Qwen2.5-VL](https://github.com/QwenLM/Qwen2.5-VL), [LMDeploy](https://github.com/InternLM/lmdeploy), [PP-StructureV3](https://github.com/PaddlePaddle/PaddleOCR), [PP-DocLayout_plus-L](https://huggingface.co/PaddlePaddle/PP-DocLayout_plus-L), and [InternVL3](https://github.com/OpenGVLab/InternVL) for providing base code and models, as well as their contributions to this field. We also thank [M6Doc](https://github.com/HCIILAB/M6Doc), [DocLayNet](https://github.com/DS4SD/DocLayNet), [CDLA](https://github.com/buptlihang/CDLA), [D4LA](https://github.com/AlibabaResearch/AdvancedLiterateMachinery), [DocGenome](https://github.com/Alpha-Innovator/DocGenome), [PubTabNet](https://github.com/ibm-aur-nlp/PubTabNet), and [UniMER-1M](https://github.com/opendatalab/UniMERNet) for providing valuable datasets. We also thank everyone who contributed to this open-source effort.
Currently, MonkeyOCR do not yet fully support for photographed text, handwritten content, Traditional Chinese characters, or multilingual text. We plan to consider adding support for these features in future public releases. Additionally, our model is deployed on a single GPU, so if too many users upload files at the same time, issues like “This application is currently busy” may occur. The processing time shown on the demo page does not reflect computation time alone—it also includes result uploading and other overhead. During periods of high traffic, this time may be longer. The inference speeds of MonkeyOCR, MinerU, and Qwen2.5 VL-7B were measured on an H800 GPU.
Please don’t hesitate to share your valuable feedback — it’s a key motivation that drives us to continuously improve our framework. Note: Our model is intended for academic research and non-commercial use only. If you are interested in faster (smaller) or stronger one, please contact us at xbai@hust.edu.cn or ylliu@hust.edu.cn.