The embedding model trained by Jina AI.
jina-embeddings-v3: Multilingual Embeddings With Task LoRA
[Blog](https://jina.ai/news/jina-embeddings-v3-a-frontier-multilingual-embedding-model/#parameter-dimensions) | [Azure](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/jinaai.jina-embeddings-v3-vm) | [AWS SageMaker](https://aws.amazon.com/marketplace/pp/prodview-kdi3xkt62lo32) | [API](https://jina.ai/embeddings)
## Intended Usage & Model Info
`jina-embeddings-v3` is a **multilingual multi-task text embedding model** designed for a variety of NLP applications.
Based on the [Jina-XLM-RoBERTa architecture](https://huggingface.co/jinaai/xlm-roberta-flash-implementation), 
this model supports Rotary Position Embeddings to handle long input sequences up to **8192 tokens**.
Additionally, it features 5 LoRA adapters to generate task-specific embeddings efficiently.
- **Extended Sequence Length:** Supports up to 8192 tokens with RoPE.
- **Task-Specific Embedding:** Customize embeddings through the `task` argument with the following options:
    - `retrieval.query`: Used for query embeddings in asymmetric retrieval tasks
    - `retrieval.passage`: Used for passage embeddings in asymmetric retrieval tasks
    - `separation`: Used for embeddings in clustering and re-ranking applications
    - `classification`: Used for embeddings in classification tasks
    - `text-matching`: Used for embeddings in tasks that quantify similarity between two texts, such as STS or symmetric retrieval tasks
- **Matryoshka Embeddings**: Supports flexible embedding sizes (`32, 64, 128, 256, 512, 768, 1024`), allowing for truncating embeddings to fit your application.
While the foundation model supports 100 languages, we've focused our tuning efforts on the following 30 languages: 
**Arabic, Bengali, Chinese, Danish, Dutch, English, Finnish, French, Georgian, German, Greek, 
Hindi, Indonesian, Italian, Japanese, Korean, Latvian, Norwegian, Polish, Portuguese, Romanian, 
Russian, Slovak, Spanish, Swedish, Thai, Turkish, Ukrainian, Urdu,** and **Vietnamese.**
> We fixed a bug in the `encode` function [#60](https://huggingface.co/jinaai/jina-embeddings-v3/discussions/60) where **Matryoshka embedding truncation** occurred *after normalization*, leading to non-normalized truncated embeddings. This issue has been resolved in the latest code revision.  
> If you have encoded data using the previous version and wish to maintain consistency, please use the specific code revision when loading the model: `AutoModel.from_pretrained('jinaai/jina-embeddings-v3', code_revision='da863dd04a4e5dce6814c6625adfba87b83838aa', ...)`
**Apply mean pooling when integrating the model.**
Mean pooling takes all token embeddings from the model's output and averages them at the sentence or paragraph level. 
This approach has been shown to produce high-quality sentence embeddings.
We provide an `encode` function that handles this for you automatically.
However, if you're working with the model directly, outside of the `encode` function, 
you'll need to apply mean pooling manually. Here's how you can do it:
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
        attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
        input_mask_expanded.sum(1), min=1e-9
sentences = ["How is the weather today?", "What is the current weather like today?"]
tokenizer = AutoTokenizer.from_pretrained("jinaai/jina-embeddings-v3")
model = AutoModel.from_pretrained("jinaai/jina-embeddings-v3", trust_remote_code=True)
encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors="pt")
task_id = model._adaptation_map[task]
adapter_mask = torch.full((len(sentences),), task_id, dtype=torch.int32)
    model_output = model(**encoded_input, adapter_mask=adapter_mask)
embeddings = mean_pooling(model_output, encoded_input["attention_mask"])
embeddings = F.normalize(embeddings, p=2, dim=1)
The easiest way to start using `jina-embeddings-v3` is with the [Jina Embedding API](https://jina.ai/embeddings/).
Alternatively, you can use `jina-embeddings-v3` directly via Transformers package:
!pip install transformers torch einops
If you run it on a GPU that support [FlashAttention-2](https://github.com/Dao-AILab/flash-attention). By 2024.9.12, it supports Ampere, Ada, or Hopper GPUs (e.g., A100, RTX 3090, RTX 4090, H100),
!pip install flash-attn --no-build-isolation
from transformers import AutoModel
model = AutoModel.from_pretrained("jinaai/jina-embeddings-v3", trust_remote_code=True)
    "Follow the white rabbit.",  # English
    "Sigue al conejo blanco.",  # Spanish
    "Suis le lapin blanc.",  # French
    "اتبع الأرنب الأبيض.",  # Arabic
    "Folge dem weißen Kaninchen.",  # German
# When calling the `encode` function, you can choose a `task` based on the use case:
# 'retrieval.query', 'retrieval.passage', 'separation', 'classification', 'text-matching'
# Alternatively, you can choose not to pass a `task`, and no specific LoRA adapter will be used.
embeddings = model.encode(texts, task="text-matching")
print(embeddings[0] @ embeddings[1].T)
By default, the model supports a maximum sequence length of 8192 tokens. 
However, if you want to truncate your input texts to a shorter length, you can pass the `max_length` parameter to the `encode` function:
embeddings = model.encode(["Very long ... document"], max_length=2048)
In case you want to use **Matryoshka embeddings** and switch to a different dimension, 
you can adjust it by passing the `truncate_dim` parameter to the `encode` function:
embeddings = model.encode(['Sample text'], truncate_dim=256)
The latest version (3.1.0) of [SentenceTransformers](https://github.com/UKPLab/sentence-transformers) also supports `jina-embeddings-v3`:
!pip install -U sentence-transformers
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("jinaai/jina-embeddings-v3", trust_remote_code=True)
    ["What is the weather like in Berlin today?"],
You can fine-tune `jina-embeddings-v3` using [SentenceTransformerTrainer](https://sbert.net/docs/package_reference/sentence_transformer/trainer.html). 
To fine-tune for a specific task, you should set the task before passing the model to the ST Trainer, either during initialization:
model = SentenceTransformer("jinaai/jina-embeddings-v3", trust_remote_code=True, model_kwargs={'default_task': 'classification'})
model = SentenceTransformer("jinaai/jina-embeddings-v3", trust_remote_code=True)
model[0].default_task = 'classification'
This way you can fine-tune the LoRA adapter for the chosen task.
However, If you want to fine-tune the entire model, make sure the main parameters are set as trainable when loading the model:
model = SentenceTransformer("jinaai/jina-embeddings-v3", trust_remote_code=True, model_kwargs={'lora_main_params_trainable': True})
This will allow fine-tuning the whole model instead of just the LoRA adapters.
You can use ONNX for efficient inference with `jina-embeddings-v3`:
from transformers import AutoTokenizer, PretrainedConfig
def mean_pooling(model_output: np.ndarray, attention_mask: np.ndarray):
    token_embeddings = model_output
    input_mask_expanded = np.expand_dims(attention_mask, axis=-1)
    input_mask_expanded = np.broadcast_to(input_mask_expanded, token_embeddings.shape)
    sum_embeddings = np.sum(token_embeddings * input_mask_expanded, axis=1)
    sum_mask = np.clip(np.sum(input_mask_expanded, axis=1), a_min=1e-9, a_max=None)
    return sum_embeddings / sum_mask
# Load tokenizer and model config
tokenizer = AutoTokenizer.from_pretrained('jinaai/jina-embeddings-v3')
config = PretrainedConfig.from_pretrained('jinaai/jina-embeddings-v3')
input_text = tokenizer('sample text', return_tensors='np')
model_path = 'jina-embeddings-v3/onnx/model.onnx'
session = onnxruntime.InferenceSession(model_path)
# Prepare inputs for ONNX model
task_id = np.array(config.lora_adaptations.index(task_type), dtype=np.int64)
    'input_ids': input_text['input_ids'],
    'attention_mask': input_text['attention_mask'],
outputs = session.run(None, inputs)[0]
# Apply mean pooling and normalization to the model outputs
embeddings = mean_pooling(outputs, input_text["attention_mask"])
embeddings = embeddings / np.linalg.norm(embeddings, ord=2, axis=1, keepdims=True)
Join our [Discord community](https://discord.jina.ai) and chat with other community members about ideas.
`jina-embeddings-v3` is listed on AWS & Azure. If you need to use it beyond those platforms or on-premises within your company, note that the models is licensed under CC BY-NC 4.0. For commercial usage inquiries, feel free to [contact us](https://jina.ai/contact-sales/).
If you find `jina-embeddings-v3` useful in your research, please cite the following paper:
@misc{sturua2024jinaembeddingsv3multilingualembeddingstask,
      title={jina-embeddings-v3: Multilingual Embeddings With Task LoRA}, 
      author={Saba Sturua and Isabelle Mohr and Mohammad Kalim Akram and Michael Günther and Bo Wang and Markus Krimmel and Feng Wang and Georgios Mastrapas and Andreas Koukounas and Andreas Koukounas and Nan Wang and Han Xiao},
      url={https://arxiv.org/abs/2409.10173}, 