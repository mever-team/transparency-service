# Apriel-1.5-15b-Thinker - Mid training is all you need!
3. [Training Details](#training-details)  
5. [Intended Use](#intended-use)  
6. [Limitations](#limitations)  
7. [Security and Responsible Use](#security-and-responsible-use)  
10. [Acknowledgements](#acknowledgements)
**Click here to skip to the technical report** -> https://huggingface.co/ServiceNow-AI/Apriel-1.5-15b-Thinker/blob/main/Apriel-1.5-Thinker.pdf
**Apriel-1.5-15b-Thinker** is a multimodal reasoning model in ServiceNow’s Apriel SLM series which achieves competitive performance against models 10 times it's size. Apriel-1.5 is the second model in the reasoning series. It introduces enhanced textual reasoning capabilities and adds image reasoning support to the previous text model.  It has undergone extensive continual pretraining across both text and image domains. In terms of post-training this model has **undergone text-SFT only**. Our research demonstrates that with a strong mid-training regimen, we are able to achive SOTA performance on text and image reasoning tasks without having any image SFT training or RL.
- Achieves a score of **52** on the Artificial Analysis index and is competitive with Deepseek R1 0528, Gemini-Flash etc.
- It is **AT LEAST 1 / 10** the size of any other model that scores > 50 on the Artificial Analysis index.
- Scores **68** on Tau2 Bench Telecom and **62** on IFBench, which are key benchmarks for the enterprise domain.
- At 15B parameters, the model fits on a single GPU, making it highly memory-efficient.
- For text benchmarks, we report evaluations perforomed by a third party - **Artificial Analysis**. 
- For image benchmarks, we report evaluations obtained by https://github.com/open-compass/VLMEvalKit
# Results reported by Artificial Analysis
![index - latest 2](https://cdn-uploads.huggingface.co/production/uploads/66a41f3c1d52bffc13c285a5/pdSRgotQw00XKB04bmJg3.png)
![index vs size fixed 3](https://cdn-uploads.huggingface.co/production/uploads/66a41f3c1d52bffc13c285a5/ewXvkN75gfyplJpWEJLyP.png)
We are a small lab with big goals. While we are not GPU poor, our lab, in comparison has a tiny fraction of the compute available to other Frontier labs. Our goal with this work is to show that a SOTA model can be built with limited resources if you have the right data, design and solid methodology.
We set out to build a **small but powerful model**, aiming for capabilities on par with frontier models. Developing a 15B model with this level of performance requires tradeoffs, so we prioritized **getting SOTA-level performance first**. Mid-training consists only of **CPT and SFT**; no **RL** has been applied.
This model performs **extensive reasoning by default**, allocating extra internal effort to improve robustness and accuracy even on simpler queries. You may notice slightly higher token usage and longer response times, but we are actively working to make it more **efficient and concise** in future releases.
**Mid training / Continual Pre‑training**
In this stage, the model is trained on billions of tokens of carefully curated textual samples drawn from mathematical reasoning, coding challenges, scientific discourse, logical puzzles, and diverse knowledge-rich texts along with multimodal samples covering image understanding and reasoning, captioning, and interleaved image-text data. The objective is to strengthen foundational reasoning capabilities of the model. This stage is critical for the model to function as a reasoner and provides significant lifts in reasoning benchmarks.
**Supervised Fine‑Tuning (SFT)**
The model is fine-tuned on over 2M high-quality text samples spanning mathematical and scientific problem-solving, coding tasks, instruction-following, API/function invocation, and conversational use cases. This results in superior text performance comparable to models such as Deepseek R1 0528 and Gemini-Flash. Although no image-specific fine-tuning is performed, the model’s inherent multimodal capabilities and cross-modal transfer of reasoning behavior from the text SFT yield competitive image performance relative to other leading open-source VL models. 
# Running Apriel-1.5-15B-Thinker with vLLM
As the upstream PR is not yet merged, you can use this custom image as an alternate way to run the model with tool and reasoning parsers enabled.
docker.io/amant555/vllm_apriel:latest
Run the container with the following command:
python3 -m vllm.entrypoints.openai.api_server \
  --model ServiceNow-AI/Apriel-1.5-15b-Thinker \
  --served-model-name Apriel-1p5-15B-Thinker \
This will start the vLLM OpenAI-compatible API server serving the **Apriel-1.5-15B-Thinker** model with Apriel’s custom tool parser and reasoning parser.
## Running the Reasoning model
Here is a code snippet demonstrating the model's usage with the transformers library's generate function:
# Tested with transformers==4.48
from transformers import AutoProcessor, AutoModelForImageTextToText
model_id = "ServiceNow-AI/Apriel-1.5-15b-Thinker"
model = AutoModelForImageTextToText.from_pretrained(
processor = AutoProcessor.from_pretrained(model_id)
            {"type": "text", "text": "What is the capital for France?"},
inputs = processor.apply_chat_template(chat, add_generation_prompt=True, tokenize=True, return_dict=True, return_tensors="pt")
inputs = {k: v.to(model.device) if isinstance(v, torch.Tensor) else v for k, v in inputs.items()}
inputs.pop("token_type_ids", None)
    output_ids = model.generate(**inputs, max_new_tokens=1024, do_sample=True, temperature=0.6)
generated_ids = output_ids[:, inputs['input_ids'].shape[1]:]
output = processor.decode(generated_ids[0], skip_special_tokens=True)
response = re.findall(r"\[BEGIN FINAL RESPONSE\](.*?)\[END FINAL RESPONSE\]", output, re.DOTALL)[0].strip()
print("Text-only Response:", response)
# Example 2: Image understanding
url = "https://picsum.photos/id/237/200/300"
image = Image.open(requests.get(url, stream=True).raw).convert("RGB")
            {"type": "text", "text": "Which animal is this?"},
prompt = processor.apply_chat_template(chat, add_generation_prompt=True, tokenize=False)
inputs = processor(text=prompt, images=[image], return_tensors="pt").to(model.device)
inputs.pop("token_type_ids", None)
    output_ids = model.generate(**inputs, max_new_tokens=1024, do_sample=True, temperature=0.6)
generated_ids = output_ids[:, inputs['input_ids'].shape[1]:]
output = processor.decode(generated_ids[0], skip_special_tokens=True)
response = re.findall(r"\[BEGIN FINAL RESPONSE\](.*?)\[END FINAL RESPONSE\]", output, re.DOTALL)[0].strip()
print("Image Response:", response)
You are a thoughtful and systematic AI assistant built by ServiceNow Language Models (SLAM) lab. Before providing an answer, analyze the problem carefully and present your reasoning step by step. After explaining your thought process, provide the final solution in the following format: [BEGIN FINAL RESPONSE] ... [END FINAL RESPONSE].
The model will first generate its thinking process and then generate its final response between `[BEGIN FINAL RESPONSE]` and `[END FINAL RESPONSE]`. Here is a code snippet demonstrating the application of the chat template:
from transformers import AutoTokenizer
model_name = "ServiceNow-AI/Apriel-1.5-15b-Thinker"
tokenizer = AutoTokenizer.from_pretrained(model_name)
custom_system_prompt = "Answer like a pirate."
prompt = "You are an expert assistant in the implementation of customer experience management aspect of retail applications \n \nYou will be using Python as the programming language. \n \nYou will utilize a factory design pattern for the implementation and following the dependency inversion principle \n \nYou will modify the implementation based on user requirements. \n \nUpon user request, you will add, update, and remove the features & enhancements in the implementation provided by you. \n \nYou will ask whether the user wants to refactor the provided code or needs a sample implementation for reference. Upon user confirmation, I will proceed accordingly. \n \n**Guidelines:** \n 1. **User Requirements:** \n - You have to ask users about their requirements, clarify the user expectations, and suggest the best possible solution by providing examples of Python code snippets. \n - Ask users about which type of reports they need to assess the AI model's performance, accuracy, and reliability. \n - After providing the solution, you have to ask the user about the trial of the solution and modify the solution based on the user feedback. \n \n 2. **Libraries/Frameworks:** \n - You will be utilizing Python as a programming language. \n - You will be using Flask framework for REST APIS implementation \n \n 3. **Communication Gesture:** \n - Your conversation with the user should be interactive, supportive, courageous, and professional. \n - You have to break down the complex concepts into sub-concepts and try to explain them to the user. \n - You have to ask the user for the required parameters. If the user refuses to provide in 2 attempts, politely exit the conversation. \n - You have to provide your supported parameters to the user, if the user refuses to accept them then you have to put an apology note and exit the conversation. \n - You have to track the conversation about unasked questions by the user. If some/one of the questions remain then you have to remind the user about these questions and proceed to answer them based on the user's confirmation \n \n 4. **Implementation:** \n - Your code/implementations should be reliable, scaleable, modular, and reusable. \n - You will be providing unit tests for the implementation upon user request. \n - You will be following MVC architecture for the applications \n - Your implementations must be well-commented and readable \n \n \n- Today's date is 23rd August 2024. \n- The default sender email is sender-assistant@email.com.\nHi, I am conducting research on retail customer feedback systems and I need assistance with designing and implementing them. Could you kindly provide me with a list of general customer feedback system modules?"
    {"role": "user", "content": custom_system_prompt + "\n\n" + prompt}
tools = [{"type": "function", "function": {"name": "getRetailFeedbackModules", "description": "Returns the list of modules usually present in the retail industry", "parameters": {"type": "object", "properties": {"page": {"type": "integer", "description": "The current page number.", "default": 1}, "page_size": {"type": "integer", "description": "The number of items per page.", "default": 3}}}}}, {"type": "function", "function": {"name": "verifyImplementation", "description": "Returns the list of modules usually present in the retail industry", "parameters": {"type": "object", "properties": {"coding_language": {"type": "string", "description": "The supported languages for verification of implementation.", "default": "python", "enum": ["python", "java", "php"]}, "code": {"type": "string", "description": "The code which needs verification"}, "design_pattern": {"type": "string", "description": "The design pattern to verify in the implementation", "enum": ["factory", "strategy", "singleton"]}, "verify_best_practices": {"type": "boolean", "description": "The verification of the coding style based on the language selected", "default": true}}}}}]
text = tokenizer.apply_chat_template(
model_inputs = tokenizer([text], return_tensors="pt")
1. Use the model’s default chat template, which already includes a system prompt.
2. We recommend setting temperature to `0.6`. 
3. We ensure the model starts with `Here are my reasoning steps:\n` during all our evaluations. This is implemented in the default chat template.
4. For multi-turn conversations, intermediate turns (historical model outputs) are expected to contain only the final response, without reasoning steps.
The Apriel family of models are designed for a variety of general-purpose instruction tasks, including:
- Code assistance and generation  
- Logical reasoning and multi-step tasks  
- Question answering and information retrieval
- Function calling, complex instruction following and agent use cases
They are **not intended** for use in safety-critical applications without human oversight or in scenarios requiring guaranteed factual accuracy.
- **Factual accuracy:** May produce incorrect, misleading, or outdated content. Outputs should be verified before use in critical contexts.  
- **Bias:** May reflect societal, cultural, or systemic biases present in training data.  
- **Ethics:** Do not use the model to produce harmful, unlawful, or unethical content.  
- **Language:** Strongest performance is in English. Output quality may degrade in underrepresented languages.  
- **Critical use:** Not suitable for medical, legal, financial, or other high-risk applications without safeguards.
# Security and Responsible Use
**Security Responsibilities:**  
Deployers and users are strongly encouraged to align their security practices with established frameworks and regulatory guidelines such as the EU AI Act and the NIST AI Risk Management Framework (RMF).
- Regularly conduct robustness assessments to identify and mitigate adversarial inputs.
- Implement validation and filtering processes to prevent harmful or biased outputs.
- Continuously perform data privacy checks to guard against unintended data leaks.
- Document and communicate the model's limitations, intended usage, and known security risks to all end-users.
- Schedule periodic security reviews and updates to address emerging threats and vulnerabilities.
- Follow established security policies and usage guidelines provided by deployers.
- Protect and manage sensitive information when interacting with the model.
- Report anomalies, suspicious behavior, or unsafe outputs to deployers or developers.
- Maintain human oversight and apply judgment to mitigate potential security or ethical risks during interactions.
Users accept responsibility for securely deploying, managing, and using this open-source LLM. The model is provided "as-is," without explicit or implied warranty regarding security or fitness for any specific application or environment.
- **Training stack:** [Fast-LLM](https://github.com/ServiceNow/Fast-LLM)
@misc{radhakrishna2025apriel1515bthinker,
      title={Apriel-1.5-15b-Thinker}, 
      author={Shruthan Radhakrishna and Aman Tiwari and Aanjaneya Shukla and Masoud Hashemi and Rishabh Maheshwary and Shiva Krishna Reddy Malay and Jash Mehta and Pulkit Pattnaik and Saloni Mittal and Khalil Slimi and Kelechi Ogueji and Akintunde Oladipo and Soham Parikh and Oluwanifemi Bamgbose and Toby Liang and Ahmed Masry and Khyati Mahajan and Sai Rajeswar Mudumba and Vikas Yadav and Sathwik Tejaswi Madhusudhan and Torsten Scholak and Sagar Davasam and Srinivas Sunkara and Nicholas Chapados},
      url={https://arxiv.org/abs/2510.01141}, 