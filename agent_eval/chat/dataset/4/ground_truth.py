GROUND_TRUTH = {
    "overview": [
        {
            "question": "What is the name of this model?",
            "ground_truth": [
                {"sentence": "Online\\_RINE", "section": "overview", "field": "name"},
            ],
        },
        {
            "question": "What is this model used for?",
            "ground_truth": [
                {"sentence": "The proposed framework introduces a continual adaptive pipeline for robust AI-generated image detection under evolving real-world conditions.", "section": "overview", "field": "description"},
                {"sentence": "Detecting ai-generated images", "section": "use", "field": "use_cases"},
            ],
        },
        {
            "question": "Who created this model?",
            "ground_truth": [
                {"sentence": "CERTH - The Centre for Research & Technology, Hellas", "section": "overview", "field": "creator"},
            ],
        },
        {
            "question": "When was this model released?",
            "ground_truth": [
                {"sentence": "2026-05-01", "section": "overview", "field": "date"},
            ],
        },
        {
            "question": "What version is this model?",
            "ground_truth": [
                {"sentence": "1.0", "section": "overview", "field": "version"},
            ],
        },
        {
            "question": "What type of model is this?",
            "ground_truth": [
                {"sentence": "Transformer", "section": "overview", "field": "type"},
            ],
        },
        {
            "question": "How many parameters does this model have?",
            "ground_truth": [],
        },
        {
            "question": "What is the task of this model?",
            "ground_truth": [
                {"sentence": "Image Classification", "section": "overview", "field": "task"},
                {"sentence": "The proposed framework introduces a continual adaptive pipeline for robust AI-generated image detection under evolving real-world conditions.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "What is the license of this model?",
            "ground_truth": [
                {"sentence": "Apache License 2.0", "section": "overview", "field": "license"},
            ],
        },
        {
            "question": "Where can I find this model?",
            "ground_truth": [
                {"sentence": "[https://github.com/mever-team/WildFC](https://github.com/mever-team/WildFC)", "section": "overview", "field": "home"},
            ],
        },
        {
            "question": "Who can I contact about this model?",
            "ground_truth": [
                {"sentence": "Thanasis Pantsios: [apantsios@iti.gr](mailto:apantsios@iti.gr)", "section": "overview", "field": "contact"},
            ],
        },
        {
            "question": "How should I cite this model?",
            "ground_truth": [
                {"sentence": "@inproceedings{pantsios2026automated,\n\ntitle={Automated In-the-Wild Data Collection for Continual AI Generated Image Detection},\n\nauthor={Pantsios, Athanasios and Karageorgiou, Dimitrios and Koutlis, Christos and Karantaidis, George and Papadopoulou, Olga and Papadopoulos, Symeon},\n\nbooktitle={The 5th ACM International Workshop on Multimedia AI against Disinformation (MAD '26)},\n\nyear={2026},\n\ndoi={10.1145/3810988.3812662}\n\n}", "section": "overview", "field": "citation"},
            ],
        },
    ],

    "use": [
        {
            "question": "What are the intended use cases?",
            "ground_truth": [
                {"sentence": "Detecting ai-generated images", "section": "use", "field": "use_cases"},
                {"sentence": "The proposed framework introduces a continual adaptive pipeline for robust AI-generated image detection under evolving real-world conditions.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "What level of human oversight is required?",
            "ground_truth": [
                {"sentence": "human-in-the-loop", "section": "use", "field": "oversight"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Treating the probability score as a final verdict rather than a helpful indicator, or relying on it for unsupervised decision-making without human review.", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "Who are the intended user groups?",
            "ground_truth": [
                {"sentence": "Journalists, Fact-checkers, Researchers,\u00a0General public", "section": "use", "field": "user_groups"},
            ],
        },
        {
            "question": "What is this model not intended for?",
            "ground_truth": [
                {"sentence": "Treating the probability score as a final verdict rather than a helpful indicator, or relying on it for unsupervised decision-making without human review.", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "What software does this model require?",
            "ground_truth": [
                {"sentence": "Detailed software implementation is available at: [https://github.com/mever-team/WildFC/](https://github.com/mever-team/WildFC/).", "section": "use", "field": "software"},
            ],
        },
        {
            "question": "How do I run / use this model?",
            "ground_truth": [
                {"sentence": "Detailed usage instructions are available at: [https://github.com/mever-team/WildFC/](https://github.com/mever-team/WildFC/)", "section": "use", "field": "instructions"},
                {"sentence": "The model accepts an image as input and returns a probability score indicating whether the image is synthetic.", "section": "use", "field": "inputs_outputs"},
                {"sentence": "It also identifies the top ten image patches that most influenced the decision, providing bounding boxes and probability scores for each.", "section": "use", "field": "inputs_outputs"},
                {"sentence": "Running the model requires a GPU with at least 4 GB of VRAM.", "section": "use", "field": "hardware"},
            ],
        },
        {
            "question": "What are the inputs and outputs of the model?",
            "ground_truth": [
                {"sentence": "The model accepts an image as input and returns a probability score indicating whether the image is synthetic.", "section": "use", "field": "inputs_outputs"},
                {"sentence": "It also identifies the top ten image patches that most influenced the decision, providing bounding boxes and probability scores for each.", "section": "use", "field": "inputs_outputs"},
            ],
        },
        {
            "question": "What factors affect the model's performance?",
            "ground_truth": [
                {"sentence": "Model performance is highly dependent on data quality, e.g., multi-cycle social media operations (repeated upload/download cycles) and heavy compression, both of which impair detection accuracy independently.", "section": "use", "field": "factors"},
            ],
        },
        {
            "question": "What hardware is required?",
            "ground_truth": [
                {"sentence": "Running the model requires a GPU with at least 4 GB of VRAM.", "section": "use", "field": "hardware"},
            ],
        },
    ],

    "training": [
        {
            "question": "What datasets were used for training?",
            "ground_truth": [
                {"sentence": "[WildFC](https://huggingface.co/datasets/pthan12/WildFC) ,\u00a0[AIGenImages2026](https://huggingface.co/datasets/pthan12/AIGenImages2026),\u00a0[Twigma](https://yiqunchen.github.io/TWIGMA/),\u00a0[LDM](https://github.com/grip-unina/DMimageDetection),\u00a0[COCO]((https://cocodataset.org/)),\u00a0[LSUN](https://arxiv.org/abs/1506.03365), [OpenImages]((https://storage.googleapis.com/openimages/web/index.html) datasets", "section": "training", "field": "datasets"},
            ],
        },
        {
            "question": "Why were these training datasets chosen?",
            "ground_truth": [
                {"sentence": "The training data combines in-the-wild images with outputs from recent diffusion models along with real images from recent datasets.", "section": "training", "field": "motivation"},
                {"sentence": "This selection ensures the model remains adaptive by\u00a0 learning modern generative artifacts while building resilience against real-world media degradations.", "section": "training", "field": "motivation"},
            ],
        },
        {
            "question": "What preprocessing was applied during training?",
            "ground_truth": [
                {"sentence": "Gaussian blurring and JPEG compression with probability 0.5,\u00a0TextureCrop\u00a0for a 224x224 crop, random horizontal flip with probability 0.5.", "section": "training", "field": "preprocessing"},
            ],
        },
        {
            "question": "What standards were followed during training?",
            "ground_truth": [
                {"sentence": "IEEE", "section": "training", "field": "standards"},
            ],
        },
        {
            "question": "Is the training data up to date?",
            "ground_truth": [
                {"sentence": "yes", "section": "training", "field": "update"},
            ],
        },
    ],

    "evaluation": [
        {
            "question": "What datasets were used for evaluation?",
            "ground_truth": [
                {"sentence": "WildFC is an evolving in-the-wild dataset collected through an automated fact-check retrieval pipeline.", "section": "evaluation", "field": "datasets"},
                {"sentence": "The evaluation datasets were chosen to cover both sources of distribution shift identified as driving AID's non-stationary nature: shift from the continuous development of recent generative models (AIGenImages2026, MNW, Synthbuster, Nano-Consistent, and Echo-4o), and shift arising from real-world usage dynamics and platform-specific processing (Chameleon, ITW-SM, MediaEval-ITW, and Deepfake-Eval).", "section": "evaluation", "field": "motivation"},
            ],
        },
        {
            "question": "Why were these evaluation datasets chosen?",
            "ground_truth": [
                {"sentence": "The evaluation datasets were chosen to cover both sources of distribution shift identified as driving AID's non-stationary nature: shift from the continuous development of recent generative models (AIGenImages2026, MNW, Synthbuster, Nano-Consistent, and Echo-4o), and shift arising from real-world usage dynamics and platform-specific processing (Chameleon, ITW-SM, MediaEval-ITW, and Deepfake-Eval).", "section": "evaluation", "field": "motivation"},
            ],
        },
        {
            "question": "What preprocessing was applied during evaluation?",
            "ground_truth": [
                {"sentence": "The validation and test images are center-cropped at 224×224.", "section": "evaluation", "field": "preprocessing"},
            ],
        },
        {
            "question": "What standards were followed during evaluation?",
            "ground_truth": [
                {"sentence": "IEEE", "section": "evaluation", "field": "standards"},
            ],
        },
        {
            "question": "Is the evaluation data up to date?",
            "ground_truth": [
                {"sentence": "yes", "section": "evaluation", "field": "update"},
            ],
        },
    ],

    "performance": [
        {
            "question": "What does the performance analysis say?",
            "ground_truth": [
                {"sentence": "Online RINE raises average performance by +8.01% accuracy across both recent-generator and in-the-wild benchmarks combined, with particularly strong gains on previously challenging recent generators such as Echo-4o (48.75% \u2192 76.80% accuracy) and Nano-Consistent (63.81% \u2192 71.01% accuracy), while also improving in-the-wild robustness(+1.01% ACC on ITW-SM, +2.39% ACC on MediaEval).", "section": "performance", "field": "analysis"},
                {"sentence": "Under continual adaptation\u00a0 Online RINE improves average AUC over its baseline by +3.49% after the first round and reaches its peak by the final round with a +7.36% average AUC gain and +20.14% accuracy improvement on AIGenImages2026, while also strengthening in-the-wild robustness along the way (+3.30% AUC on Deepfake-Eval by the second round).", "section": "performance", "field": "analysis"},
                {"sentence": "Together, these results confirm that jointly leveraging in-the-wild and generator-driven data within a continual learning strategy allows the model to adapt to newly emerging generators while preserving real-world robustness and avoiding catastrophic forgetting.", "section": "performance", "field": "analysis"},
            ],
        },
        {
            "question": "What are the benchmark metrics?",
            "ground_truth": [
                {"sentence": "**AUC / ACC (%), threshold = 0.5**", "section": "performance", "field": "metrics"},
                {"sentence": "AIGenImages2026: 97.75 / 92.13\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "MNW: 95.74 / 88.59\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "Echo-4o: 88.45 / 76.80\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "Nano-Consistent: 78.35 / 71.01", "section": "performance", "field": "metrics"},
                {"sentence": "Synthbuster: 94.81 / 77.75\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "Chameleon: 89.64 / 78.58\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "DeepFake-Eval: 87.59 / 78.63\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "ITW-SM: 95.74 / 82.50\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "MediaEval:\u00a0 91.09 / 78.80", "section": "performance", "field": "metrics"},
            ],
        },
        {
            "question": "What decision thresholds are used?",
            "ground_truth": [
                {"sentence": "> Accuracy decision threshold: **0.5**\u00a0  \n> Applied at detector evaluation to compute Accuracy across all benchmarks.", "section": "performance", "field": "thresholds"},
                {"sentence": "> \u03c4\\_anchor: 0.8\u00a0  \n> Applied during fact-check retrieval to select anchor images whose VLM similarity score to extracted textual descriptions meets or exceeds this value.", "section": "performance", "field": "thresholds"},
                {"sentence": "> \u03c4\\_sim: 0.75\u00a0  \n> Applied during fact-check retrieval to expand the anchor set with candidate images whose CLIP ViT-L/14 visual similarity to an anchor image meets or exceeds this value.", "section": "performance", "field": "thresholds"},
                {"sentence": "> TopK: 500\u00a0  \n> Applied during real\u2013fake pair construction to cap the number of real images retrieved per AI-generated image.", "section": "performance", "field": "thresholds"},
                {"sentence": "> Segmentation threshold: 0.4\u00a0  \n> Applied during image segmentation with Grounding DINO Tiny to isolate visual regions and remove platform-specific overlays or UI elements.", "section": "performance", "field": "thresholds"},
            ],
        },
        {
            "question": "What is the evaluation methodology?",
            "ground_truth": [
                {"sentence": "We evaluate our detector using two complementary metrics: AUC (Area Under the ROC Curve) and ACC (Accuracy).", "section": "performance", "field": "methodology"},
                {"sentence": "AUC measures overall ranking capability independent of a fixed decision threshold, providing a threshold-agnostic view of discriminative ability.", "section": "performance", "field": "methodology"},
                {"sentence": "ACC reflects performance at a specific operating point, offering a more practical, deployment-relevant measure.", "section": "performance", "field": "methodology"},
            ],
        },
        {
            "question": "What is the energy consumption?",
            "ground_truth": [],
        },
        {
            "question": "What is the environmental impact?",
            "ground_truth": [],
        },
        {
            "question": "Was the model tested for bias?",
            "ground_truth": [
                {"sentence": "The model was not tested for bias across demographic groups.", "section": "performance", "field": "bias"},
                {"sentence": "Fairness is defined as invariance of the model's predictions to an image's semantic content, such that classification depends on generation-related forensic artifacts rather than the depicted subject or context.", "section": "safety", "field": "fairness"},
                {"sentence": "This aims to reduce implicit biases that may cause certain types of content to be systematically classified as more or less likely to be AI-generated.", "section": "safety", "field": "fairness"},
            ],
        },
    ],

    "safety": [
        {
            "question": "What are the ethical considerations?",
            "ground_truth": [
                {"sentence": "Mislabeling authentic images as AI-generated (false positives) can undermine trust in genuine visual evidence and may contribute to the dismissal of authentic documentation of real-world events.", "section": "safety", "field": "ethics"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
            ],
        },
        {
            "question": "How is fairness defined / assessed?",
            "ground_truth": [
                {"sentence": "Fairness is defined as invariance of the model's predictions to an image's semantic content, such that classification depends on generation-related forensic artifacts rather than the depicted subject or context.", "section": "safety", "field": "fairness"},
                {"sentence": "This aims to reduce implicit biases that may cause certain types of content to be systematically classified as more or less likely to be AI-generated.", "section": "safety", "field": "fairness"},
                {"sentence": "The model was not tested for bias across demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "What are the risks of this model?",
            "ground_truth": [
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Mislabeling authentic images as AI-generated (false positives) can undermine trust in genuine visual evidence and may contribute to the dismissal of authentic documentation of real-world events.", "section": "safety", "field": "ethics"},
                {"sentence": "Model performance is highly dependent on data quality, e.g., multi-cycle social media operations (repeated upload/download cycles) and heavy compression, both of which impair detection accuracy independently.", "section": "use", "field": "factors"},
            ],
        },
        {
            "question": "Is the model secure / compliant with security standards?",
            "ground_truth": [
                {"sentence": "No", "section": "safety", "field": "security"},
            ],
        },
        {
            "question": "What are the caveats of this model?",
            "ground_truth": [
                {"sentence": "Model performance is highly dependent on data quality, e.g., multi-cycle social media operations (repeated upload/download cycles) and heavy compression, both of which impair detection accuracy independently.", "section": "use", "field": "factors"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Mislabeling authentic images as AI-generated (false positives) can undermine trust in genuine visual evidence and may contribute to the dismissal of authentic documentation of real-world events.", "section": "safety", "field": "ethics"},
                {"sentence": "The model was not tested for bias across demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
    ],

    "paraphrased": [
        {
            "question": "What is the purpose of this model?",
            "ground_truth": [
                {"sentence": "The proposed framework introduces a continual adaptive pipeline for robust AI-generated image detection under evolving real-world conditions.", "section": "overview", "field": "description"},
                {"sentence": "Detecting ai-generated images", "section": "use", "field": "use_cases"},
            ],
        },
        {
            "question": "What does this model do?",
            "ground_truth": [
                {"sentence": "The proposed framework introduces a continual adaptive pipeline for robust AI-generated image detection under evolving real-world conditions.", "section": "overview", "field": "description"},
                {"sentence": "Detecting ai-generated images", "section": "use", "field": "use_cases"},
                {"sentence": "The model accepts an image as input and returns a probability score indicating whether the image is synthetic.", "section": "use", "field": "inputs_outputs"},
                {"sentence": "It also identifies the top ten image patches that most influenced the decision, providing bounding boxes and probability scores for each.", "section": "use", "field": "inputs_outputs"},
            ],
        },
        {
            "question": "Which organization built this model?",
            "ground_truth": [
                {"sentence": "CERTH - The Centre for Research & Technology, Hellas", "section": "overview", "field": "creator"},
            ],
        },
        {
            "question": "When did this model come out?",
            "ground_truth": [
                {"sentence": "2026-05-01", "section": "overview", "field": "date"},
            ],
        },
        {
            "question": "What kind of architecture is used?",
            "ground_truth": [
                {"sentence": "Transformer", "section": "overview", "field": "type"},
            ],
        },
        {
            "question": "What is the size of the model?",
            "ground_truth": [],
        },
        {
            "question": "Where do I download it from?",
            "ground_truth": [
                {"sentence": "[https://github.com/mever-team/WildFC](https://github.com/mever-team/WildFC)", "section": "overview", "field": "home"},
                {"sentence": "Detailed software implementation is available at: [https://github.com/mever-team/WildFC/](https://github.com/mever-team/WildFC/).", "section": "use", "field": "software"},
            ],
        },
        {
            "question": "Who should I email about it?",
            "ground_truth": [
                {"sentence": "Thanasis Pantsios: [apantsios@iti.gr](mailto:apantsios@iti.gr)", "section": "overview", "field": "contact"},
            ],
        },
        {
            "question": "What Python packages do I need?",
            "ground_truth": [
                {"sentence": "Detailed software implementation is available at: [https://github.com/mever-team/WildFC/](https://github.com/mever-team/WildFC/).", "section": "use", "field": "software"},
            ],
        },
        {
            "question": "What GPU do I need to run it?",
            "ground_truth": [
                {"sentence": "Running the model requires a GPU with at least 4 GB of VRAM.", "section": "use", "field": "hardware"},
            ],
        },
        {
            "question": "What does the model take as input, and what does it return?",
            "ground_truth": [
                {"sentence": "The model accepts an image as input and returns a probability score indicating whether the image is synthetic.", "section": "use", "field": "inputs_outputs"},
                {"sentence": "It also identifies the top ten image patches that most influenced the decision, providing bounding boxes and probability scores for each.", "section": "use", "field": "inputs_outputs"},
            ],
        },
        {
            "question": "How do I load and run the model on data?",
            "ground_truth": [
                {"sentence": "Detailed usage instructions are available at: [https://github.com/mever-team/WildFC/](https://github.com/mever-team/WildFC/)", "section": "use", "field": "instructions"},
                {"sentence": "The model accepts an image as input and returns a probability score indicating whether the image is synthetic.", "section": "use", "field": "inputs_outputs"},
                {"sentence": "It also identifies the top ten image patches that most influenced the decision, providing bounding boxes and probability scores for each.", "section": "use", "field": "inputs_outputs"},
                {"sentence": "Running the model requires a GPU with at least 4 GB of VRAM.", "section": "use", "field": "hardware"},
            ],
        },
        {
            "question": "What could make its performance worse?",
            "ground_truth": [
                {"sentence": "Model performance is highly dependent on data quality, e.g., multi-cycle social media operations (repeated upload/download cycles) and heavy compression, both of which impair detection accuracy independently.", "section": "use", "field": "factors"},
            ],
        },
        {
            "question": "What should this model not be used for?",
            "ground_truth": [
                {"sentence": "Treating the probability score as a final verdict rather than a helpful indicator, or relying on it for unsupervised decision-making without human review.", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "Who is this model for?",
            "ground_truth": [
                {"sentence": "Journalists, Fact-checkers, Researchers,\u00a0General public", "section": "use", "field": "user_groups"},
            ],
        },
        {
            "question": "Does a human need to review the outputs?",
            "ground_truth": [
                {"sentence": "human-in-the-loop", "section": "use", "field": "oversight"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Treating the probability score as a final verdict rather than a helpful indicator, or relying on it for unsupervised decision-making without human review.", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "What does it say about its accuracy?",
            "ground_truth": [
                {"sentence": "Online RINE raises average performance by +8.01% accuracy across both recent-generator and in-the-wild benchmarks combined, with particularly strong gains on previously challenging recent generators such as Echo-4o (48.75% \u2192 76.80% accuracy) and Nano-Consistent (63.81% \u2192 71.01% accuracy), while also improving in-the-wild robustness(+1.01% ACC on ITW-SM, +2.39% ACC on MediaEval).", "section": "performance", "field": "analysis"},
                {"sentence": "Under continual adaptation\u00a0 Online RINE improves average AUC over its baseline by +3.49% after the first round and reaches its peak by the final round with a +7.36% average AUC gain and +20.14% accuracy improvement on AIGenImages2026, while also strengthening in-the-wild robustness along the way (+3.30% AUC on Deepfake-Eval by the second round).", "section": "performance", "field": "analysis"},
                {"sentence": "AIGenImages2026: 97.75 / 92.13\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "MNW: 95.74 / 88.59\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "Echo-4o: 88.45 / 76.80\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "Nano-Consistent: 78.35 / 71.01", "section": "performance", "field": "metrics"},
                {"sentence": "Synthbuster: 94.81 / 77.75\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "Chameleon: 89.64 / 78.58\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "DeepFake-Eval: 87.59 / 78.63\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "ITW-SM: 95.74 / 82.50\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "MediaEval:\u00a0 91.09 / 78.80", "section": "performance", "field": "metrics"},
            ],
        },
        {
            "question": "What threshold is used to make predictions?",
            "ground_truth": [
                {"sentence": "> Accuracy decision threshold: **0.5**\u00a0  \n> Applied at detector evaluation to compute Accuracy across all benchmarks.", "section": "performance", "field": "thresholds"},
            ],
        },
        {
            "question": "What could go wrong if I use this model?",
            "ground_truth": [
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Mislabeling authentic images as AI-generated (false positives) can undermine trust in genuine visual evidence and may contribute to the dismissal of authentic documentation of real-world events.", "section": "safety", "field": "ethics"},
                {"sentence": "Model performance is highly dependent on data quality, e.g., multi-cycle social media operations (repeated upload/download cycles) and heavy compression, both of which impair detection accuracy independently.", "section": "use", "field": "factors"},
            ],
        },
        {
            "question": "Are there ethical concerns with using this?",
            "ground_truth": [
                {"sentence": "Mislabeling authentic images as AI-generated (false positives) can undermine trust in genuine visual evidence and may contribute to the dismissal of authentic documentation of real-world events.", "section": "safety", "field": "ethics"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
            ],
        },
        {
            "question": "How much energy does it consume?",
            "ground_truth": [],
        },
        {
            "question": "Is it compliant with any security standard?",
            "ground_truth": [
                {"sentence": "No", "section": "safety", "field": "security"},
            ],
        },
        {
            "question": "Is the model fair across subgroups?",
            "ground_truth": [
                {"sentence": "Fairness is defined as invariance of the model's predictions to an image's semantic content, such that classification depends on generation-related forensic artifacts rather than the depicted subject or context.", "section": "safety", "field": "fairness"},
                {"sentence": "This aims to reduce implicit biases that may cause certain types of content to be systematically classified as more or less likely to be AI-generated.", "section": "safety", "field": "fairness"},
                {"sentence": "The model was not tested for bias across demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "What are its known limitations?",
            "ground_truth": [
                {"sentence": "Model performance is highly dependent on data quality, e.g., multi-cycle social media operations (repeated upload/download cycles) and heavy compression, both of which impair detection accuracy independently.", "section": "use", "field": "factors"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Mislabeling authentic images as AI-generated (false positives) can undermine trust in genuine visual evidence and may contribute to the dismissal of authentic documentation of real-world events.", "section": "safety", "field": "ethics"},
                {"sentence": "The model was not tested for bias across demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "What datasets was it trained and evaluated on?",
            "ground_truth": [
                {"sentence": "[WildFC](https://huggingface.co/datasets/pthan12/WildFC) ,\u00a0[AIGenImages2026](https://huggingface.co/datasets/pthan12/AIGenImages2026),\u00a0[Twigma](https://yiqunchen.github.io/TWIGMA/),\u00a0[LDM](https://github.com/grip-unina/DMimageDetection),\u00a0[COCO]((https://cocodataset.org/)),\u00a0[LSUN](https://arxiv.org/abs/1506.03365), [OpenImages]((https://storage.googleapis.com/openimages/web/index.html) datasets", "section": "training", "field": "datasets"},
                {"sentence": "WildFC is an evolving in-the-wild dataset collected through an automated fact-check retrieval pipeline.", "section": "evaluation", "field": "datasets"},
                {"sentence": "The evaluation datasets were chosen to cover both sources of distribution shift identified as driving AID's non-stationary nature: shift from the continuous development of recent generative models (AIGenImages2026, MNW, Synthbuster, Nano-Consistent, and Echo-4o), and shift arising from real-world usage dynamics and platform-specific processing (Chameleon, ITW-SM, MediaEval-ITW, and Deepfake-Eval).", "section": "evaluation", "field": "motivation"},
            ],
        },
        {
            "question": "How was the model evaluated?",
            "ground_truth": [
                {"sentence": "We evaluate our detector using two complementary metrics: AUC (Area Under the ROC Curve) and ACC (Accuracy).", "section": "performance", "field": "methodology"},
                {"sentence": "AUC measures overall ranking capability independent of a fixed decision threshold, providing a threshold-agnostic view of discriminative ability.", "section": "performance", "field": "methodology"},
                {"sentence": "ACC reflects performance at a specific operating point, offering a more practical, deployment-relevant measure.", "section": "performance", "field": "methodology"},
                {"sentence": "> Accuracy decision threshold: **0.5**\u00a0  \n> Applied at detector evaluation to compute Accuracy across all benchmarks.", "section": "performance", "field": "thresholds"},
            ],
        },
        {
            "question": "What standards does it follow?",
            "ground_truth": [
                {"sentence": "IEEE", "section": "training", "field": "standards"},
                {"sentence": "IEEE", "section": "evaluation", "field": "standards"},
            ],
        },
    ],

    "cross_field": [
        {
            "question": "Who created this model and what kind of model is it?",
            "ground_truth": [
                {"sentence": "CERTH - The Centre for Research & Technology, Hellas", "section": "overview", "field": "creator"},
                {"sentence": "Transformer", "section": "overview", "field": "type"},
            ],
        },
        {
            "question": "What is the model's task and its intended use?",
            "ground_truth": [
                {"sentence": "Image Classification", "section": "overview", "field": "task"},
                {"sentence": "The proposed framework introduces a continual adaptive pipeline for robust AI-generated image detection under evolving real-world conditions.", "section": "overview", "field": "description"},
                {"sentence": "Detecting ai-generated images", "section": "use", "field": "use_cases"},
            ],
        },
        {
            "question": "When was the model released and what version is it?",
            "ground_truth": [
                {"sentence": "2026-05-01", "section": "overview", "field": "date"},
                {"sentence": "1.0", "section": "overview", "field": "version"},
            ],
        },
        {
            "question": "What hardware and software do I need to run this model?",
            "ground_truth": [
                {"sentence": "Running the model requires a GPU with at least 4 GB of VRAM.", "section": "use", "field": "hardware"},
                {"sentence": "Detailed software implementation is available at: [https://github.com/mever-team/WildFC/](https://github.com/mever-team/WildFC/).", "section": "use", "field": "software"},
            ],
        },
        {
            "question": "What are the risks and ethical concerns of using this model?",
            "ground_truth": [
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Mislabeling authentic images as AI-generated (false positives) can undermine trust in genuine visual evidence and may contribute to the dismissal of authentic documentation of real-world events.", "section": "safety", "field": "ethics"},
            ],
        },
        {
            "question": "What is the energy consumption and environmental impact?",
            "ground_truth": [],
        },
        {
            "question": "Who are the intended users and what oversight is required?",
            "ground_truth": [
                {"sentence": "Journalists, Fact-checkers, Researchers,\u00a0General public", "section": "use", "field": "user_groups"},
                {"sentence": "human-in-the-loop", "section": "use", "field": "oversight"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
            ],
        },
        {
            "question": "What are the caveats and out-of-scope uses?",
            "ground_truth": [
                {"sentence": "Model performance is highly dependent on data quality, e.g., multi-cycle social media operations (repeated upload/download cycles) and heavy compression, both of which impair detection accuracy independently.", "section": "use", "field": "factors"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Mislabeling authentic images as AI-generated (false positives) can undermine trust in genuine visual evidence and may contribute to the dismissal of authentic documentation of real-world events.", "section": "safety", "field": "ethics"},
                {"sentence": "The model was not tested for bias across demographic groups.", "section": "performance", "field": "bias"},
                {"sentence": "Treating the probability score as a final verdict rather than a helpful indicator, or relying on it for unsupervised decision-making without human review.", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "How was the model trained and evaluated?",
            "ground_truth": [
                {"sentence": "[WildFC](https://huggingface.co/datasets/pthan12/WildFC) ,\u00a0[AIGenImages2026](https://huggingface.co/datasets/pthan12/AIGenImages2026),\u00a0[Twigma](https://yiqunchen.github.io/TWIGMA/),\u00a0[LDM](https://github.com/grip-unina/DMimageDetection),\u00a0[COCO]((https://cocodataset.org/)),\u00a0[LSUN](https://arxiv.org/abs/1506.03365), [OpenImages]((https://storage.googleapis.com/openimages/web/index.html) datasets", "section": "training", "field": "datasets"},
                {"sentence": "The training data combines in-the-wild images with outputs from recent diffusion models along with real images from recent datasets.", "section": "training", "field": "motivation"},
                {"sentence": "This selection ensures the model remains adaptive by\u00a0 learning modern generative artifacts while building resilience against real-world media degradations.", "section": "training", "field": "motivation"},
                {"sentence": "Gaussian blurring and JPEG compression with probability 0.5,\u00a0TextureCrop\u00a0for a 224x224 crop, random horizontal flip with probability 0.5.", "section": "training", "field": "preprocessing"},
                {"sentence": "WildFC is an evolving in-the-wild dataset collected through an automated fact-check retrieval pipeline.", "section": "evaluation", "field": "datasets"},
                {"sentence": "The evaluation datasets were chosen to cover both sources of distribution shift identified as driving AID's non-stationary nature: shift from the continuous development of recent generative models (AIGenImages2026, MNW, Synthbuster, Nano-Consistent, and Echo-4o), and shift arising from real-world usage dynamics and platform-specific processing (Chameleon, ITW-SM, MediaEval-ITW, and Deepfake-Eval).", "section": "evaluation", "field": "motivation"},
                {"sentence": "The validation and test images are center-cropped at 224×224.", "section": "evaluation", "field": "preprocessing"},
                {"sentence": "We evaluate our detector using two complementary metrics: AUC (Area Under the ROC Curve) and ACC (Accuracy).", "section": "performance", "field": "methodology"},
                {"sentence": "AUC measures overall ranking capability independent of a fixed decision threshold, providing a threshold-agnostic view of discriminative ability.", "section": "performance", "field": "methodology"},
                {"sentence": "ACC reflects performance at a specific operating point, offering a more practical, deployment-relevant measure.", "section": "performance", "field": "methodology"},
            ],
        },
        {
            "question": "What are the input/output formats, and how do I run the model?",
            "ground_truth": [
                {"sentence": "The model accepts an image as input and returns a probability score indicating whether the image is synthetic.", "section": "use", "field": "inputs_outputs"},
                {"sentence": "It also identifies the top ten image patches that most influenced the decision, providing bounding boxes and probability scores for each.", "section": "use", "field": "inputs_outputs"},
                {"sentence": "Detailed usage instructions are available at: [https://github.com/mever-team/WildFC/](https://github.com/mever-team/WildFC/)", "section": "use", "field": "instructions"},
                {"sentence": "Running the model requires a GPU with at least 4 GB of VRAM.", "section": "use", "field": "hardware"},
                {"sentence": "Detailed software implementation is available at: [https://github.com/mever-team/WildFC/](https://github.com/mever-team/WildFC/).", "section": "use", "field": "software"},
            ],
        },
        {
            "question": "What technical or ethical standards does the model follow?",
            "ground_truth": [
                {"sentence": "IEEE", "section": "training", "field": "standards"},
                {"sentence": "IEEE", "section": "evaluation", "field": "standards"},
                {"sentence": "Mislabeling authentic images as AI-generated (false positives) can undermine trust in genuine visual evidence and may contribute to the dismissal of authentic documentation of real-world events.", "section": "safety", "field": "ethics"},
            ],
        },
        {
            "question": "What factors could degrade performance, and what are the known caveats?",
            "ground_truth": [
                {"sentence": "Model performance is highly dependent on data quality, e.g., multi-cycle social media operations (repeated upload/download cycles) and heavy compression, both of which impair detection accuracy independently.", "section": "use", "field": "factors"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Mislabeling authentic images as AI-generated (false positives) can undermine trust in genuine visual evidence and may contribute to the dismissal of authentic documentation of real-world events.", "section": "safety", "field": "ethics"},
                {"sentence": "The model was not tested for bias across demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "How do I install the software, and what hardware does it need?",
            "ground_truth": [
                {"sentence": "Detailed software implementation is available at: [https://github.com/mever-team/WildFC/](https://github.com/mever-team/WildFC/).", "section": "use", "field": "software"},
                {"sentence": "Detailed usage instructions are available at: [https://github.com/mever-team/WildFC/](https://github.com/mever-team/WildFC/)", "section": "use", "field": "instructions"},
                {"sentence": "Running the model requires a GPU with at least 4 GB of VRAM.", "section": "use", "field": "hardware"},
            ],
        },
        {
            "question": "Who should use this model, and what should they not do with it?",
            "ground_truth": [
                {"sentence": "Journalists, Fact-checkers, Researchers,\u00a0General public", "section": "use", "field": "user_groups"},
                {"sentence": "Detecting ai-generated images", "section": "use", "field": "use_cases"},
                {"sentence": "Treating the probability score as a final verdict rather than a helpful indicator, or relying on it for unsupervised decision-making without human review.", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "What is the model's license and how do I cite it?",
            "ground_truth": [
                {"sentence": "Apache License 2.0", "section": "overview", "field": "license"},
                {"sentence": "@inproceedings{pantsios2026automated,\n\ntitle={Automated In-the-Wild Data Collection for Continual AI Generated Image Detection},\n\nauthor={Pantsios, Athanasios and Karageorgiou, Dimitrios and Koutlis, Christos and Karantaidis, George and Papadopoulou, Olga and Papadopoulos, Symeon},\n\nbooktitle={The 5th ACM International Workshop on Multimedia AI against Disinformation (MAD '26)},\n\nyear={2026},\n\ndoi={10.1145/3810988.3812662}\n\n}", "section": "overview", "field": "citation"},
            ],
        },
    ],

    "negative": [
        {
            "question": "What is the CO₂ emissions footprint of training?",
            "ground_truth": [],
        },
        {
            "question": "What is the training compute in FLOPs?",
            "ground_truth": [],
        },
        {
            "question": "How many individual samples were in the training dataset?",
            "ground_truth": [],
        },
        {
            "question": "What demographic groups were used for bias evaluation?",
            "ground_truth": [
                {"sentence": "The model was not tested for bias across demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "What is the model's robustness to adversarial attacks?",
            "ground_truth": [],
        },
        {
            "question": "What is the model's water usage?",
            "ground_truth": [],
        },
        {
            "question": "Who are the individual authors (not the institution)?",
            "ground_truth": [
                {"sentence": "Thanasis Pantsios: [apantsios@iti.gr](mailto:apantsios@iti.gr)", "section": "overview", "field": "contact"},
                {"sentence": "@inproceedings{pantsios2026automated,\n\ntitle={Automated In-the-Wild Data Collection for Continual AI Generated Image Detection},\n\nauthor={Pantsios, Athanasios and Karageorgiou, Dimitrios and Koutlis, Christos and Karantaidis, George and Papadopoulou, Olga and Papadopoulos, Symeon},\n\nbooktitle={The 5th ACM International Workshop on Multimedia AI against Disinformation (MAD '26)},\n\nyear={2026},\n\ndoi={10.1145/3810988.3812662}\n\n}", "section": "overview", "field": "citation"},
            ],
        },
        {
            "question": "Can you provide the citation in BibTeX format?",
            "ground_truth": [
                {"sentence": "@inproceedings{pantsios2026automated,\n\ntitle={Automated In-the-Wild Data Collection for Continual AI Generated Image Detection},\n\nauthor={Pantsios, Athanasios and Karageorgiou, Dimitrios and Koutlis, Christos and Karantaidis, George and Papadopoulou, Olga and Papadopoulos, Symeon},\n\nbooktitle={The 5th ACM International Workshop on Multimedia AI against Disinformation (MAD '26)},\n\nyear={2026},\n\ndoi={10.1145/3810988.3812662}\n\n}", "section": "overview", "field": "citation"},
            ],
        },
        {
            "question": "What is the inference latency per request?",
            "ground_truth": [],
        },
        {
            "question": "What is the model file size on disk?",
            "ground_truth": [],
        },
        {
            "question": "What data privacy measures are in place?",
            "ground_truth": [],
        },
        {
            "question": "Is the model explainable / interpretable?",
            "ground_truth": [
                {"sentence": "It also identifies the top ten image patches that most influenced the decision, providing bounding boxes and probability scores for each.", "section": "use", "field": "inputs_outputs"},
            ],
        },
        {
            "question": "Does the model handle audio / video modalities (if not applicable)?",
            "ground_truth": [
                {"sentence": "The model accepts an image as input and returns a probability score indicating whether the image is synthetic.", "section": "use", "field": "inputs_outputs"},
            ],
        },
        {
            "question": "What is the model's update / changelog history?",
            "ground_truth": [],
        },
        {
            "question": "Is there any additional information not covered elsewhere on this card?",
            "ground_truth": [],
        },
    ],

    "ambiguous": [
        {
            "question": "Is this model safe?",
            "ground_truth": [
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Mislabeling authentic images as AI-generated (false positives) can undermine trust in genuine visual evidence and may contribute to the dismissal of authentic documentation of real-world events.", "section": "safety", "field": "ethics"},
                {"sentence": "No", "section": "safety", "field": "security"},
                {"sentence": "Model performance is highly dependent on data quality, e.g., multi-cycle social media operations (repeated upload/download cycles) and heavy compression, both of which impair detection accuracy independently.", "section": "use", "field": "factors"},
                {"sentence": "The model was not tested for bias across demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "What are the limitations of this model?",
            "ground_truth": [
                {"sentence": "Model performance is highly dependent on data quality, e.g., multi-cycle social media operations (repeated upload/download cycles) and heavy compression, both of which impair detection accuracy independently.", "section": "use", "field": "factors"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Mislabeling authentic images as AI-generated (false positives) can undermine trust in genuine visual evidence and may contribute to the dismissal of authentic documentation of real-world events.", "section": "safety", "field": "ethics"},
                {"sentence": "The model was not tested for bias across demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "Is this model accurate?",
            "ground_truth": [
                {"sentence": "Online RINE raises average performance by +8.01% accuracy across both recent-generator and in-the-wild benchmarks combined, with particularly strong gains on previously challenging recent generators such as Echo-4o (48.75% \u2192 76.80% accuracy) and Nano-Consistent (63.81% \u2192 71.01% accuracy), while also improving in-the-wild robustness(+1.01% ACC on ITW-SM, +2.39% ACC on MediaEval).", "section": "performance", "field": "analysis"},
                {"sentence": "AIGenImages2026: 97.75 / 92.13\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "MNW: 95.74 / 88.59\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "Echo-4o: 88.45 / 76.80\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "Nano-Consistent: 78.35 / 71.01", "section": "performance", "field": "metrics"},
                {"sentence": "Synthbuster: 94.81 / 77.75\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "Chameleon: 89.64 / 78.58\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "DeepFake-Eval: 87.59 / 78.63\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "ITW-SM: 95.74 / 82.50\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "MediaEval:\u00a0 91.09 / 78.80", "section": "performance", "field": "metrics"},
            ],
        },
        {
            "question": "Is this model good?",
            "ground_truth": [
                {"sentence": "Online RINE raises average performance by +8.01% accuracy across both recent-generator and in-the-wild benchmarks combined, with particularly strong gains on previously challenging recent generators such as Echo-4o (48.75% \u2192 76.80% accuracy) and Nano-Consistent (63.81% \u2192 71.01% accuracy), while also improving in-the-wild robustness(+1.01% ACC on ITW-SM, +2.39% ACC on MediaEval).", "section": "performance", "field": "analysis"},
                {"sentence": "Under continual adaptation\u00a0 Online RINE improves average AUC over its baseline by +3.49% after the first round and reaches its peak by the final round with a +7.36% average AUC gain and +20.14% accuracy improvement on AIGenImages2026, while also strengthening in-the-wild robustness along the way (+3.30% AUC on Deepfake-Eval by the second round).", "section": "performance", "field": "analysis"},
                {"sentence": "Together, these results confirm that jointly leveraging in-the-wild and generator-driven data within a continual learning strategy allows the model to adapt to newly emerging generators while preserving real-world robustness and avoiding catastrophic forgetting.", "section": "performance", "field": "analysis"},
            ],
        },
        {
            "question": "How does this model work?",
            "ground_truth": [
                {"sentence": "The proposed framework introduces a continual adaptive pipeline for robust AI-generated image detection under evolving real-world conditions.", "section": "overview", "field": "description"},
                {"sentence": "The model accepts an image as input and returns a probability score indicating whether the image is synthetic.", "section": "use", "field": "inputs_outputs"},
                {"sentence": "It also identifies the top ten image patches that most influenced the decision, providing bounding boxes and probability scores for each.", "section": "use", "field": "inputs_outputs"},
                {"sentence": "The training data combines in-the-wild images with outputs from recent diffusion models along with real images from recent datasets.", "section": "training", "field": "motivation"},
                {"sentence": "This selection ensures the model remains adaptive by\u00a0 learning modern generative artifacts while building resilience against real-world media degradations.", "section": "training", "field": "motivation"},
            ],
        },
        {
            "question": "Is this model trustworthy?",
            "ground_truth": [
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Mislabeling authentic images as AI-generated (false positives) can undermine trust in genuine visual evidence and may contribute to the dismissal of authentic documentation of real-world events.", "section": "safety", "field": "ethics"},
                {"sentence": "No", "section": "safety", "field": "security"},
                {"sentence": "Model performance is highly dependent on data quality, e.g., multi-cycle social media operations (repeated upload/download cycles) and heavy compression, both of which impair detection accuracy independently.", "section": "use", "field": "factors"},
                {"sentence": "The model was not tested for bias across demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "What is this model's main contribution?",
            "ground_truth": [
                {"sentence": "The proposed framework introduces a continual adaptive pipeline for robust AI-generated image detection under evolving real-world conditions.", "section": "overview", "field": "description"},
                {"sentence": "Together, these results confirm that jointly leveraging in-the-wild and generator-driven data within a continual learning strategy allows the model to adapt to newly emerging generators while preserving real-world robustness and avoiding catastrophic forgetting.", "section": "performance", "field": "analysis"},
            ],
        },
        {
            "question": "Is this model reliable?",
            "ground_truth": [
                {"sentence": "Model performance is highly dependent on data quality, e.g., multi-cycle social media operations (repeated upload/download cycles) and heavy compression, both of which impair detection accuracy independently.", "section": "use", "field": "factors"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Mislabeling authentic images as AI-generated (false positives) can undermine trust in genuine visual evidence and may contribute to the dismissal of authentic documentation of real-world events.", "section": "safety", "field": "ethics"},
                {"sentence": "The model was not tested for bias across demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "What makes this model novel?",
            "ground_truth": [
                {"sentence": "The proposed framework introduces a continual adaptive pipeline for robust AI-generated image detection under evolving real-world conditions.", "section": "overview", "field": "description"},
                {"sentence": "Together, these results confirm that jointly leveraging in-the-wild and generator-driven data within a continual learning strategy allows the model to adapt to newly emerging generators while preserving real-world robustness and avoiding catastrophic forgetting.", "section": "performance", "field": "analysis"},
            ],
        },
        {
            "question": "Is this model ready for production?",
            "ground_truth": [
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Model performance is highly dependent on data quality, e.g., multi-cycle social media operations (repeated upload/download cycles) and heavy compression, both of which impair detection accuracy independently.", "section": "use", "field": "factors"},
                {"sentence": "The model was not tested for bias across demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "Is this model eco-friendly?",
            "ground_truth": [],
        },
        {
            "question": "How do I use this model?",
            "ground_truth": [
                {"sentence": "Detailed usage instructions are available at: [https://github.com/mever-team/WildFC/](https://github.com/mever-team/WildFC/)", "section": "use", "field": "instructions"},
                {"sentence": "The model accepts an image as input and returns a probability score indicating whether the image is synthetic.", "section": "use", "field": "inputs_outputs"},
                {"sentence": "It also identifies the top ten image patches that most influenced the decision, providing bounding boxes and probability scores for each.", "section": "use", "field": "inputs_outputs"},
                {"sentence": "Running the model requires a GPU with at least 4 GB of VRAM.", "section": "use", "field": "hardware"},
                {"sentence": "Detailed software implementation is available at: [https://github.com/mever-team/WildFC/](https://github.com/mever-team/WildFC/).", "section": "use", "field": "software"},
            ],
        },
        {
            "question": "What should I know before using this model?",
            "ground_truth": [
                {"sentence": "Model performance is highly dependent on data quality, e.g., multi-cycle social media operations (repeated upload/download cycles) and heavy compression, both of which impair detection accuracy independently.", "section": "use", "field": "factors"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Mislabeling authentic images as AI-generated (false positives) can undermine trust in genuine visual evidence and may contribute to the dismissal of authentic documentation of real-world events.", "section": "safety", "field": "ethics"},
                {"sentence": "The model was not tested for bias across demographic groups.", "section": "performance", "field": "bias"},
                {"sentence": "Treating the probability score as a final verdict rather than a helpful indicator, or relying on it for unsupervised decision-making without human review.", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "Can I use this model commercially?",
            "ground_truth": [
                {"sentence": "Apache License 2.0", "section": "overview", "field": "license"},
            ],
        },
        {
            "question": "What are the main takeaways about this model?",
            "ground_truth": [
                {"sentence": "The proposed framework introduces a continual adaptive pipeline for robust AI-generated image detection under evolving real-world conditions.", "section": "overview", "field": "description"},
                {"sentence": "Online RINE raises average performance by +8.01% accuracy across both recent-generator and in-the-wild benchmarks combined, with particularly strong gains on previously challenging recent generators such as Echo-4o (48.75% \u2192 76.80% accuracy) and Nano-Consistent (63.81% \u2192 71.01% accuracy), while also improving in-the-wild robustness(+1.01% ACC on ITW-SM, +2.39% ACC on MediaEval).", "section": "performance", "field": "analysis"},
                {"sentence": "Under continual adaptation\u00a0 Online RINE improves average AUC over its baseline by +3.49% after the first round and reaches its peak by the final round with a +7.36% average AUC gain and +20.14% accuracy improvement on AIGenImages2026, while also strengthening in-the-wild robustness along the way (+3.30% AUC on Deepfake-Eval by the second round).", "section": "performance", "field": "analysis"},
                {"sentence": "Together, these results confirm that jointly leveraging in-the-wild and generator-driven data within a continual learning strategy allows the model to adapt to newly emerging generators while preserving real-world robustness and avoiding catastrophic forgetting.", "section": "performance", "field": "analysis"},
            ],
        },
    ],
}