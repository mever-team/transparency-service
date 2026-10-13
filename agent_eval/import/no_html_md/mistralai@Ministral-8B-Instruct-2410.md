# Model Card for Ministral-8B-Instruct-2410
We introduce two new state-of-the-art models for local intelligence, on-device computing, and at-the-edge use cases. We call them les Ministraux: Ministral 3B and Ministral 8B. 
The Ministral-8B-Instruct-2410 Language Model is an instruct fine-tuned model significantly outperforming existing models of similar size, released under the Mistral Research License.
If you are interested in using Ministral-3B or Ministral-8B commercially, outperforming Mistral-7B, [reach out to us](https://mistral.ai/contact/).
For more details about les Ministraux please refer to our release [blog post](https://mistral.ai/news/ministraux).
- Released under the **Mistral Research License**, reach out to us for a commercial license
- Trained with a **128k context window** with **interleaved sliding-window attention**
- Trained on a large proportion of **multilingual and code data**
- Supports **function calling**
- Vocabulary size of **131k**, using the **V3-Tekken** tokenizer
### Basic Instruct Template (V3-Tekken)
[INST]user message[/INST]assistant response[INST]new user message[/INST]
*For more information about the tokenizer please refer to [mistral-common](https://github.com/mistralai/mistral-common)*
We recommend using this model with the [vLLM library](https://github.com/vllm-project/vllm)
to implement production-ready inference pipelines.
> Currently vLLM is capped at 32k context size because interleaved attention kernels for paged attention are not yet implemented in vLLM.
> Attention kernels for paged attention are being worked on and as soon as it is fully supported in vLLM, this model card will be updated.
> To take advantage of the full 128k context size we recommend [Mistral Inference](https://huggingface.co/mistralai/Ministral-8B-Instruct-2410#mistral-inference)
Make sure you install `vLLM >= v0.6.4`:
Also make sure you have `mistral_common >= 1.4.4` installed:
pip install --upgrade mistral_common
You can also make use of a ready-to-go [docker image](https://github.com/vllm-project/vllm/blob/main/Dockerfile).
from vllm.sampling_params import SamplingParams
model_name = "mistralai/Ministral-8B-Instruct-2410"
sampling_params = SamplingParams(max_tokens=8192)
# note that running Ministral 8B on a single GPU requires 24 GB of GPU RAM
# If you want to divide the GPU requirement over multiple devices, please add *e.g.* `tensor_parallel=2`
llm = LLM(model=model_name, tokenizer_mode="mistral", config_format="mistral", load_format="mistral")
prompt = "Do we need to think for 10 seconds to find the answer of 1 + 1?"
outputs = llm.chat(messages, sampling_params=sampling_params)
print(outputs[0].outputs[0].text)
# You don't need to think for 10 seconds to find the answer to 1 + 1. The answer is 2,
# and you can easily add these two numbers in your mind very quickly without any delay.
You can also use Ministral-8B in a server/client setting. 
vllm serve mistralai/Ministral-8B-Instruct-2410 --tokenizer_mode mistral --config_format mistral --load_format mistral
**Note:** Running Ministral-8B on a single GPU requires 24 GB of GPU RAM. 
If you want to divide the GPU requirement over multiple devices, please add *e.g.* `--tensor_parallel=2`
curl --location 'http://:8000/v1/chat/completions' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer token' \
    "model": "mistralai/Ministral-8B-Instruct-2410",
        "content": "Do we need to think for 10 seconds to find the answer of 1 + 1?"
We recommend using [mistral-inference](https://github.com/mistralai/mistral-inference) to quickly try out / "vibe-check" the model.
Make sure to have `mistral_inference >= 1.5.0` installed.
pip install mistral_inference --upgrade
from huggingface_hub import snapshot_download
mistral_models_path = Path.home().joinpath('mistral_models', '8B-Instruct')
mistral_models_path.mkdir(parents=True, exist_ok=True)
snapshot_download(repo_id="mistralai/Ministral-8B-Instruct-2410", allow_patterns=["params.json", "consolidated.safetensors", "tekken.json"], local_dir=mistral_models_path)
After installing `mistral_inference`, a `mistral-chat` CLI command should be available in your environment. You can chat with the model using
mistral-chat $HOME/mistral_models/8B-Instruct --instruct --max_tokens 256
> In this example the passkey message has over >100k tokens and mistral-inference
> does not have a chunked pre-fill mechanism. Therefore you will need a lot of
> GPU memory in order to run the below example (80 GB). For a more memory-efficient
> solution we recommend using vLLM.
from mistral_inference.transformer import Transformer
from mistral_inference.generate import generate
from huggingface_hub import hf_hub_download
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.protocol.instruct.messages import UserMessage
from mistral_common.protocol.instruct.request import ChatCompletionRequest
def load_passkey_request() -> ChatCompletionRequest:
    passkey_file = hf_hub_download(repo_id="mistralai/Ministral-8B-Instruct-2410", filename="passkey_example.json")
    with open(passkey_file, "r") as f:
    message_content = data["messages"][0]["content"]
    return ChatCompletionRequest(messages=[UserMessage(content=message_content)])
tokenizer = MistralTokenizer.from_file(f"{mistral_models_path}/tekken.json")
model = Transformer.from_folder(mistral_models_path, softmax_fp32=False)
completion_request = load_passkey_request()
tokens = tokenizer.encode_chat_completion(completion_request).tokens
out_tokens, _ = generate([tokens], model, max_tokens=64, temperature=0.0, eos_id=tokenizer.instruct_tokenizer.tokenizer.eos_id)
result = tokenizer.instruct_tokenizer.tokenizer.decode(out_tokens[0])
print(result)  # The pass key is 13005.
from mistral_inference.transformer import Transformer
from mistral_inference.generate import generate
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.protocol.instruct.messages import UserMessage
from mistral_common.protocol.instruct.request import ChatCompletionRequest
tokenizer = MistralTokenizer.from_file(f"{mistral_models_path}/tekken.json")
model = Transformer.from_folder(mistral_models_path)
completion_request = ChatCompletionRequest(messages=[UserMessage(content="How often does the letter r occur in Mistral?")])
tokens = tokenizer.encode_chat_completion(completion_request).tokens
out_tokens, _ = generate([tokens], model, max_tokens=64, temperature=0.0, eos_id=tokenizer.instruct_tokenizer.tokenizer.eos_id)
result = tokenizer.instruct_tokenizer.tokenizer.decode(out_tokens[0])
from mistral_common.protocol.instruct.tool_calls import Function, Tool
from mistral_inference.transformer import Transformer
from mistral_inference.generate import generate
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.protocol.instruct.messages import UserMessage
from mistral_common.protocol.instruct.request import ChatCompletionRequest
from mistral_common.tokens.tokenizers.tekken import SpecialTokenPolicy
tokenizer = MistralTokenizer.from_file(f"{mistral_models_path}/tekken.json")
tekken = tokenizer.instruct_tokenizer.tokenizer
tekken.special_token_policy = SpecialTokenPolicy.IGNORE
model = Transformer.from_folder(mistral_models_path)
completion_request = ChatCompletionRequest(
                description="Get the current weather",
                            "description": "The city and state, e.g. San Francisco, CA",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "The temperature unit to use. Infer this from the users location.",
                    "required": ["location", "format"],
        UserMessage(content="What's the weather like today in Paris?"),
tokens = tokenizer.encode_chat_completion(completion_request).tokens
out_tokens, _ = generate([tokens], model, max_tokens=64, temperature=0.0, eos_id=tokenizer.instruct_tokenizer.tokenizer.eos_id)
result = tokenizer.instruct_tokenizer.tokenizer.decode(out_tokens[0])
Albert Jiang, Alexandre Abou Chahine, Alexandre Sablayrolles, Alexis Tacnet, Alodie Boissonnet, Alok Kothari, Amélie Héliou, Andy Lo, Anna Peronnin, Antoine Meunier, Antoine Roux, Antonin Faure, Aritra Paul, Arthur Darcet, Arthur Mensch, Audrey Herblin-Stoop, Augustin Garreau, Austin Birky, Avinash Sooriyarachchi, Baptiste Rozière, Barry Conklin, Bastien Bouillon, Blanche Savary de Beauregard, Carole Rambaud, Caroline Feldman, Charles de Freminville, Charline Mauro, Chih-Kuan Yeh, Chris Bamford, Clement Auguy, Corentin Heintz, Cyriaque Dubois, Devendra Singh Chaplot, Diego Las Casas, Diogo Costa, Eléonore Arcelin, Emma Bou Hanna, Etienne Metzger, Fanny Olivier Autran, Francois Lesage, Garance Gourdel, Gaspard Blanchet, Gaspard Donada Vidal, Gianna Maria Lengyel, Guillaume Bour, Guillaume Lample, Gustave Denis, Harizo Rajaona, Himanshu Jaju, Ian Mack, Ian Mathew, Jean-Malo Delignon, Jeremy Facchetti, Jessica Chudnovsky, Joachim Studnia, Justus Murke, Kartik Khandelwal, Kenneth Chiu, Kevin Riera, Leonard Blier, Leonard Suslian, Leonardo Deschaseaux, Louis Martin, Louis Ternon, Lucile Saulnier, Lélio Renard Lavaud, Sophia Yang, Margaret Jennings, Marie Pellat, Marie Torelli, Marjorie Janiewicz, Mathis Felardos, Maxime Darrin, Michael Hoff, Mickaël Seznec, Misha Jessel Kenyon, Nayef Derwiche, Nicolas Carmont Zaragoza, Nicolas Faurie, Nicolas Moreau, Nicolas Schuhl, Nikhil Raghuraman, Niklas Muhs, Olivier de Garrigues, Patricia Rozé, Patricia Wang, Patrick von Platen, Paul Jacob, Pauline Buche, Pavankumar Reddy Muddireddy, Perry Savas, Pierre Stock, Pravesh Agrawal, Renaud de Peretti, Romain Sauvestre, Romain Sinthe, Roman Soletskyi, Sagar Vaze, Sandeep Subramanian, Saurabh Garg, Soham Ghosh, Sylvain Regnier, Szymon Antoniak, Teven Le Scao, Theophile Gervet, Thibault Schueller, Thibaut Lavril, Thomas Wang, Timothée Lacroix, Valeriia Nemychnikova, Wendy Shang, William El Sayed, William Marshall