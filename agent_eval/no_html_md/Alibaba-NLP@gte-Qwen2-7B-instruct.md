**gte-Qwen2-7B-instruct** is the latest model in the gte (General Text Embedding) model family that ranks **No.1** in both English and Chinese evaluations on the Massive Text Embedding Benchmark [MTEB benchmark](https://huggingface.co/spaces/mteb/leaderboard) (as of June 16, 2024).
Recently, the [**Qwen team**](https://huggingface.co/Qwen) released the Qwen2 series models, and we have trained the **gte-Qwen2-7B-instruct** model based on the [Qwen2-7B](https://huggingface.co/Qwen/Qwen2-7B) LLM model. Compared to the [gte-Qwen1.5-7B-instruct](https://huggingface.co/Alibaba-NLP/gte-Qwen1.5-7B-instruct) model, the **gte-Qwen2-7B-instruct** model uses the same training data and training strategies during the finetuning stage, with the only difference being the upgraded base model to Qwen2-7B. Considering the improvements in the Qwen2 series models compared to the Qwen1.5 series, we can also expect consistent performance enhancements in the embedding models.
The model incorporates several key advancements:
- Integration of bidirectional attention mechanisms, enriching its contextual understanding.
- Instruction tuning, applied solely on the query side for streamlined efficiency
- Comprehensive training across a vast, multilingual text corpus spanning diverse domains and scenarios. This training leverages both weakly supervised and supervised data, ensuring the model's applicability across numerous languages and a wide array of downstream tasks.
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("Alibaba-NLP/gte-Qwen2-7B-instruct", trust_remote_code=True)
# In case you want to reduce the maximum length:
    "how much protein should a female eat",
    "As a general guideline, the CDC's average requirement of protein for women ages 19 to 70 is 46 grams per day. But, as you can see from this chart, you'll need to increase that if you're expecting or training for a marathon. Check out the chart below to see how much protein you should be eating each day.",
    "Definition of summit for English Language Learners. : 1  the highest point of a mountain : the top of a mountain. : 2  the highest level. : 3  a meeting or series of meetings between the leaders of two or more governments.",
query_embeddings = model.encode(queries, prompt_name="query")
document_embeddings = model.encode(documents)
scores = (query_embeddings @ document_embeddings.T) * 100
Observe the [config_sentence_transformers.json](config_sentence_transformers.json) to see all pre-built prompt names. Otherwise, you can use `model.encode(queries, prompt="Instruct: ...\nQuery: "` to use a custom prompt of your choice.
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
def last_token_pool(last_hidden_states: Tensor,
                 attention_mask: Tensor) -> Tensor:
    left_padding = (attention_mask[:, -1].sum() == attention_mask.shape[0])
        return last_hidden_states[:, -1]
        sequence_lengths = attention_mask.sum(dim=1) - 1
        batch_size = last_hidden_states.shape[0]
        return last_hidden_states[torch.arange(batch_size, device=last_hidden_states.device), sequence_lengths]
def get_detailed_instruct(task_description: str, query: str) -> str:
    return f'Instruct: {task_description}\nQuery: {query}'
# Each query must come with a one-sentence instruction that describes the task
task = 'Given a web search query, retrieve relevant passages that answer the query'
    get_detailed_instruct(task, 'how much protein should a female eat'),
    get_detailed_instruct(task, 'summit define')
# No need to add instruction for retrieval documents
    "As a general guideline, the CDC's average requirement of protein for women ages 19 to 70 is 46 grams per day. But, as you can see from this chart, you'll need to increase that if you're expecting or training for a marathon. Check out the chart below to see how much protein you should be eating each day.",
    "Definition of summit for English Language Learners. : 1  the highest point of a mountain : the top of a mountain. : 2  the highest level. : 3  a meeting or series of meetings between the leaders of two or more governments."
input_texts = queries + documents
tokenizer = AutoTokenizer.from_pretrained('Alibaba-NLP/gte-Qwen2-7B-instruct', trust_remote_code=True)
model = AutoModel.from_pretrained('Alibaba-NLP/gte-Qwen2-7B-instruct', trust_remote_code=True)
batch_dict = tokenizer(input_texts, max_length=max_length, padding=True, truncation=True, return_tensors='pt')
embeddings = last_token_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
embeddings = F.normalize(embeddings, p=2, dim=1)
scores = (embeddings[:2] @ embeddings[2:].T) * 100
Usage via [infinity](https://github.com/michaelfeil/infinity), a MIT Licensed inference server.
# requires ~16-32GB VRAM NVIDIA Compute Capability >= 8.0
-v $PWD/data:/app/.cache --gpus "0" -p "7997":"7997" \
michaelf34/infinity:0.0.68-trt-onnx \
v2 --model-id Alibaba-NLP/gte-Qwen2-7B-instruct --revision "refs/pr/38" --dtype bfloat16 --batch-size 8 --device cuda --engine torch --port 7997 --no-bettertransformer
You can use the [scripts/eval_mteb.py](https://huggingface.co/Alibaba-NLP/gte-Qwen2-7B-instruct/blob/main/scripts/eval_mteb.py) to reproduce the following result of **gte-Qwen2-7B-instruct** on MTEB(English)/C-MTEB(Chinese):
The gte series models have consistently released two types of models: encoder-only models (based on the BERT architecture) and decode-only models (based on the LLM architecture). 
In addition to the open-source [GTE](https://huggingface.co/collections/Alibaba-NLP/gte-models-6680f0b13f885cb431e6d469) series models, GTE series models are also available as commercial API services on Alibaba Cloud.
- [Embedding Models](https://help.aliyun.com/zh/model-studio/developer-reference/general-text-embedding/): Three versions of the text embedding models are available: text-embedding-v1/v2/v3, with v3 being the latest API service.
- [ReRank Models](https://help.aliyun.com/zh/model-studio/developer-reference/general-text-sorting-model/): The gte-rerank model service is available.
Note that the models behind the commercial APIs are not entirely identical to the open-source models.
GTE models can be fine-tuned with a third party framework SWIFT.
# check: https://swift.readthedocs.io/en/latest/BestPractices/Embedding.html
NPROC_PER_NODE=$nproc_per_node \
    --model Alibaba-NLP/gte-Qwen2-7B-instruct \
    --dataset 'sentence-transformers/stsb' \
    --per_device_train_batch_size 2 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps $(expr 64 / $nproc_per_node) \
    --loss_type cosine_similarity \
If you find our paper or models helpful, please consider cite:
  title={Towards general text embeddings with multi-stage contrastive learning},
  author={Li, Zehan and Zhang, Xin and Zhang, Yanzhao and Long, Dingkun and Xie, Pengjun and Zhang, Meishan},
  journal={arXiv preprint arXiv:2308.03281},