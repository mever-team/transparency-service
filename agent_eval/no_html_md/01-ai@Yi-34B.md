Building the Next Generation of Open-Source and Bilingual LLMs
🤗 Hugging Face • 🤖 ModelScope • ✡️ WiseModel
    👩‍🚀 Ask questions or discuss ideas on  GitHub 
    👋 Join us on  👾 Discord  or  💬 WeChat 
  - [Introduction](#introduction)
- [How to use Yi?](#how-to-use-yi)
    - [Choose your path](#choose-your-path)
    - [docker](#quick-start---docker)
    - [llama.cpp](#quick-start---llamacpp)
    - [conda-lock](#quick-start---conda-lock)
  - [Quantization](#quantization)
  - [Learning hub](#learning-hub)
      - [Quantization](#quantization-1)
      - [Fine-tuning](#fine-tuning-1)
    - [Base model performance](#base-model-performance)
    - [Chat model performance](#chat-model-performance)
- [Who can use Yi?](#who-can-use-yi)
  - [Acknowledgements](#acknowledgments)
- 🤖 The Yi series models are the next generation of open-source large language models trained from scratch by [01.AI](https://01.ai/).
- 🙌 Targeted as a bilingual language model and trained on 3T multilingual corpus, the Yi series models become one of the strongest LLM worldwide, showing promise in language understanding, commonsense reasoning, reading comprehension, and more. For example,
  - Yi-34B-Chat model **landed in second place (following GPT-4 Turbo)**, outperforming other LLMs (such as GPT-4, Mixtral, Claude) on the AlpacaEval Leaderboard (based on data available up to January 2024).
  - Yi-34B model **ranked first among all existing open-source models** (such as Falcon-180B, Llama-70B, Claude) in **both English and Chinese** on various benchmarks, including Hugging Face Open LLM Leaderboard (pre-trained) and C-Eval (based on data available up to November 2023).
  - 🙏 (Credits to Llama) Thanks to the Transformer and Llama open-source communities, as they reduce the efforts required to build from scratch and enable the utilization of the same tools within the AI ecosystem.  
   If you're interested in Yi's adoption of Llama architecture and license usage policy, see  Yi's relation with Llama. ⬇️  
> The Yi series models adopt the same model architecture as Llama but are **NOT** derivatives of Llama.
- Both Yi and Llama are based on the Transformer structure, which has been the standard architecture for large language models since 2018.
- Grounded in the Transformer architecture, Llama has become a new cornerstone for the majority of state-of-the-art open-source models due to its excellent stability, reliable convergence, and robust compatibility. This positions Llama as the recognized foundational framework for models including Yi.
- Thanks to the Transformer and Llama architectures, other models can leverage their power, reducing the effort required to build from scratch and enabling the utilization of the same tools within their ecosystems.
- However, the Yi series models are NOT derivatives of Llama, as they do not use Llama's weights.
  - As Llama's structure is employed by the majority of open-source models, the key factors of determining model performance are training datasets, training pipelines, and training infrastructure.
  - Developing in a unique and proprietary way, Yi has independently created its own high-quality training datasets, efficient training pipelines, and robust training infrastructure entirely from the ground up. This effort has led to excellent performance with Yi series models ranking just behind GPT4 and surpassing Llama on the [Alpaca Leaderboard in Dec 2023](https://tatsu-lab.github.io/alpaca_eval/). 
🔥 2024-07-29: The Yi Cookbook 1.0  is released, featuring tutorials and examples in both Chinese and English.
🎯 2024-05-13: The Yi-1.5 series models  are open-sourced, further improving coding, math, reasoning, and instruction-following abilities.
🎯 2024-03-16: The Yi-9B-200K is open-sourced and available to the public.
🎯 2024-03-08: Yi Tech Report is published! 
🔔 2024-03-07: The long text capability of the Yi-34B-200K has been enhanced. 
In the "Needle-in-a-Haystack" test, the Yi-34B-200K's performance is improved by 10.5%, rising from 89.3% to an impressive 99.8%. We continue to pre-train the model on 5B tokens long-context data mixture and demonstrate a near-all-green performance.
🎯 2024-03-06: The Yi-9B is open-sourced and available to the public.
Yi-9B stands out as the top performer among a range of similar-sized open-source models (including Mistral-7B, SOLAR-10.7B, Gemma-7B, DeepSeek-Coder-7B-Base-v1.5 and more), particularly excelling in code, math, common-sense reasoning, and reading comprehension.
🎯 2024-01-23: The Yi-VL models, Yi-VL-34B and Yi-VL-6B, are open-sourced and available to the public.
Yi-VL-34B has ranked first among all existing open-source models in the latest benchmarks, including MMMU and CMMMU (based on data available up to January 2024).
🎯 2023-11-23: Chat models are open-sourced and available to the public.
This release contains two chat models based on previously released base models, two 8-bit models quantized by GPTQ, and two 4-bit models quantized by AWQ.
You can try some of them interactively at:
- [Hugging Face](https://huggingface.co/spaces/01-ai/Yi-34B-Chat)
- [Replicate](https://replicate.com/01-ai)
🔔 2023-11-23: The Yi Series Models Community License Agreement is updated to v2.1.
🔥 2023-11-08: Invited test of Yi-34B chat model.
- [English](https://cn.mikecrm.com/l91ODJf)
- [Chinese](https://cn.mikecrm.com/gnEZjiQ)
🎯 2023-11-05: The base models, Yi-6B-200K and Yi-34B-200K, are open-sourced and available to the public.
This release contains two base models with the same parameter sizes as the previous
release, except that the context window is extended to 200K.
🎯 2023-11-02: The base models, Yi-6B and Yi-34B, are open-sourced and available to the public.
The first public release contains two bilingual (English/Chinese) base models
with the parameter sizes of 6B and 34B.  Both of them are trained with 4K
sequence length and can be extended to 32K during inference time.
Yi models come in multiple sizes and cater to different use cases. You can also fine-tune Yi models to meet your specific requirements. 
If you want to deploy Yi models, make sure you meet the [software and hardware requirements](#deployment).
 - 4-bit series models are quantized by AWQ.  - 8-bit series models are quantized by GPTQ  - All quantized models have a low barrier to use since they can be deployed on consumer-grade GPUs (e.g., 3090, 4090). 
 - 200k is roughly equivalent to 400,000 Chinese characters.   - If you want to use the previous version of the Yi-34B-200K (released on Nov 5, 2023), run `git checkout 069cd341d60f4ce4b07ec394e82b79e94f656cf` to download the weight. 
They are suitable for personal and academic use.
It is the best at coding and math in the Yi series models.
Yi-9B is continuously trained based on Yi-6B, using 0.8T tokens.
They are suitable for personal, academic, and commercial (particularly for small and medium-sized enterprises) purposes. It's a cost-effective solution that's affordable and equipped with emergent ability.
  For chat model limitations, see the explanations below. ⬇️
The released chat model has undergone exclusive training using Supervised Fine-Tuning (SFT). Compared to other standard chat models, our model produces more diverse responses, making it suitable for various downstream tasks, such as creative scenarios. Furthermore, this diversity is expected to enhance the likelihood of generating higher quality responses, which will be advantageous for subsequent Reinforcement Learning (RL) training.
    However, this higher diversity might amplify certain existing issues, including:
      Hallucination: This refers to the model generating factually incorrect or nonsensical information. With the model's responses being more varied, there's a higher chance of hallucination that are not based on accurate data or logical reasoning.
Non-determinism in re-generation: When attempting to regenerate or sample responses, inconsistencies in the outcomes may occur. The increased diversity can lead to varying results even under similar input conditions.
Cumulative Error: This occurs when errors in the model's responses compound over time. As the model generates more diverse responses, the likelihood of small inaccuracies building up into larger errors increases, especially in complex tasks like extended reasoning, mathematical problem-solving, etc.
To achieve more coherent and consistent responses, it is advisable to adjust generation configuration parameters such as temperature, top_p, or top_k. These adjustments can help in the balance between creativity and coherence in the model's outputs.
  - [Choose your path](#choose-your-path)
  - [docker](#quick-start---docker)
  - [conda-lock](#quick-start---conda-lock)
  - [llama.cpp](#quick-start---llamacpp)
- [Quantization](#quantization)
- [Learning hub](#learning-hub)
> **💡 Tip**: If you want to get started with the Yi model and explore different methods for inference, check out the [Yi Cookbook](https://github.com/01-ai/Yi/tree/main/Cookbook).
Select one of the following paths to begin your journey with Yi!
 ![Quick start - Choose your path](https://github.com/01-ai/Yi/blob/main/assets/img/quick_start_path.png?raw=true)
If you prefer to deploy Yi models locally, 
  - 🙋‍♀️ and you have **sufficient** resources (for example, NVIDIA A800 80GB), you can choose one of the following methods:
    - [Docker](#quick-start---docker)
    - [conda-lock](#quick-start---conda-lock)
  - 🙋‍♀️ and you have **limited** resources (for example, a MacBook Pro), you can use [llama.cpp](#quick-start---llamacpp).
#### 🎯 Not to deploy Yi locally
If you prefer not to deploy Yi models locally, you can explore Yi's capabilities using any of the following options.
If you want to explore more features of Yi, you can adopt one of these methods:
  - [Early access has been granted](https://x.com/01AI_Yi/status/1735728934560600536?s=20) to some applicants. Stay tuned for the next round of access!
- [Yi APIs](https://replicate.com/01-ai/yi-34b-chat/api?tab=nodejs) (Replicate)
##### 🙋‍♀️ Run Yi in playground
If you want to chat with Yi with more customizable options (e.g., system prompt, temperature, repetition penalty, etc.), you can try one of the following options:
  - [Yi-34B-Chat-Playground](https://platform.lingyiwanwu.com/prompt/playground) (Yi official)
    - Access is available through a whitelist. Welcome to apply (fill out a form in [English](https://cn.mikecrm.com/l91ODJf) or [Chinese](https://cn.mikecrm.com/gnEZjiQ)).
  - [Yi-34B-Chat-Playground](https://replicate.com/01-ai/yi-34b-chat) (Replicate) 
 If you want to chat with Yi, you can use one of these online services, which offer a similar user experience:
- [Yi-34B-Chat](https://huggingface.co/spaces/01-ai/Yi-34B-Chat) (Yi official on Hugging Face)
  - No registration is required.
- [Yi-34B-Chat](https://platform.lingyiwanwu.com/) (Yi official beta)
  - Access is available through a whitelist. Welcome to apply (fill out a form in [English](https://cn.mikecrm.com/l91ODJf) or [Chinese](https://cn.mikecrm.com/gnEZjiQ)).
This tutorial guides you through every step of running **Yi-34B-Chat locally on an A800 (80G)** and then performing inference.
- Make sure Python 3.10 or a later version is installed.
- If you want to run other Yi models, see [software and hardware requirements](#deployment).
#### Step 1: Prepare your environment 
To set up the environment and install the required packages, execute the following command.
git clone https://github.com/01-ai/Yi.git
pip install -r requirements.txt
#### Step 2: Download the Yi model
You can download the weights and tokenizer of Yi models from the following sources:
- [Hugging Face](https://huggingface.co/01-ai)
- [ModelScope](https://www.modelscope.cn/organization/01ai/)
- [WiseModel](https://wisemodel.cn/organization/01.AI)
#### Step 3: Perform inference
You can perform inference with Yi chat or base models as below.
##### Perform inference with Yi chat model
1. Create a file named  `quick_start.py` and copy the following content to it.
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
    # Since transformers 4.35.0, the GPT-Q/AWQ model can be loaded using AutoModelForCausalLM.
    model = AutoModelForCausalLM.from_pretrained(
        {"role": "user", "content": "hi"}
    input_ids = tokenizer.apply_chat_template(conversation=messages, tokenize=True, add_generation_prompt=True, return_tensors='pt')
    output_ids = model.generate(input_ids.to('cuda'))
    response = tokenizer.decode(output_ids[0][input_ids.shape[1]:], skip_special_tokens=True)
    # Model response: "Hello! How can I assist you today?"
    Then you can see an output similar to the one below. 🥳
    Hello! How can I assist you today?
##### Perform inference with Yi base model
  The steps are similar to [pip - Perform inference with Yi chat model](#perform-inference-with-yi-chat-model).
  You can use the existing file [`text_generation.py`](https://github.com/01-ai/Yi/tree/main/demo).
  python demo/text_generation.py  --model 
  Then you can see an output similar to the one below. 🥳
  **Prompt**: Let me tell you an interesting story about cat Tom and mouse Jerry,
  **Generation**: Let me tell you an interesting story about cat Tom and mouse Jerry, which happened in my childhood. My father had a big house with two cats living inside it to kill mice. One day when I was playing at home alone, I found one of the tomcats lying on his back near our kitchen door, looking very much like he wanted something from us but couldn’t get up because there were too many people around him! He kept trying for several minutes before finally giving up...
  from transformers import AutoModelForCausalLM, AutoTokenizer
  model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, torch_dtype="auto")
  tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, use_fast=False)
  input_text = "# write the quick sort algorithm"
  inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
  outputs = model.generate(**inputs, max_length=256)
  print(tokenizer.decode(outputs[0], skip_special_tokens=True))
  # write the quick sort algorithm
      left = [x for x in arr if x < pivot]
      middle = [x for x in arr if x == pivot]
      right = [x for x in arr if x > pivot]
      return quick_sort(left) + middle + quick_sort(right)
  # test the quick sort algorithm
  print(quick_sort([3, 6, 8, 10, 1, 2, 1]))
 Run Yi-34B-chat locally with Docker: a step-by-step guide. ⬇️
This tutorial guides you through every step of running Yi-34B-Chat on an A800 GPU or 4*4090 locally and then performing inference.
Make sure you've installed Docker and nvidia-container-toolkit.
Alternatively, you can pull the Yi Docker image from registry.lingyiwanwu.com/ci/01-ai/yi:latest.
You can perform inference with Yi chat or base models as below.
Perform inference with Yi chat model
The steps are similar to pip - Perform inference with Yi chat model.
Note that the only difference is to set model_path = '<your-model-mount-path>' instead of model_path = '<your-model-path>'.
Perform inference with Yi base model
The steps are similar to pip - Perform inference with Yi base model.
Note that the only difference is to set --model <your-model-mount-path>' instead of model <your-model-path>.
You can use conda-lock to generate fully reproducible lock files for conda environments. ⬇️
You can refer to conda-lock.yml  for the exact versions of the dependencies. Additionally, you can utilize micromamba for installing these dependencies.
To install the dependencies, follow these steps:
1. Install micromamba by following the instructions available here.
2. Execute micromamba install -y -n yi -f conda-lock.yml to create a conda environment named yi and install the necessary dependencies.
The following tutorial  will guide you through every step of running a quantized model (Yi-chat-6B-2bits) locally and then performing inference.
 Run Yi-chat-6B-2bits locally with llama.cpp: a step-by-step guide. ⬇️
This tutorial guides you through every step of running a quantized model (Yi-chat-6B-2bits) locally and then performing inference.
- [Step 0: Prerequisites](#step-0-prerequisites)
- [Step 1: Download llama.cpp](#step-1-download-llamacpp)
- [Step 2: Download Yi model](#step-2-download-yi-model)
- [Step 3: Perform inference](#step-3-perform-inference)
- This tutorial assumes you use a MacBook Pro with 16GB of memory and an Apple M2 Pro chip.
- Make sure [`git-lfs`](https://git-lfs.com/) is installed on your machine.
#### Step 1: Download `llama.cpp`
To clone the [`llama.cpp`](https://github.com/ggerganov/llama.cpp) repository, run the following command.
git clone git@github.com:ggerganov/llama.cpp.git
#### Step 2: Download Yi model
2.1 To clone [XeIaso/yi-chat-6B-GGUF](https://huggingface.co/XeIaso/yi-chat-6B-GGUF/tree/main) with just pointers, run the following command.
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/XeIaso/yi-chat-6B-GGUF
2.2 To download a quantized Yi model ([yi-chat-6b.Q2_K.gguf](https://huggingface.co/XeIaso/yi-chat-6B-GGUF/blob/main/yi-chat-6b.Q2_K.gguf)), run the following command.
git-lfs pull --include yi-chat-6b.Q2_K.gguf
#### Step 3: Perform inference
To perform inference with the Yi model, you can use one of the following methods.
- [Method 1: Perform inference in terminal](#method-1-perform-inference-in-terminal)
- [Method 2: Perform inference in web](#method-2-perform-inference-in-web)
##### Method 1: Perform inference in terminal
To compile `llama.cpp` using 4 threads and then conduct inference, navigate to the `llama.cpp` directory, and run the following command.
> - Replace `/Users/yu/yi-chat-6B-GGUF/yi-chat-6b.Q2_K.gguf` with the actual path of your model.
> - By default, the model operates in completion mode.
> - For additional output customization options (for example, system prompt, temperature, repetition penalty, etc.), run `./main -h` to check detailed descriptions and usage.
make -j4 && ./main -m /Users/yu/yi-chat-6B-GGUF/yi-chat-6b.Q2_K.gguf -p "How do you feed your pet fox? Please answer this question in 6 simple steps:\nStep 1:" -n 384 -e
How do you feed your pet fox? Please answer this question in 6 simple steps:
Step 1: Select the appropriate food for your pet fox. You should choose high-quality, balanced prey items that are suitable for their unique dietary needs. These could include live or frozen mice, rats, pigeons, or other small mammals, as well as fresh fruits and vegetables.
Step 2: Feed your pet fox once or twice a day, depending on the species and its individual preferences. Always ensure that they have access to fresh water throughout the day.
Step 3: Provide an appropriate environment for your pet fox. Ensure it has a comfortable place to rest, plenty of space to move around, and opportunities to play and exercise.
Step 4: Socialize your pet with other animals if possible. Interactions with other creatures can help them develop social skills and prevent boredom or stress.
Step 5: Regularly check for signs of illness or discomfort in your fox. Be prepared to provide veterinary care as needed, especially for common issues such as parasites, dental health problems, or infections.
Step 6: Educate yourself about the needs of your pet fox and be aware of any potential risks or concerns that could affect their well-being. Regularly consult with a veterinarian to ensure you are providing the best care.
Now you have successfully asked a question to the Yi model and got an answer! 🥳
##### Method 2: Perform inference in web
1. To initialize a lightweight and swift chatbot, run the following command.
    ./server --ctx-size 2048 --host 0.0.0.0 --n-gpu-layers 64 --model /Users/yu/yi-chat-6B-GGUF/yi-chat-6b.Q2_K.gguf
    Then you can get an output like this:
    llama_new_context_with_model: n_ctx      = 2048
    llama_new_context_with_model: freq_base  = 5000000.0
    llama_new_context_with_model: freq_scale = 1
    ggml_metal_init: found device: Apple M2 Pro
    ggml_metal_init: picking default device: Apple M2 Pro
    ggml_metal_init: ggml.metallib not found, loading from source
    ggml_metal_init: GGML_METAL_PATH_RESOURCES = nil
    ggml_metal_init: loading '/Users/yu/llama.cpp/ggml-metal.metal'
    ggml_metal_init: GPU name:   Apple M2 Pro
    ggml_metal_init: GPU family: MTLGPUFamilyApple8 (1008)
    ggml_metal_init: hasUnifiedMemory              = true
    ggml_metal_init: recommendedMaxWorkingSetSize  = 11453.25 MB
    ggml_metal_init: maxTransferRate               = built-in GPU
    ggml_backend_metal_buffer_type_alloc_buffer: allocated buffer, size =   128.00 MiB, ( 2629.44 / 10922.67)
    llama_new_context_with_model: KV self size  =  128.00 MiB, K (f16):   64.00 MiB, V (f16):   64.00 MiB
    ggml_backend_metal_buffer_type_alloc_buffer: allocated buffer, size =     0.02 MiB, ( 2629.45 / 10922.67)
    llama_build_graph: non-view tensors processed: 676/676
    llama_new_context_with_model: compute buffer total size = 159.19 MiB
    ggml_backend_metal_buffer_type_alloc_buffer: allocated buffer, size =   156.02 MiB, ( 2785.45 / 10922.67)
    llama server listening at http://0.0.0.0:8080
2. To access the chatbot interface, open your web browser and enter `http://0.0.0.0:8080` into the address bar. 
    ![Yi model chatbot interface - llama.cpp](https://github.com/01-ai/Yi/blob/main/assets/img/yi_llama_cpp1.png?raw=true)
3. Enter a question, such as "How do you feed your pet fox? Please answer this question in 6 simple steps" into the prompt window, and you will receive a corresponding answer.
    ![Ask a question to Yi model - llama.cpp](https://github.com/01-ai/Yi/blob/main/assets/img/yi_llama_cpp2.png?raw=true)
You can build a web UI demo for Yi **chat** models (note that Yi base models are not supported in this senario).
[Step 1: Prepare your environment](#step-1-prepare-your-environment). 
[Step 2: Download the Yi model](#step-2-download-the-yi-model).
Step 3. To start a web service locally, run the following command.
You can access the web UI by entering the address provided in the console into your browser. 
 ![Quick start - web demo](https://github.com/01-ai/Yi/blob/main/assets/img/yi_34b_chat_web_demo.gif?raw=true)
bash finetune/scripts/run_sft_Yi_6b.sh
Once finished, you can compare the finetuned model and the base model with the following command:
bash finetune/scripts/run_eval.sh
For advanced usage (like fine-tuning based on your custom data), see the explanations below. ⬇️  
### Finetune code for Yi 6B and 34B
By default, we use a small dataset from [BAAI/COIG](https://huggingface.co/datasets/BAAI/COIG) to finetune the base model.
You can also prepare your customized dataset in the following `jsonl` format:
{ "prompt": "Human: Who are you? Assistant:", "chosen": "I'm Yi." }
And then mount them in the container to replace the default ones:
    -v /path/to/save/finetuned/model/:/finetuned-model \
    -v /path/to/train.jsonl:/yi/finetune/data/train.json \
    -v /path/to/eval.jsonl:/yi/finetune/data/eval.json \
    bash finetune/scripts/run_sft_Yi_6b.sh
Make sure you have conda. If not, use
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
conda create -n dev_env python=3.10 -y
pip install torch==2.0.1 deepspeed==0.10 tensorboard transformers datasets sentencepiece accelerate ray==2.7
For the Yi-6B model, a node with 4 GPUs, each with GPU memory larger than 60GB, is recommended.
For the Yi-34B model, because the usage of the zero-offload technique consumes a lot of CPU memory, please be careful to limit the number of GPUs in the 34B finetune training. Please use CUDA_VISIBLE_DEVICES to limit the number of GPUs (as shown in scripts/run_sft_Yi_34b.sh).
A typical hardware setup for finetuning the 34B model is a node with 8 GPUs (limited to 4 in running by CUDA_VISIBLE_DEVICES=0,1,2,3), each with GPU memory larger than 80GB, and total CPU memory larger than 900GB.
Download a LLM-base model to MODEL_PATH (6B and 34B). A typical folder of models is like:
|   |-- pytorch_model-00001-of-00002.bin
|   |-- pytorch_model-00002-of-00002.bin
|   |-- pytorch_model.bin.index.json
Download a dataset from huggingface to local storage DATA_PATH, e.g. Dahoas/rm-static.
|   |   |-- train-00000-of-00001-2a1df75c6bce91ab.parquet
|   |   |-- test-00000-of-00001-8c7c51afc6d45980.parquet
`finetune/yi_example_dataset` has example datasets, which are modified from [BAAI/COIG](https://huggingface.co/datasets/BAAI/COIG)
`cd` into the scripts folder, copy and paste the script, and run. For example:
For the Yi-6B base model, setting training_debug_steps=20 and num_train_epochs=4 can output a chat model, which takes about 20 minutes.
For the Yi-34B base model, it takes a relatively long time for initialization. Please be patient.
Then you'll see the answer from both the base model and the finetuned model.
python quantization/gptq/quant_autogptq.py \
  --model /base_model                      \
  --output_dir /quantized_model            \
Once finished, you can then evaluate the resulting model as follows:
python quantization/gptq/eval_quantized_model.py \
  --model /quantized_model                       \
For details, see the explanations below. ⬇️ 
[GPT-Q](https://github.com/IST-DASLab/gptq) is a PTQ (Post-Training Quantization)
method. It saves memory and provides potential speedups while retaining the accuracy
Yi models can be GPT-Q quantized without a lot of efforts. 
We provide a step-by-step tutorial below.
To run GPT-Q, we will use [AutoGPTQ](https://github.com/PanQiWei/AutoGPTQ) and
[exllama](https://github.com/turboderp/exllama).
And the huggingface transformers has integrated optimum and auto-gptq to perform
GPTQ quantization on language models.
The `quant_autogptq.py` script is provided for you to perform GPT-Q quantization:
python quant_autogptq.py --model /base_model \
    --output_dir /quantized_model --bits 4 --group_size 128 --trust_remote_code
You can run a quantized model using the `eval_quantized_model.py`:
python eval_quantized_model.py --model /quantized_model --trust_remote_code
python quantization/awq/quant_autoawq.py \
  --model /base_model                      \
  --output_dir /quantized_model            \
Once finished, you can then evaluate the resulting model as follows:
python quantization/awq/eval_quantized_model.py \
  --model /quantized_model                       \
For details, see the explanations below. ⬇️ 
[AWQ](https://github.com/mit-han-lab/llm-awq) is a PTQ (Post-Training Quantization)
method. It's an efficient and accurate low-bit weight quantization (INT3/4) for LLMs.
Yi models can be AWQ quantized without a lot of efforts. 
We provide a step-by-step tutorial below.
To run AWQ, we will use [AutoAWQ](https://github.com/casper-hansen/AutoAWQ).
The `quant_autoawq.py` script is provided for you to perform AWQ quantization:
python quant_autoawq.py --model /base_model \
    --output_dir /quantized_model --bits 4 --group_size 128 --trust_remote_code
You can run a quantized model using the `eval_quantized_model.py`:
python eval_quantized_model.py --model /quantized_model --trust_remote_code
If you want to deploy Yi models, make sure you meet the software and hardware requirements. 
Before using Yi quantized models, make sure you've installed the correct software listed below.
Before deploying Yi in your environment, make sure your hardware meets the following requirements.
Below are detailed minimum VRAM requirements under different batch use cases.
 If you have any questions while using the Yi series models, the answers provided below could serve as a helpful reference for you. ⬇️
- Base model or Chat model - which to fine-tune?
The choice of pre-trained language model for fine-tuning hinges on the computational resources you have at your disposal and the particular demands of your task.
    - If you are working with a substantial volume of fine-tuning data (say, over 10,000 samples), the Base model could be your go-to choice.
    - On the other hand, if your fine-tuning data is not quite as extensive, opting for the Chat model might be a more fitting choice.
    - It is generally advisable to fine-tune both the Base and Chat models, compare their performance, and then pick the model that best aligns with your specific requirements.
- Yi-34B versus Yi-34B-Chat for full-scale fine-tuning - what is the difference?
  The key distinction between full-scale fine-tuning on `Yi-34B`and `Yi-34B-Chat` comes down to the fine-tuning approach and outcomes.
    - Yi-34B-Chat employs a Special Fine-Tuning (SFT) method, resulting in responses that mirror human conversation style more closely.
    - The Base model's fine-tuning is more versatile, with a relatively high performance potential.
    - If you are confident in the quality of your data, fine-tuning with `Yi-34B` could be your go-to.
    - If you are aiming for model-generated responses that better mimic human conversational style, or if you have doubts about your data quality, `Yi-34B-Chat` might be your best bet.
- Quantized model versus original model - what is the performance gap?
    - The performance variance is largely contingent on the quantization method employed and the specific use cases of these models. For instance, when it comes to models provided by the AWQ official, from a Benchmark standpoint, quantization might result in a minor performance drop of a few percentage points.
    - Subjectively speaking, in situations like logical reasoning, even a 1% performance shift could impact the accuracy of the output results.
- Where can I source fine-tuning question answering datasets?
    - You can find fine-tuning question answering datasets on platforms like Hugging Face, with datasets like [m-a-p/COIG-CQIA](https://huggingface.co/datasets/m-a-p/COIG-CQIA) readily available. 
    - Additionally, Github offers fine-tuning frameworks, such as [hiyouga/LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory), which integrates pre-made datasets.
- What is the GPU memory requirement for fine-tuning Yi-34B FP16?
  The GPU memory needed for fine-tuning 34B FP16 hinges on the specific fine-tuning method employed. For full parameter fine-tuning, you'll need 8 GPUs each with 80 GB; however, more economical solutions like Lora require less. For more details, check out [hiyouga/LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory). Also, consider using BF16 instead of FP16 for fine-tuning to optimize performance.
- Are there any third-party platforms that support chat functionality for the Yi-34b-200k model?
  If you're looking for third-party Chats, options include [fireworks.ai](https://fireworks.ai/login?callbackURL=https://fireworks.ai/models/fireworks/yi-34b-chat).
 If you want to learn Yi, you can find a wealth of helpful educational resources here. ⬇️
Welcome to the Yi learning hub! 
Whether you're a seasoned developer or a newcomer, you can find a wealth of helpful educational resources to enhance your understanding and skills with Yi models, including insightful blog posts, comprehensive video tutorials, hands-on guides, and more.  
The content you find here has been generously contributed by knowledgeable Yi experts and passionate enthusiasts. We extend our heartfelt gratitude for your invaluable contributions! 
At the same time, we also warmly invite you to join our collaborative effort by contributing to Yi. If you have already made contributions to Yi, please don't hesitate to showcase your remarkable work in the table below.
With all these resources at your fingertips, you're ready to start your exciting journey with Yi. Happy learning! 🥳
      - [Quantization](#quantization-1)
      - [Fine-tuning](#fine-tuning-1)
    - [Chat model performance](#chat-model-performance)
    - [Base model performance](#base-model-performance)
      - [Yi-34B and Yi-34B-200K](#yi-34b-and-yi-34b-200k)
Yi has a comprehensive ecosystem, offering a range of tools, services, and models to enrich your experiences and maximize productivity.
  - [Quantization](#quantization-1)
  - [Fine-tuning](#fine-tuning-1)
The Yi series models follow the same model architecture as Llama. By choosing Yi, you can leverage existing tools, libraries, and resources within the Llama ecosystem, eliminating the need to create new tools and enhancing development efficiency.
For example, the Yi series models are saved in the format of the Llama model. You can directly use `LlamaForCausalLM` and `LlamaTokenizer` to load the model. For more information, see [Use the chat model](#31-use-the-chat-model).
from transformers import AutoModelForCausalLM, AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("01-ai/Yi-34b", use_fast=False)
model = AutoModelForCausalLM.from_pretrained("01-ai/Yi-34b", device_map="auto")
> - Feel free to create a PR and share the fantastic work you've built using the Yi series models.
> - To help others quickly understand your work, it is recommended to use the format of `:  + `.
If you want to get up with Yi in a few minutes, you can use the following services built upon Yi.
- Yi-34B-Chat: you can chat with Yi using one of the following platforms:
  - [Yi-34B-Chat | Hugging Face](https://huggingface.co/spaces/01-ai/Yi-34B-Chat)
  - [Yi-34B-Chat | Yi Platform](https://platform.lingyiwanwu.com/): **Note** that currently it's available through a whitelist. Welcome to apply (fill out a form in [English](https://cn.mikecrm.com/l91ODJf) or [Chinese](https://cn.mikecrm.com/gnEZjiQ)) and experience it firsthand!
- [Yi-6B-Chat (Replicate)](https://replicate.com/01-ai): you can use this model with more options by setting additional parameters and calling APIs.
- [ScaleLLM](https://github.com/vectorch-ai/ScaleLLM#supported-models): you can use this service to run Yi models locally with added flexibility and customization.
If you have limited computational capabilities, you can use Yi's quantized models as follows. 
These quantized models have reduced precision but offer increased efficiency, such as faster inference speed and smaller RAM usage.
- [TheBloke/Yi-34B-GPTQ](https://huggingface.co/TheBloke/Yi-34B-GPTQ) 
- [TheBloke/Yi-34B-GGUF](https://huggingface.co/TheBloke/Yi-34B-GGUF)
- [TheBloke/Yi-34B-AWQ](https://huggingface.co/TheBloke/Yi-34B-AWQ)
If you're seeking to explore the diverse capabilities within Yi's thriving family, you can delve into Yi's fine-tuned models as below.
- [TheBloke Models](https://huggingface.co/TheBloke): this site hosts numerous fine-tuned models derived from various LLMs including Yi. 
  This is not an exhaustive list for Yi, but to name a few sorted on downloads:
  - [TheBloke/dolphin-2_2-yi-34b-AWQ](https://huggingface.co/TheBloke/dolphin-2_2-yi-34b-AWQ)
  - [TheBloke/Yi-34B-Chat-AWQ](https://huggingface.co/TheBloke/Yi-34B-Chat-AWQ)
  - [TheBloke/Yi-34B-Chat-GPTQ](https://huggingface.co/TheBloke/Yi-34B-Chat-GPTQ)
- [SUSTech/SUS-Chat-34B](https://huggingface.co/SUSTech/SUS-Chat-34B): this model ranked first among all models below 70B and outperformed the twice larger deepseek-llm-67b-chat. You can check the result on the [Open LLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard).
- [OrionStarAI/OrionStar-Yi-34B-Chat-Llama](https://huggingface.co/OrionStarAI/OrionStar-Yi-34B-Chat-Llama): this model excelled beyond other models (such as GPT-4, Qwen-14B-Chat, Baichuan2-13B-Chat) in C-Eval and CMMLU evaluations on the [OpenCompass LLM Leaderboard](https://opencompass.org.cn/leaderboard-llm). 
- [NousResearch/Nous-Capybara-34B](https://huggingface.co/NousResearch/Nous-Capybara-34B): this model is trained with 200K context length and 3 epochs on the Capybara dataset. 
- [amazing-openai-api](https://github.com/soulteary/amazing-openai-api): this tool converts Yi model APIs into the OpenAI API format out of the box.
- [LlamaEdge](https://www.secondstate.io/articles/yi-34b/#create-an-openai-compatible-api-service-for-the-yi-34b-chat-model): this tool builds an OpenAI-compatible API server for Yi-34B-Chat using a portable Wasm (WebAssembly) file, powered by Rust.
For detailed capabilities of the Yi series model, see [Yi: Open Foundation Models by 01.AI](https://arxiv.org/abs/2403.04652).
    title={Yi: Open Foundation Models by 01.AI},
    author={01. AI and : and Alex Young and Bei Chen and Chao Li and Chengen Huang and Ge Zhang and Guanwei Zhang and Heng Li and Jiangcheng Zhu and Jianqun Chen and Jing Chang and Kaidong Yu and Peng Liu and Qiang Liu and Shawn Yue and Senbin Yang and Shiming Yang and Tao Yu and Wen Xie and Wenhao Huang and Xiaohui Hu and Xiaoyi Ren and Xinyao Niu and Pengcheng Nie and Yuchi Xu and Yudong Liu and Yue Wang and Yuxuan Cai and Zhenyu Gu and Zhiyuan Liu and Zonghong Dai},
- [Chat model performance](#chat-model-performance)
- [Base model performance](#base-model-performance)
Yi-34B-Chat model demonstrates exceptional performance, ranking first among all existing open-source models in the benchmarks including MMLU, CMMLU, BBH, GSM8k, and more.
![Chat model performance](https://github.com/01-ai/Yi/blob/main/assets/img/benchmark_chat.png?raw=true) 
 Evaluation methods and challenges. ⬇️ 
- **Evaluation methods**: we evaluated various benchmarks using both zero-shot and few-shot methods, except for TruthfulQA.
- **Zero-shot vs. few-shot**: in chat models, the zero-shot approach is more commonly employed.
- **Evaluation strategy**: our evaluation strategy involves generating responses while following instructions explicitly or implicitly (such as using few-shot examples). We then isolate relevant answers from the generated text.
- **Challenges faced**: some models are not well-suited to produce output in the specific format required by instructions in few datasets, which leads to suboptimal results.
*: C-Eval results are evaluated on the validation datasets
The Yi-34B and Yi-34B-200K models stand out as the top performers among open-source models, especially excelling in MMLU, CMMLU, common-sense reasoning, reading comprehension, and more.
![Base model performance](https://github.com/01-ai/Yi/blob/main/assets/img/benchmark_base.png?raw=true)
- **Disparity in results**: while benchmarking open-source models, a disparity has been noted between results from our pipeline and those reported by public sources like OpenCompass.
- **Investigation findings**: a deeper investigation reveals that variations in prompts, post-processing strategies, and sampling techniques across models may lead to significant outcome differences.
- **Uniform benchmarking process**: our methodology aligns with the original benchmarks—consistent prompts and post-processing strategies are used, and greedy decoding is applied during evaluations without any post-processing for the generated content.
- **Efforts to retrieve unreported scores**: for scores that were not reported by the original authors (including scores reported with different settings), we try to get results with our pipeline.
- **Extensive model evaluation**: to evaluate the model’s capability extensively, we adopted the methodology outlined in Llama2. Specifically, we included PIQA, SIQA, HellaSwag, WinoGrande, ARC, OBQA, and CSQA to assess common sense reasoning. SquAD, QuAC, and BoolQ were incorporated to evaluate reading comprehension.
- **Special configurations**: CSQA was exclusively tested using a 7-shot setup, while all other tests were conducted with a 0-shot configuration. Additionally, we introduced GSM8K (8-shot@1), MATH (4-shot@1), HumanEval (0-shot@1), and MBPP (3-shot@1) under the category "Math & Code".
- **Falcon-180B caveat**: Falcon-180B was not tested on QuAC and OBQA due to technical constraints. Its performance score is an average from other tasks, and considering the generally lower scores of these two tasks, Falcon-180B's capabilities are likely not underestimated.
Yi-9B is almost the best among a range of similar-sized open-source models (including Mistral-7B, SOLAR-10.7B, Gemma-7B, DeepSeek-Coder-7B-Base-v1.5 and more), particularly excelling in code, math, common-sense reasoning, and reading comprehension.
![Yi-9B benchmark - details](https://github.com/01-ai/Yi/blob/main/assets/img/Yi-9B_benchmark_details.png?raw=true)
- In terms of **overall** ability (Mean-All), Yi-9B performs the best among similarly sized open-source models, surpassing DeepSeek-Coder, DeepSeek-Math, Mistral-7B, SOLAR-10.7B, and Gemma-7B.
  ![Yi-9B benchmark - overall](https://github.com/01-ai/Yi/blob/main/assets/img/Yi-9B_benchmark_overall.png?raw=true)
- In terms of **coding** ability (Mean-Code), Yi-9B's performance is second only to DeepSeek-Coder-7B, surpassing Yi-34B, SOLAR-10.7B, Mistral-7B, and Gemma-7B.
  ![Yi-9B benchmark - code](https://github.com/01-ai/Yi/blob/main/assets/img/Yi-9B_benchmark_code.png?raw=true)
- In terms of **math** ability (Mean-Math), Yi-9B's performance is second only to DeepSeek-Math-7B, surpassing SOLAR-10.7B, Mistral-7B, and Gemma-7B.
  ![Yi-9B benchmark - math](https://github.com/01-ai/Yi/blob/main/assets/img/Yi-9B_benchmark_math.png?raw=true)
- In terms of **common sense and reasoning** ability (Mean-Text), Yi-9B's performance is on par with Mistral-7B, SOLAR-10.7B, and Gemma-7B.
  ![Yi-9B benchmark - text](https://github.com/01-ai/Yi/blob/main/assets/img/Yi-9B_benchmark_text.png?raw=true)
The code and weights of the Yi series models are distributed under the [Apache 2.0 license](https://github.com/01-ai/Yi/blob/main/LICENSE), which means the Yi series models are free for personal usage, academic purposes, and commercial use. 
A heartfelt thank you to each of you who have made contributions to the Yi community! You have helped Yi not just a project, but a vibrant, growing home for innovation.
[![yi contributors](https://contrib.rocks/image?repo=01-ai/yi&max=2000&columns=15)](https://github.com/01-ai/yi/graphs/contributors)
We use data compliance checking algorithms during the training process, to
ensure the compliance of the trained model to the best of our ability. Due to
complex data and the diversity of language model usage scenarios, we cannot
guarantee that the model will generate correct, and reasonable output in all
scenarios. Please be aware that there is still a risk of the model producing
problematic outputs. We will not be responsible for any risks and issues
resulting from misuse, misguidance, illegal usage, and related misinformation,
as well as any associated data security concerns.
The code and weights of the Yi-1.5 series models are distributed under the [Apache 2.0 license](https://github.com/01-ai/Yi/blob/main/LICENSE).
If you create derivative works based on this model, please include the following attribution in your derivative works:
    This work is a derivative of [The Yi Series Model You Base On] by 01.AI, used under the Apache 2.0 License.