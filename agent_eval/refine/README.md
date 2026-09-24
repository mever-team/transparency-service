# Import Evaluation Report 

## 🗄️ Data gathering
To create an evaluation dataset for the refine functionality, 32 samples of technical content were gathered from the same Hugging Face model cards used for the import evaluation, with the assistance of ChatGPT. The samples were then manually selected to represent content likely to appear in model descriptions and other fields intended for non-expert readers. More technical content intended for technical fields was excluded.

For each sample, ChatGPT was prompted to create a requirements checklist that the refine output was expected to satisfy. The checklist consists of two types of requirements: “mention” and “explain”. These requirements were used to evaluate the refine functionality in terms of information retention and technical explainability, respectively. The checklists were partially manually checked.

The resulting dataset contains 144 “mention” requirements and 152 “explain” requirements, for a total of 296 checklist items. The evaluation dataset is available [here](./results/5_manually_corrected/dataset.json)

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

For each dimension, the final score is calculated as:
**`Satisfaction Score = Total Points / Number of Items`**

The evaluation labels are obtained by prompting an LLM. The `gpt-oss:120b-cloud` from Ollama was used for this job. The evaluation labels were partially manually checked.

Furthermore, to obtain the FF checklist, the same `gpt-oss:120b-cloud` model was prompted to first generate a factual checklist from the output text and then evaluate each fact against the corresponding original sample.

## 📊 Results

### **Overall Satisfaction score 84.2%**
| Dimention | Total | Fully satisfied | Partially satisfied | Not satisfied | Satisfaction score |
|--------|-------|-----------------|---------------------|---------------|--------------------|
| IR (Information Retention)     | 144   | 133 / 144 (92.36%) | 7 / 144 (4.86%)  | 	4 / 144 (2.78%) | 94.79% |
| TE (Technical Explainability)     | 152   | 82 / 152 (53.95%) | 35 / 152 (23.03%)  | 35 / 152 (23.03%) | 65.46% |
| FF (Factual Faithfulness)     | 204   | 177 / 204 (86.76%) | 16 / 204 (7.84%)  | 11 / 204 (5.39%) | 90.69% |

The above are the final results after 3 refine prompt adjustments. It was obserbed that there was a trade-off between FF and TE depending on the strictness and emphasis on preserving the original facts. 

For the 11 UNSUPPORTED FF (false facts that the refine produced): 
* 3 of them were wrong or oversimplified explanations of terms found in the original, which ended up as unsupported facts
* 6 of them were added assumptions about the usage / effectiveness of the model (basically the refine added extra adjectives and adverbs not included in the original like effective, efficiently etc.)
* and 2 were not stated by the original sample. (facts that are not present or related to the original text)

For the 4 Not satisfied IR (facts that the refine missed): 
* 2 of them were information loss due to oversimplification, 
* and 2 facts that were simply not stated at all.

The 35 Not satisfied TE (terms that the refine was expected to explain but did not) the terms are:
* parameter-efficient
* Mixture-of-Experts
* embedding
* image embeddings
* text embedding
* Rotary Position Embeddings
* supervised fine-tuning
* EnCodec speech features
* weakly supervised
* Pixel-level Unified Transformer (UiT)
* VAE (Variational Autoencoder) 
* shared token space
* subject-driven personalization
* denoising 
* causal temporal modeling
* Long-horizon Search
* Sliding Window Attention (SWA) 
* discrete diffusion
* layout detection
* content recognition
* coding agents
* model distillation

The results can be found in an HTML [here](./results/5_manually_corrected/evaluation_report.html)


