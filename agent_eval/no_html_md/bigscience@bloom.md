BigScience Large Open-science Open-access Multilingual Language Model  
Current Checkpoint: **Training Iteration  95000**
Link to paper: [here](https://arxiv.org/abs/2211.05100)
BLOOM is an autoregressive Large Language Model (LLM), trained to continue text from a prompt on vast amounts of text data using industrial-scale computational resources. As such, it is able to output coherent text in 46 languages and 13 programming languages that is hardly distinguishable from text written by humans. BLOOM can also be instructed to perform text tasks it hasn't been explicitly trained for, by casting them as text generation tasks.
*This section provides information about the model type, version, license, funders, release date, developers, and contact information.*
*It is useful for anyone who wants to reference the model.*
**Developed by:** BigScience ([website](https://bigscience.huggingface.co))
*All collaborators are either volunteers or have an agreement with their employer. (Further breakdown of participants forthcoming.)*
**Model Type:** Transformer-based Language Model
**Checkpoints format:** `transformers` (Megatron-DeepSpeed format available [here](https://huggingface.co/bigscience/bloom-optimizer-states))
**Languages:** Multiple; see [training data](#training-data)
**License:** RAIL License v1.0 ([link](https://huggingface.co/spaces/bigscience/license) / [article and FAQ](https://bigscience.huggingface.co/blog/the-bigscience-rail-license))
**Release Date Estimate:** Monday, 11.July.2022
**Send Questions to:** bigscience-contact@googlegroups.com
**Cite as:** BigScience, _BigScience Language Open-science Open-access Multilingual (BLOOM) Language Model_. International, May 2021-May 2022
* Hugging Face ([website](https://huggingface.co)).
* Organizations of contributors.  *(Further breakdown of organizations forthcoming.)*
*This section includes details about the model objective and architecture, and the compute infrastructure.*
*It is useful for people interested in model development.*
Please see [the BLOOM training README](https://github.com/bigscience-workshop/bigscience/tree/master/train/tr11-176B-ml#readme) for full details on replicating training.
### Model Architecture and Objective
* Modified from Megatron-LM GPT2 (see [paper](https://arxiv.org/abs/1909.08053), [BLOOM Megatron code](https://github.com/bigscience-workshop/Megatron-DeepSpeed)):
* Layer normalization applied to word embeddings layer (`StableEmbedding`; see [code](https://github.com/facebookresearch/bitsandbytes), [paper](https://arxiv.org/pdf/2110.02861.pdf))
* ALiBI positional encodings (see [paper](https://arxiv.org/pdf/2108.12409.pdf)), with GeLU activation functions
    * 3,596,615,680 embedding parameters
    * 70 layers, 112 attention heads
    * Hidden layers are 14336-dimensional
    * Sequence length of 2048 tokens used (see [BLOOM tokenizer](https://huggingface.co/bigscience/tokenizer), [tokenizer description](#tokenization))
**Objective Function:** Cross Entropy with mean reduction (see [API documentation](https://pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html#torch.nn.CrossEntropyLoss)).
Jean Zay Public Supercomputer, provided by the French government (see [announcement](https://www.enseignementsup-recherche.gouv.fr/fr/signature-du-marche-d-acquisition-de-l-un-des-supercalculateurs-les-plus-puissants-d-europe-46733)).
* 384 A100 80GB GPUs (48 nodes)
* Additional 32 A100 80GB GPUs (4 nodes) in reserve
* 8 GPUs per node Using NVLink 4 inter-gpu connects, 4 OmniPath links
* Inter-node connect: Omni-Path Architecture (OPA)
* NCCL-communications network: a fully dedicated subnet
* Disc IO network: shared network with other types of nodes
* Megatron-DeepSpeed ([Github link](https://github.com/bigscience-workshop/Megatron-DeepSpeed))
* DeepSpeed ([Github link](https://github.com/microsoft/DeepSpeed))
* PyTorch (pytorch-1.11 w/ CUDA-11.5; see [Github link](https://github.com/pytorch/pytorch))
* apex ([Github link](https://github.com/NVIDIA/apex))
*This section provides information about the training data, the speed and size of training elements, and the environmental impact of training.*
*It is useful for people who want to learn more about the model inputs and training footprint.*
*This section provides a high-level overview of the training data. It is relevant for anyone who wants to know the basics of what the model is learning.*
Details for each dataset are provided in individual [Data Cards](https://huggingface.co/spaces/bigscience/BigScienceCorpus), and the sizes of each of their contributions to the aggregated training data are presented in an [Interactive Corpus Map](https://huggingface.co/spaces/bigscience-catalogue-lm-data/corpus-map).
-   In 1.6TB of pre-processed text, converted into 350B unique tokens (see [the tokenizer section](#tokenization) for more.)
The pie chart shows the distribution of languages in training data.
![pie chart showing the distribution of languages in training data](https://github.com/bigscience-workshop/model_card/blob/main/assets/data/pie_v2.svg?raw=true)
The following tables shows the further distribution of Niger-Congo & Indic languages and programming languages in the training data.
Distribution of Niger Congo and Indic languages.
Distribution of programming languages.
**Tokenization:** The BLOOM tokenizer ([link](https://huggingface.co/bigscience/tokenizer)), a learned subword tokenizer trained using:
- A byte-level Byte Pair Encoding (BPE) algorithm 
- A simple pre-tokenization rule, no normalization
- A vocabulary size of 250,680
It was trained on a subset of a preliminary version of the corpus using alpha-weighting per language.  
Training logs: [Tensorboard link](https://huggingface.co/tensorboard/bigscience/tr11-176B-ml-logs/)
    - Started 11th March, 2022 11:42am PST
    - Estimated end: 5th July, 2022
    - Full checkpoint with optimizer states: 2.3TB
- Training throughput: About 150 TFLOP per GPU per second
- Estimated cost of training: Equivalent of $2-5M in cloud computing (including preliminary experiments)
- Server training location: Île-de-France, France
The training supercomputer, Jean Zay ([website](http://www.idris.fr/eng/jean-zay/jean-zay-presentation-eng.html)), uses mostly nuclear energy. The heat generated by it is reused for heating campus housing.
**Estimated carbon emissions:**  *(Forthcoming.)*
**Estimated electricity usage:** *(Forthcoming.)*
*This section addresses questions around how the model is intended to be used, discusses the foreseeable users of the model (including those affected by the model), and describes uses that are considered out of scope or misuse of the model.*
*It is useful for anyone considering using the model or who is affected by the model.*
This model can be easily used and deployed using HuggingFace's ecosystem. This needs `transformers` and `accelerate` installed. The model can be downloaded as follows:
This model is being created in order to enable public research on large language models (LLMs). LLMs are intended to be used for language generation or as a pretrained base model that can be further fine-tuned for specific tasks. Use cases below are not exhaustive.
-   Exploring characteristics of language generated by a language model
    -   Examples: Cloze tests, counterfactuals, generations with reframings
-   Tasks that leverage language models include: Information Extraction, Question Answering, Summarization
### Misuse and Out-of-scope Use
*This section addresses what users ought not do with the model.*
See the [BLOOM License](https://huggingface.co/spaces/bigscience/license), Attachment A, for detailed usage restrictions. The below list is non-exhaustive, but lists some easily foreseeable problematic use cases.
Using the model in [high-stakes](#high-stakes) settings is out of scope for this model.  The model is not designed for [critical decisions](#critical-decisions) nor uses with any material consequences on an individual's livelihood or wellbeing. The model outputs content that appears factual but may not be correct.  
-   Usage in biomedical domains, political and legal domains, or finance domains
-   Usage for evaluating or scoring individuals, such as for employment, education, or credit
-   Applying the model for critical automatic decisions, generating factual content, creating reliable summaries, or generating predictions that must be correct
Intentionally using the model for harm, violating [human rights](#human-rights), or other kinds of malicious activities, is a misuse of this model. This includes:
-   Disinformation and influence operations
-   Disparagement and defamation
-   Unconsented impersonation and imitation
-   Generating content without attribution to the model, as specified in the [RAIL License, Use Restrictions](https://huggingface.co/spaces/bigscience/license)
-   Community advocates, including human and civil rights groups
-   Users of derivatives created by Direct Users, such as those using software with an [intended use](#intended-use)
-   Users of [Derivatives of the Model, as described in the License](https://huggingface.co/spaces/bigscience/license)
### Others Affected (Parties Prenantes)
-   People and groups referred to by the LLM
-   People and groups exposed to outputs of, or decisions based on, the LLM
-   People and groups whose original work is included in the LLM
*This section identifies foreseeable harms and misunderstandings.*
-   Overrepresent some viewpoints and underrepresent others
-   Contain [personal information](#personal-data-and-information)
    -   Hateful, abusive, or violent language
    -   Discriminatory or prejudicial language
    -   Content that may not be appropriate for all settings, including sexual content
-   Make errors, including producing incorrect information as if it were factual
-   Generate irrelevant or repetitive outputs
-   Induce users into attributing human traits to it, such as sentience or consciousness
*This section describes the evaluation protocols and provides the results.*
*This section describes the different ways performance is calculated and why.*
And multiple different metrics for specific tasks. _(More evaluation metrics forthcoming upon completion of evaluation protocol.)_
*This section lists some different aspects of BLOOM models. Its focus is on aspects that are likely to give rise to high variance in model behavior.*
- Language, such as English or Yoruba
- Domain, such as newswire or stories
- Demographic characteristics, such as gender or nationality
*Results are based on the [Factors](#factors) and [Metrics](#metrics).*
WARNING: This section used to contain much more results, however they were not correct and we released without the approval of the evaluation working group. We are currently in the process of fixing the evaluations.
See this repository for JSON files: https://github.com/bigscience-workshop/evaluation-results
Final checkpoint after 95K steps:
For more see: https://huggingface.co/bigscience/tr11-176B-ml-logs
*This section provides information on warnings and potential mitigations.*
-   Indirect users should be made aware when the content they're working with is created by the LLM.
-   Users should be aware of [Risks and Limitations](#risks-and-limitations), and include an appropriate age disclaimer or blocking interface as necessary.
-   Models trained or finetuned downstream of BLOOM LM should include an updated Model Card.
-   Users of the model should provide mechanisms for those affected to provide feedback, such as an email address for comments.
*This section defines common terms and how metrics are calculated.*
-   **Loss:** A calculation of the difference between what the model has learned and what the data shows ("groundtruth"). The lower the loss, the better. The training process aims to minimize the loss. 
-   **Perplexity:** This is based on what the model estimates the probability of new data is. The lower the perplexity, the better.  If the model is 100% correct at predicting the next token it will see, then the perplexity is 1. Mathematically this is calculated using entropy. 
-   **High-stakes settings:** Such as those identified as "high-risk AI systems" and "unacceptable risk AI systems" in the European Union's proposed [Artificial Intelligence (AI) Act](https://artificialintelligenceact.eu/annexes/).
-   **Critical decisions:** Such as those defined in [the United States' proposed Algorithmic Accountability Act](https://www.congress.gov/117/bills/s3572/BILLS-117s3572is.pdf).
-   **Human rights:** Includes those rights defined in the [Universal Declaration of Human Rights](https://www.un.org/sites/un2.un.org/files/2021/03/udhr.pdf).
-  **Personal Data and Personal Information:** Personal data and information is defined in multiple data protection regulations, such as "[personal data](https://gdpr-info.eu/issues/personal-data/)" in the [European Union's General Data Protection Regulation](https://gdpr-info.eu); and "personal information" in the Republic of South Africa's [Protection of Personal Information Act](https://www.gov.za/sites/default/files/gcis_document/201409/3706726-11act4of2013popi.pdf), The People's Republic of China's [Personal information protection law](http://en.npc.gov.cn.cdurl.cn/2021-12/29/c_694559.htm).
- **Sensitive characteristics:** This includes specifically protected categories in human rights (see [UHDR, Article 2](https://www.un.org/sites/un2.un.org/files/2021/03/udhr.pdf)) and personal information regulation (see GDPR, [Article 9; Protection of Personal Information Act, Chapter 1](https://www.gov.za/sites/default/files/gcis_document/201409/3706726-11act4of2013popi.pdf))
- **Deception:** Doing something to intentionally mislead individuals to believe something that is false, such as by creating deadbots or chatbots on social media posing as real people, or generating text documents without making consumers aware that the text is machine generated.
*This section provides links to writing on dataset creation, technical specifications, lessons learned, and initial results.*
For academic (or any) usage, we published the intermediate checkpoints, corresponding to the model state at each 5000 steps. Please follow [this link](https://huggingface.co/bigscience/bloom-176-intermediate) to get these checkpoints.
Blog post detailing the design choices during the dataset creation: https://bigscience.huggingface.co/blog/building-a-tb-scale-multilingual-dataset-for-language-modeling
Blog post summarizing how the architecture, size, shape, and pre-training duration where selected: https://bigscience.huggingface.co/blog/what-language-model-to-train-if-you-have-two-million-gpu-hours
More details on the architecture/optimizer: https://github.com/bigscience-workshop/bigscience/tree/master/train/tr11-176B-ml
Blog post on the hardware/engineering side: https://bigscience.huggingface.co/blog/which-hardware-to-train-a-176b-parameters-model
Details on the distributed setup used for the training: https://github.com/bigscience-workshop/bigscience/tree/master/train/tr11-176B-ml
Tensorboard updated during the training: https://huggingface.co/bigscience/tr11-176B-ml-logs/tensorboard#scalars&tagFilter=loss
Insights on how to approach training, negative results: https://github.com/bigscience-workshop/bigscience/blob/master/train/lessons-learned.md
Details on the obstacles overcome during the preparation on the engineering side (instabilities, optimization of training throughput, so many technical tricks and questions): https://github.com/bigscience-workshop/bigscience/blob/master/train/tr11-176B-ml/chronicles.md
Initial prompting experiments using interim checkpoints: https://huggingface.co/spaces/bigscience/bloom-book
The checkpoints in this repo correspond to the HuggingFace Transformers format. If you want to use our fork of [Megatron-DeepSpeed](https://github.com/bigscience-workshop/Megatron-DeepSpeed) that the model was trained with, you'd want to use [this repo instead](https://huggingface.co/bigscience/bloom-optimizer-states).
Many intermediate checkpoints are available at https://huggingface.co/bigscience/bloom-intermediate/
*Ordered roughly chronologically and by amount of time spent on creating this model card.*
Margaret Mitchell, Giada Pistilli, Yacine Jernite, Ezinwanne Ozoani, Marissa Gerchick, Nazneen Rajani, Sasha Luccioni, Irene Solaiman, Maraim Masoud, Somaieh Nikpoor, Carlos Muñoz Ferrandis, Stas Bekman, Christopher Akiki, Danish Contractor, David Lansky, Angelina McMillan-Major, Tristan Thrush, Suzana Ilić, Gérard Dupont, Shayne Longpre, Manan Dey, Stella Biderman, Douwe Kiela, Emi Baylor, Teven Le Scao, Aaron Gokaslan, Julien Launay, Niklas Muennighoff