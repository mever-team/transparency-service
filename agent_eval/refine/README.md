# Refine Evaluation Report 

## 🗄️ Data gathering
To create an evaluation dataset for the refine functionality, 32 samples of technical content were gathered from the same Hugging Face model cards used for the import evaluation, with the assistance of ChatGPT. The samples were then manually selected to represent content likely to appear in model descriptions and other fields intended for non-expert readers. More technical content intended for technical fields was excluded.

For each sample, ChatGPT was prompted to create a requirements checklist that the refine output was expected to satisfy. The checklist consists of two types of requirements: “mention” and “explain”. These requirements were used to evaluate the refine functionality in terms of information retention and technical explainability, respectively. The checklists were partially manually checked.

The resulting dataset contains 144 “mention” requirements and 149 “explain” requirements, for a total of 293 checklist items. The evaluation dataset is available [here](./dataset.json)

<details>
<summary><strong>Example of one sample:</strong></summary>
<pre>
{
   "id": 4,
   "input": "DeepSeek-R1-Zero is trained through large-scale reinforcement learning (RL) without supervised fine-tuning (SFT) as a preliminary step, allowing it to develop reasoning behaviors through reinforcement learning alone.",
   "ground_truth": [
      {
            "id": 1,
            "type": "mention",
            "requirement": "States that DeepSeek-R1-Zero is trained using reinforcement learning (RL)."
      },
      {
            "id": 2,
            "type": "explain",
            "requirement": "Explains that reinforcement learning is a training approach in which the model learns by receiving feedback or rewards for its behavior."
      },
      {
            "id": 3,
            "type": "mention",
            "requirement": "States that the reinforcement learning used for training is performed at large scale."
      },
      {
            "id": 4,
            "type": "mention",
            "requirement": "States that DeepSeek-R1-Zero is trained without supervised fine-tuning (SFT) as a preliminary or initial training step."
      },
      {
            "id": 5,
            "type": "explain",
            "requirement": "Explains that supervised fine-tuning is a training process in which a model is further trained using examples with desired or labeled outputs."
      },
      {
            "id": 6,
            "type": "mention",
            "requirement": "Clearly preserves the distinction that SFT is omitted specifically as a preliminary step before the reinforcement learning stage."
      },
      {
            "id": 7,
            "type": "mention",
            "requirement": "States that DeepSeek-R1-Zero develops reasoning behaviors through reinforcement learning."
      },
      {
            "id": 8,
            "type": "explain",
            "requirement": "Makes clear that these reasoning behaviors emerge from the reinforcement learning process rather than from a preceding supervised fine-tuning stage."
      }
   ],
   "source": "https://huggingface.co/deepseek-ai/DeepSeek-R1"
}
</pre>
</details>

## 🧭 Methodology
To evaluate the model, we ask 3 questions:
1.	Information Retention (IR): How much of the original information is preserved
2.	Technical Explainability (TE): How many of the technical terms were explained 
3.	Factual Faithfulness (FF): How much of the information stated in the output is supported by the original, and how much is fabricated. 

the possible evaluation labels for each are:
1. IR: 
   * "YES" = 1 point
   * "PARTIAL" = 0.5 points
   * "NO" = 0 points
2. TE:
   * "YES" = 1 point
   * "PARTIAL" = 0.5 points
   * "NO" = 0 points
3. FF:
   * "SUPPORTED" = 1 point
   * "PARTIAL" = 0.5 points
   * "UNSUPPORTED" = 0 points
   * "CONTRADICTION" = -1 points

For each dimension, the final score is calculated as:
**`Satisfaction Score = Total Points / Number of Items`**

The evaluation labels are obtained by prompting an LLM. The `gpt-oss:120b-cloud` from Ollama was used for this job. The evaluation labels were partially manually checked.

Furthermore, to obtain the FF checklist, the same `gpt-oss:120b-cloud` model was prompted to first generate a factual checklist from the output text and then evaluate each fact against the corresponding original sample.

## 🧪 Experimental Setup

Models checked:
* mistral:latest
* qwen2.5:7b
* qwen3:4b-instruct
* qwen3:4b-thinking
* granite4:3b
* phi4-mini
* llama3.2:3b

The agent was enhanced with:
* A **glossary** with 164 technical terms and their definitions. If any of them are detected in the input, the definitions are then injected in the system prompt.
* A **tool call** that the LLM can use if a technical terms is not included in the glossary. This tool prompts `gpt-oss:120b-cloud` to provide an explanation of the term.
* Improvements to prompt for better explainability.

## 📊 Results

The best performing model with glossary + tool enhancements is qwen2.5:7b. These two enhasments increased the TE Satisfaction score by +10% and the overall Satisfaction score by +5.9%. 

### **Overall Satisfaction score 86.24% of qwen2.5:7b**
| Dimention | Total | Fully satisfied | Partially satisfied | Not satisfied | Satisfaction score |
|--------|-------|-----------------|---------------------|---------------|--------------------|
| IR (Information Retention)     | 144   | 139 / 144 (96.53%) | 0 / 144 (0%)  | 	5 / 144 (3.47%) | 96.53% |
| TE (Technical Explainability)     | 149   | 95 / 149 (63.76%) | 10 / 149 (6.71%)  | 44 / 149 (29.53%) | 67.11% |
| FF (Factual Faithfulness)     | 183   | 165 / 183 (90.17%) | 13 / 183 (7.1%)  | 5 / 183 (2.73%) | 93.72% |

The bottleneck for obtaining higher TE scores is the ability of the agent model (qwen2.5:7b) to decide if something needs explanation or not. This behavior can be partially changed through the system prompt but unfortunately there is a tradeoff between TE and FF scores. The more freedom the model has on explaining terms, the less faithful it becomes to the original text introducing unsupported claims. The prompt was optimized to yield good TE results without compromising the IR and FF scores. 

For the 5 UNSUPPORTED FF (false facts that the refine produced):
* 2 of them were wrong or oversimplified explanations of terms found in the original, which ended up as unsupported facts
* 1 of them were added assumptions about the usage / effectiveness of the model (basically the refine added extra adjectives and adverbs not included in the original like effective, efficiently etc.)
* and 2 were not stated by the original sample. (facts that are not present or related to the original text)

For the 5 Not satisfied IR (facts that the refine missed): 
States that coarse (L0) EnCodec speech features are obtained from the text and reference audio.
States that the SRR triplet paradigm simplifies the multi-tool pipeline used by modular approaches.
* 4 of them were information loss due to oversimplification, 
* and 1 facts that were simply not stated at all.

The 51 Not satisfied TE (terms that the refine was expected to explain but did not) the terms are:
* embedding
* CLIP image embeddings
* labeled data
* SLM 
* text-to-speech
* EnCodec speech features
* downstream tasks
* multi-tool pipeline
* VAE (Variational Autoencoder)
* disjoint text encoders
* encoding 
* causal temporal modeling
* agentic model
* Long-horizon Search
* reinforcement learning
* agentic reinforcement learning
* SWE-Bench
* complex reasoning tasks
* NLP applications
* Rotary Position Embeddings
* discrete diffusion
* conditioning frame

### Other models
* **mistral:latest**: Best raw performance. Low FF score with glossary
* **qwen3:4b-instruct**: Bad with number understanding. Results in contradictory facts
* **qwen3:4b-thinking**: Super slow
* **granite4:3b**: OK but not good. Nothing special to report
* **phi4-mini**: OK but not good. Nothing special to report
* **llama3.2:3b**: OK but not good. Nothing special to report

The results of **qwen2.5:7b** can be found in an HTML [here](./results/12_qwen2.5:7b/evaluation_report.html)

