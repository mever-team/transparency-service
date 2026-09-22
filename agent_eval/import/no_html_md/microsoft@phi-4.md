[Phi-4 Technical Report](https://arxiv.org/pdf/2412.08905)
Our training data is an extension of the data used for Phi-3 and includes a wide variety of sources from:
1. Publicly available documents filtered rigorously for quality, selected high-quality educational data, and code.
2. Newly created synthetic, “textbook-like” data for the purpose of teaching math, coding, common sense reasoning, general knowledge of the world (science, daily activities, theory of mind, etc.).
3. Acquired academic books and Q&A datasets.
4. High quality chat format supervised data covering various topics to reflect human preferences on different aspects such as instruct-following, truthfulness, honesty and helpfulness.
Multilingual data constitutes about 8% of our overall data. We are focusing on the quality of data that could potentially improve the reasoning ability for the model, and we filter the publicly available documents to contain the correct level of knowledge.
We evaluated `phi-4` using [OpenAI’s SimpleEval](https://github.com/openai/simple-evals) and our own internal benchmarks to understand the model’s capabilities, more specifically: 
* **MMLU:** Popular aggregated dataset for multitask language understanding.
* **MATH:** Challenging competition math problems.
* **GPQA:** Complex, graduate-level science questions.
* **DROP:** Complex comprehension and reasoning.
* **MGSM:** Multi-lingual grade-school math.
* **HumanEval:** Functional code generation.
* **SimpleQA:** Factual responses.
`phi-4` has adopted a robust safety post-training approach. This approach leverages a variety of both open-source and in-house generated synthetic datasets. The overall technique employed to do the safety alignment is a combination of SFT (Supervised Fine-Tuning) and iterative DPO (Direct Preference Optimization), including publicly available datasets focusing on helpfulness and harmlessness as well as various questions and answers targeted to multiple safety categories. 
### Safety Evaluation and Red-Teaming 
Prior to release, `phi-4` followed a multi-faceted evaluation approach. Quantitative evaluation was conducted with multiple open-source safety benchmarks and in-house tools utilizing adversarial conversation simulation. For qualitative safety evaluation, we collaborated with the independent AI Red Team (AIRT) at Microsoft to assess safety risks posed by `phi-4` in both average and adversarial user scenarios. In the average user scenario, AIRT emulated typical single-turn and multi-turn interactions to identify potentially risky behaviors. The adversarial user scenario tested a wide range of techniques aimed at intentionally subverting the model’s safety training including jailbreaks, encoding-based attacks, multi-turn attacks, and adversarial suffix attacks.   
Please refer to the technical report for more details on safety alignment. 
To understand the capabilities, we compare `phi-4` with a set of models over OpenAI’s SimpleEval benchmark. 
At the high-level overview of the model quality on representative benchmarks. For the table below, higher numbers indicate better performance: 
\* These scores are lower than those reported by Meta, perhaps because simple-evals has a strict formatting requirement that Llama models have particular trouble following. We use the simple-evals framework because it is reproducible, but Meta reports 77 for MATH and 88 for HumanEval on Llama-3.3-70B.
Given the nature of the training data, `phi-4` is best suited for prompts using the chat format as follows: 
You are a medieval knight and must provide explanations to modern people.<|im_end|>
How should I explain the Internet?<|im_end|>
<|im_start|>assistant<|im_sep|>
pipeline = transformers.pipeline(
    model_kwargs={"torch_dtype": "auto"},
    {"role": "system", "content": "You are a medieval knight and must provide explanations to modern people."},
    {"role": "user", "content": "How should I explain the Internet?"},
outputs = pipeline(messages, max_new_tokens=128)
print(outputs[0]["generated_text"][-1])
## Responsible AI Considerations
Like other language models, `phi-4` can potentially behave in ways that are unfair, unreliable, or offensive. Some of the limiting behaviors to be aware of include:   
* **Quality of Service:** The model is trained primarily on English text. Languages other than English will experience worse performance. English language varieties with less representation in the training data might experience worse performance than standard American English. `phi-4` is not intended to support multilingual use. 
* **Representation of Harms & Perpetuation of Stereotypes:** These models can over- or under-represent groups of people, erase representation of some groups, or reinforce demeaning or negative stereotypes. Despite safety post-training, these limitations may still be present due to differing levels of representation of different groups or prevalence of examples of negative stereotypes in training data that reflect real-world patterns and societal biases.  
* **Inappropriate or Offensive Content:** These models may produce other types of inappropriate or offensive content, which may make it inappropriate to deploy for sensitive contexts without additional mitigations that are specific to the use case.  
* **Information Reliability:** Language models can generate nonsensical content or fabricate content that might sound reasonable but is inaccurate or outdated.   
* **Limited Scope for Code:** Majority of `phi-4` training data is based in Python and uses common packages such as `typing`, `math`, `random`, `collections`, `datetime`, `itertools`. If the model generates Python scripts that utilize other packages or scripts in other languages, we strongly recommend users manually verify all API uses.  
Developers should apply responsible AI best practices and are responsible for ensuring that a specific use case complies with relevant laws and regulations (e.g. privacy, trade, etc.). Using safety services like [Azure AI Content Safety](https://azure.microsoft.com/en-us/products/ai-services/ai-content-safety) that have advanced guardrails is highly recommended. Important areas for consideration include:
* **Allocation:** Models may not be suitable for scenarios that could have consequential impact on legal status or the allocation of resources or life opportunities (ex: housing, employment, credit, etc.) without further assessments and additional debiasing techniques. 
* **High-Risk Scenarios:** Developers should assess suitability of using models in high-risk scenarios where unfair, unreliable or offensive outputs might be extremely costly or lead to harm. This includes providing advice in sensitive or expert domains where accuracy and reliability are critical (ex: legal or health advice). Additional safeguards should be implemented at the application level according to the deployment context.  
* **Misinformation:** Models may produce inaccurate information. Developers should follow transparency best practices and inform end-users they are interacting with an AI system. At the application level, developers can build feedback mechanisms and pipelines to ground responses in use-case specific, contextual information, a technique known as Retrieval Augmented Generation (RAG).    
* **Generation of Harmful Content:** Developers should assess outputs for their context and use available safety classifiers or custom solutions appropriate for their use case.  
* **Misuse:** Other forms of misuse such as fraud, spam, or malware production may be possible, and developers should ensure that their applications do not violate applicable laws and regulations.
* **Data Summary:** https://huggingface.co/microsoft/phi-4/blob/main/data_summary_card.md