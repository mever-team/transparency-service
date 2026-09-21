The crispy sentence embedding family from Mixedbread.
 🍞 Looking for a simple end-to-end retrieval solution? Meet Omni, our multimodal and multilingual model. Get in touch for access. 
# mixedbread-ai/mxbai-embed-large-v1
Here, we provide several ways to produce sentence embeddings. Please note that you have to provide the prompt `Represent this sentence for searching relevant passages:` for query if you want to use it for retrieval. Besides that you don't need any prompt. Our model also supports [Matryoshka Representation Learning and binary quantization](https://www.mixedbread.ai/blog/binary-mrl).
Here, we provide several ways to produce sentence embeddings. Please note that you have to provide the prompt `Represent this sentence for searching relevant passages: ` for query if you want to use it for retrieval. Besides that you don't need any prompt.
python -m pip install -U sentence-transformers
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from sentence_transformers.quantization import quantize_embeddings
# 1. Specify preffered dimensions
model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1", truncate_dim=dimensions)
# The prompt used for query retrieval tasks:
# query_prompt = 'Represent this sentence for searching relevant passages: '
query = "A man is eating a piece of bread"
    "The girl is carrying a baby.",
query_embedding = model.encode(query, prompt_name="query")
# query_embedding = model.encode(query_prompt + query)
# query_embedding = model.encode(query, prompt=query_prompt)
docs_embeddings = model.encode(docs)
# Optional: Quantize the embeddings
binary_query_embedding = quantize_embeddings(query_embedding, precision="ubinary")
binary_docs_embeddings = quantize_embeddings(docs_embeddings, precision="ubinary")
similarities = cos_sim(query_embedding, docs_embeddings)
print('similarities:', similarities)
from transformers import AutoModel, AutoTokenizer
from sentence_transformers.util import cos_sim
# For retrieval you need to pass this prompt. Please find our more in our blog post.
def transform_query(query: str) -> str:
    """ For retrieval, add the prompt for query (not for documents).
    return f'Represent this sentence for searching relevant passages: {query}'
# The model works really well with cls pooling (default) but also with mean pooling.
def pooling(outputs: torch.Tensor, inputs: Dict,  strategy: str = 'cls') -> np.ndarray:
            outputs * inputs["attention_mask"][:, :, None], dim=1) / torch.sum(inputs["attention_mask"], dim=1, keepdim=True)
    return outputs.detach().cpu().numpy()
model_id = 'mixedbread-ai/mxbai-embed-large-v1'
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModel.from_pretrained(model_id).cuda()
    transform_query('A man is eating a piece of bread'),
    "The girl is carrying a baby.",
inputs = tokenizer(docs, padding=True, return_tensors='pt')
outputs = model(**inputs).last_hidden_state
embeddings = pooling(outputs, inputs, 'cls')
similarities = cos_sim(embeddings[0], embeddings[1:])
print('similarities:', similarities)
If you haven't already, you can install the [Transformers.js](https://huggingface.co/docs/transformers.js) JavaScript library from [NPM](https://www.npmjs.com/package/@huggingface/transformers) using:
npm i @huggingface/transformers
You can then use the model to compute embeddings like this:
import { pipeline, cos_sim } from "@huggingface/transformers";
// Create a feature extraction pipeline
const extractor = await pipeline("feature-extraction", "mixedbread-ai/mxbai-embed-large-v1", {
    dtype: "fp32", // Options: "fp32", "fp16", "q8"
// Generate sentence embeddings
    "Represent this sentence for searching relevant passages: A man is eating a piece of bread",
    "The girl is carrying a baby.",
const output = await extractor(docs, { pooling: "cls" });
const [source_embeddings, ...document_embeddings ] = output.tolist();
const similarities = document_embeddings.map(x => cos_sim(source_embeddings, x));
console.log(similarities); // [0.7919578577247139, 0.6369278664248345, 0.16512018371357193, 0.3620778366720027]
You can use the model via our API as follows:
from mixedbread_ai.client import MixedbreadAI, EncodingFormat
from sklearn.metrics.pairwise import cosine_similarity
mxbai = MixedbreadAI(api_key="{MIXEDBREAD_API_KEY}")
    'What is the capital of Australia?',
    'Canberra is the capital of Australia.'
     model="mixedbread-ai/mxbai-embed-large-v1",
     encoding_format=[EncodingFormat.FLOAT, EncodingFormat.UBINARY, EncodingFormat.INT_8],
encoded_embeddings = res.data[0].embedding
print(res.dimensions, encoded_embeddings.ubinary, encoded_embeddings.float_, encoded_embeddings.int_8)
The API comes with native int8 and binary quantization support! Check out the [docs](https://mixedbread.ai/docs) for more information.
docker run --gpus all -v $PWD/data:/app/.cache -p "7997":"7997" \
v2 --model-id mixedbread-ai/mxbai-embed-large-v1 --revision "main" --dtype float16 --engine torch --port 7997
As of March 2024, our model archives SOTA performance for Bert-large sized models on the [MTEB](https://huggingface.co/spaces/mteb/leaderboard). It ourperforms commercial models like OpenAIs text-embedding-3-large and matches the performance of model 20x it's size like the [echo-mistral-7b](https://huggingface.co/jspringer/echo-mistral-7b-instruct-lasttoken). Our model was trained with no overlap of the MTEB data, which indicates that our model generalizes well across several domains, tasks and text length. We know there are some limitations with this model, which will be fixed in v2. 
Please find more information in our [blog post](https://mixedbread.ai/blog/mxbai-embed-large-v1). 
## Matryoshka and Binary Quantization
Embeddings in their commonly used form (float arrays) have a high memory footprint when used at scale. Two approaches to solve this problem are Matryoshka Representation Learning (MRL) and (Binary) Quantization. While MRL reduces the number of dimensions of an embedding, binary quantization transforms the value of each dimension from a float32 into a lower precision (int8 or even binary).  The model supports both approaches! 
You can also take it one step further, and combine both MRL and quantization. This combination of binary quantization and MRL allows you to reduce the memory usage of your embeddings significantly. This leads to much lower costs when using a vector database in particular. You can read more about the technology and its advantages in our [blog post](https://www.mixedbread.ai/blog/binary-mrl).
Please join our [Discord Community](https://discord.gg/jDfMHzAVfU) and share your feedback and thoughts! We are here to help and also always happy to chat.
  title={Open Source Strikes Bread - New Fluffy Embeddings Model},
  author={Sean Lee and Aamir Shakir and Darius Koenig and Julius Lipp},
  url={https://www.mixedbread.ai/blog/mxbai-embed-large-v1},
  title={AnglE-optimized Text Embeddings},
  author={Li, Xianming and Li, Jing},
  journal={arXiv preprint arXiv:2309.12871},