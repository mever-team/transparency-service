GROUND_TRUTH = {
    "overview": [
        {
            "question": "What is the name of this model?",
            "target_fields": ["overview.name"],
            "ground_truth": [
                {"sentence": "TrAI-Import", "section": "overview", "field": "name"},
            ],
        },
        {
            "question": "What is this model used for?",
            "target_fields": ["use.use_cases"],
            "ground_truth": [
                {"sentence": "This operation enables the automated retrieval of information from a specified URL and the autocompletion of model card fields.", "section": "overview", "field": "description"},
                {"sentence": "Import external information into a model card", "section": "use", "field": "use_cases"},
            ],
        },
        {
            "question": "Who created this model?",
            "target_fields": ["overview.creator"],
            "ground_truth": [
                {"sentence": "CERTH - The Centre for Research & Technology, Hellas", "section": "overview", "field": "creator"},
            ],
        },
        {
            "question": "When was this model released?",
            "target_fields": ["overview.date"],
            "ground_truth": [
                {"sentence": "2025-11-11", "section": "overview", "field": "date"},
            ],
        },
        {
            "question": "What version is this model?",
            "target_fields": ["overview.version"],
            "ground_truth": [
                {"sentence": "1.0", "section": "overview", "field": "version"},
            ],
        },
        {
            "question": "What is the type of the model?",
            "target_fields": ["overview.type"],
            "ground_truth": [
                {"sentence": "Transformer", "section": "overview", "field": "type"},
                {"sentence": "This function is powered by the BGE model.", "section": "overview", "field": "description"},
            ],
        },
        {
            # FLAG: GT sentence is tagged performance.analysis, not overview.parameters.
            "question": "How many parameters does this model have?",
            "target_fields": ["performance.analysis"],
            "ground_truth": [
                {"sentence": "The model is highly efficient, using 33 million parameters to produce 384-dimension vectors at 130MB runtime memory", "section": "performance", "field": "analysis"},
            ],
        },
        {
            "question": "What is the task of this model?",
            "target_fields": ["overview.task"],
            "ground_truth": [
                {"sentence": "Model Card Auto-Fill", "section": "overview", "field": "task"},
                {"sentence": "This operation enables the automated retrieval of information from a specified URL and the autocompletion of model card fields.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "What is the license of this model?",
            "target_fields": ["overview.license"],
            "ground_truth": [
                {"sentence": "TBD", "section": "overview", "field": "license"},
            ],
        },
        {
            "question": "Where can I find this model?",
            "target_fields": ["overview.home"],
            "ground_truth": [
                {"sentence": "[https://trai.mever.gr](https://trai.mever.gr/)", "section": "overview", "field": "home"},
            ],
        },
        {
            "question": "Who can I contact about this model?",
            "target_fields": ["overview.contact"],
            "ground_truth": [
                {"sentence": "[gnikoul@iti.gr](mailto:gnikoul@iti.gr),\u00a0[maniospas@iti.gr](mailto:maniospas@iti.gr),\u00a0[laaposto@iti.gr](mailto:laaposto@iti.gr)", "section": "overview", "field": "contact"},
            ],
        },
        {
            "question": "How should I cite this model?",
            "target_fields": ["overview.citation"],
            "ground_truth": [
                {"sentence": "Use this model card as a citation", "section": "overview", "field": "citation"},
            ],
        },
    ],

    "use": [
        {
            "question": "What are the intended use cases?",
            "target_fields": ["use.use_cases"],
            "ground_truth": [
                {"sentence": "Import external information into a model card", "section": "use", "field": "use_cases"},
                {"sentence": "This operation enables the automated retrieval of information from a specified URL and the autocompletion of model card fields.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "What level of human oversight is required?",
            "target_fields": ["use.oversight"],
            "ground_truth": [
                {"sentence": "human-on-the-loop", "section": "use", "field": "oversight"},
                {"sentence": "Users should review all auto\u2011populated fields before publication.", "section": "safety", "field": "ethics"},
            ],
        },
        {
            "question": "Who are the intended user groups?",
            "target_fields": ["use.user_groups"],
            "ground_truth": [
                {"sentence": "Model card creators", "section": "use", "field": "user_groups"},
            ],
        },
        {
            "question": "What is this model not intended for?",
            "target_fields": ["use.out_of_scope_use"],
            "ground_truth": [
                {"sentence": "Do not use unrelated sources to import information", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "What software does this model require?",
            "target_fields": ["use.software"],
            "ground_truth": [
                {"sentence": "Python, transformers", "section": "use", "field": "software"},
            ],
        },
        {
            "question": "How do I run / use this model?",
            "target_fields": ["use.instructions"],
            "ground_truth": [
                {"sentence": "You can use this operation from any model card by navigating to the **Actions -> Import**\u00a0at the top right corner of the screen.", "section": "use", "field": "instructions"},
                {"sentence": "You can also find more information in our [handbook](https://trai.mever.gr/transparency/handbook.html).", "section": "use", "field": "instructions"},
                {"sentence": "Input: URL -> Output: model card", "section": "use", "field": "inputs_outputs"},
                {"sentence": "Python, transformers", "section": "use", "field": "software"},
            ],
        },
        {
            "question": "What are the inputs and outputs of the model?",
            "target_fields": ["use.inputs_outputs"],
            "ground_truth": [
                {"sentence": "Input: URL -> Output: model card", "section": "use", "field": "inputs_outputs"},
                {"sentence": "This operation enables the automated retrieval of information from a specified URL and the autocompletion of model card fields.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "What factors affect the model's performance?",
            "target_fields": ["use.factors"],
            "ground_truth": [
                {"sentence": "The quality of the output directly depends on the quality of the information withing the provided URL.", "section": "use", "field": "factors"},
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
            ],
        },
        {
            "question": "What hardware is required?",
            "target_fields": ["use.hardware"],
            "ground_truth": [
                {"sentence": "The model runs on an Intel Xeon CPU E5-2620 0 @ 2.00GHz", "section": "use", "field": "hardware"},
            ],
        },
    ],

    "training": [
        {
            "question": "What datasets were used for training?",
            "target_fields": ["training.datasets"],
            "ground_truth": [
                {"sentence": "The system uses the [bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)\u00a0base model.", "section": "training", "field": "datasets"},
                {"sentence": "No fine tuning was made.", "section": "training", "field": "datasets"},
                {"sentence": "This function is powered by the BGE model.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "Why were these training datasets chosen?",
            "target_fields": ["training.motivation"],
            "ground_truth": [
                {"sentence": "N/A", "section": "training", "field": "motivation"},
            ],
        },
        {
            "question": "What preprocessing was applied during training?",
            "target_fields": ["training.preprocessing"],
            "ground_truth": [
                {"sentence": "N/A", "section": "training", "field": "preprocessing"},
            ],
        },
        {
            "question": "What standards were followed during training?",
            "target_fields": ["training.standards"],
            "ground_truth": [
                {"sentence": "N/A", "section": "training", "field": "standards"},
            ],
        },
        {
            "question": "Is the training data up to date?",
            "target_fields": ["training.update"],
            "ground_truth": [
                {"sentence": "N/A", "section": "training", "field": "update"},
            ],
        },
    ],

    "evaluation": [
        {
            "question": "What datasets were used for evaluation?",
            "target_fields": ["evaluation.datasets"],
            "ground_truth": [
                {"sentence": "FlagEmbedding models are evaluated on a comprehensive suite of established information retrieval and text embedding benchmarks.", "section": "evaluation", "field": "datasets"},
                {"sentence": "These include MTEB (Massive Text Embedding Benchmark) for English tasks and C-MTEB for Chinese tasks, BEIR (Benchmarking IR), MSMARCO, MIRACL, MLDR, MKQA, AIR-Bench, BRIGHT, and others.", "section": "evaluation", "field": "datasets"},
            ],
        },
        {
            "question": "Why were these evaluation datasets chosen?",
            "target_fields": ["evaluation.motivation"],
            "ground_truth": [
                {"sentence": "The primary motivation is to provide a standardized and holistic evaluation of the model's ability to generate embeddings for a wide range of tasks, including retrieval, classification, clustering, pair classification, reranking, and semantic textual similarity (STS).", "section": "evaluation", "field": "motivation"},
            ],
        },
        {
            # Empty GT → excluded from scoring.
            "question": "What preprocessing was applied during evaluation?",
            "target_fields": [],
            "ground_truth": [],
        },
        {
            "question": "What standards were followed during evaluation?",
            "target_fields": [],
            "ground_truth": [
                {"sentence": "", "section": "evaluation", "field": "standards"},
            ],
        },
        {
            "question": "Is the evaluation data up to date?",
            "target_fields": ["evaluation.update"],
            "ground_truth": [
                {"sentence": "yes", "section": "evaluation", "field": "update"},
            ],
        },
    ],

    "performance": [
        {
            "question": "What does the performance analysis say?",
            "target_fields": ["performance.analysis"],
            "ground_truth": [
                {"sentence": "bge-small-en-v1.5 achieves an average of 62.17 over 7 tasks.", "section": "performance", "field": "analysis"},
                {"sentence": "The model is highly efficient, using 33 million parameters to produce 384-dimension vectors at 130MB runtime memory", "section": "performance", "field": "analysis"},
            ],
        },
        {
            "question": "What are the benchmark metrics?",
            "target_fields": ["performance.metrics"],
            "ground_truth": [
                {"sentence": "Retrieval:\u00a051.68", "section": "performance", "field": "metrics"},
                {"sentence": "Clustering:\u00a043.82", "section": "performance", "field": "metrics"},
                {"sentence": "Pair Classification:\u00a084.92", "section": "performance", "field": "metrics"},
                {"sentence": "Reranking:\u00a058.36", "section": "performance", "field": "metrics"},
                {"sentence": "STS:\u00a081.59", "section": "performance", "field": "metrics"},
                {"sentence": "Summarization:\u00a030.12", "section": "performance", "field": "metrics"},
                {"sentence": "Classification:\u00a074.14\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "**Average:\u00a062.17**", "section": "performance", "field": "metrics"},
            ],
        },
        {
            "question": "What decision thresholds are used?",
            "target_fields": ["performance.thresholds"],
            "ground_truth": [
                {"sentence": "**0.337** minimum matching.", "section": "performance", "field": "thresholds"},
                {"sentence": "Semantic similarity lesser than this is considered irrelevant", "section": "performance", "field": "thresholds"},
            ],
        },
        {
            "question": "What is the evaluation methodology?",
            "target_fields": ["performance.methodology"],
            "ground_truth": [
                {"sentence": "For more information see [FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding/tree/master)", "section": "performance", "field": "methodology"},
                {"sentence": "The primary motivation is to provide a standardized and holistic evaluation of the model's ability to generate embeddings for a wide range of tasks, including retrieval, classification, clustering, pair classification, reranking, and semantic textual similarity (STS).", "section": "evaluation", "field": "motivation"},
            ],
        },
        {
            # Empty GT → excluded from scoring.
            "question": "What is the energy consumption?",
            "target_fields": [],
            "ground_truth": [],
        },
        {
            # Empty GT → excluded from scoring.
            "question": "What is the environmental impact?",
            "target_fields": [],
            "ground_truth": [],
        },
        {
            "question": "Was the model tested for bias?",
            "target_fields": ["performance.bias"],
            "ground_truth": [
                {"sentence": "There are no official documented bias metrics for\u00a0bge-small-en-v1.5", "section": "performance", "field": "bias"},
                {"sentence": "BGE models are state-of-the-art and trained on diverse datasets, making them strong candidates for more robust and fair inference.", "section": "safety", "field": "fairness"},
                {"sentence": "However, fairness is not a concern in this system, as sensitive attributes such as gender, ethnicity, disabilities, and others are not relevant to the task.", "section": "safety", "field": "fairness"},
            ],
        },
    ],

    "safety": [
        {
            "question": "What are the ethical considerations?",
            "target_fields": ["safety.ethics"],
            "ground_truth": [
                {"sentence": "The system extracts and classifies content from third-party URLs without human oversight, which may lead to misrepresentation of information.", "section": "safety", "field": "ethics"},
                {"sentence": "Users should review all auto\u2011populated fields before publication.", "section": "safety", "field": "ethics"},
            ],
        },
        {
            "question": "How is fairness defined / assessed?",
            "target_fields": ["safety.fairness"],
            "ground_truth": [
                {"sentence": "BGE models are state-of-the-art and trained on diverse datasets, making them strong candidates for more robust and fair inference.", "section": "safety", "field": "fairness"},
                {"sentence": "However, fairness is not a concern in this system, as sensitive attributes such as gender, ethnicity, disabilities, and others are not relevant to the task.", "section": "safety", "field": "fairness"},
                {"sentence": "There are no official documented bias metrics for\u00a0bge-small-en-v1.5", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "What are the risks of this model?",
            "target_fields": ["safety.risks"],
            "ground_truth": [
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
                {"sentence": "The system lacks automated validation step.", "section": "safety", "field": "caveats"},
                {"sentence": "Wrong classification must be corrected by the user.", "section": "safety", "field": "caveats"},
                {"sentence": "The system extracts and classifies content from third-party URLs without human oversight, which may lead to misrepresentation of information.", "section": "safety", "field": "ethics"},
            ],
        },
        {
            "question": "Is the model secure / compliant with security standards?",
            "target_fields": ["safety.security"],
            "ground_truth": [
                {"sentence": "The system is designed to prevent malicious content like\u00a0JavaScript injection.", "section": "safety", "field": "security"},
                {"sentence": "However, no red teaming has been performed.", "section": "safety", "field": "security"},
            ],
        },
        {
            "question": "What are the caveats of this model?",
            "target_fields": ["safety.caveats"],
            "ground_truth": [
                {"sentence": "The system lacks automated validation step.", "section": "safety", "field": "caveats"},
                {"sentence": "Wrong classification must be corrected by the user.", "section": "safety", "field": "caveats"},
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
                {"sentence": "The quality of the output directly depends on the quality of the information withing the provided URL.", "section": "use", "field": "factors"},
            ],
        },
    ],

    "paraphrased": [
        {
            "question": "What is the purpose of this model?",
            "target_fields": ["use.use_cases"],
            "ground_truth": [
                {"sentence": "This operation enables the automated retrieval of information from a specified URL and the autocompletion of model card fields.", "section": "overview", "field": "description"},
                {"sentence": "Import external information into a model card", "section": "use", "field": "use_cases"},
            ],
        },
        {
            "question": "What does this model do?",
            "target_fields": ["overview.description"],
            "ground_truth": [
                {"sentence": "This operation enables the automated retrieval of information from a specified URL and the autocompletion of model card fields.", "section": "overview", "field": "description"},
                {"sentence": "Initially, the system fetches textual and image content from the provided URL.", "section": "overview", "field": "description"},
                {"sentence": "The BGE extracts the text and image embeddings which then gets classified into the model card fields by comparing the field description embeddings.", "section": "overview", "field": "description"},
                {"sentence": "Import external information into a model card", "section": "use", "field": "use_cases"},
            ],
        },
        {
            "question": "Which organization built this model?",
            "target_fields": ["overview.creator"],
            "ground_truth": [
                {"sentence": "CERTH - The Centre for Research & Technology, Hellas", "section": "overview", "field": "creator"},
            ],
        },
        {
            "question": "When did this model come out?",
            "target_fields": ["overview.date"],
            "ground_truth": [
                {"sentence": "2025-11-11", "section": "overview", "field": "date"},
            ],
        },
        {
            "question": "What kind of architecture is used?",
            "target_fields": ["overview.type"],
            "ground_truth": [
                {"sentence": "Transformer", "section": "overview", "field": "type"},
                {"sentence": "This function is powered by the BGE model.", "section": "overview", "field": "description"},
                {"sentence": "The system uses the [bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)\u00a0base model.", "section": "training", "field": "datasets"},
            ],
        },
        {
            # FLAG: same as "How many parameters" — GT tagged performance.analysis.
            "question": "What is the size of the model?",
            "target_fields": ["performance.analysis"],
            "ground_truth": [
                {"sentence": "The model is highly efficient, using 33 million parameters to produce 384-dimension vectors at 130MB runtime memory", "section": "performance", "field": "analysis"},
            ],
        },
        {
            "question": "Where do I download it from?",
            "target_fields": ["overview.home"],
            "ground_truth": [
                {"sentence": "[https://trai.mever.gr](https://trai.mever.gr/)", "section": "overview", "field": "home"},
                {"sentence": "The system uses the [bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)\u00a0base model.", "section": "training", "field": "datasets"},
            ],
        },
        {
            "question": "Who should I email about it?",
            "target_fields": ["overview.contact"],
            "ground_truth": [
                {"sentence": "[gnikoul@iti.gr](mailto:gnikoul@iti.gr),\u00a0[maniospas@iti.gr](mailto:maniospas@iti.gr),\u00a0[laaposto@iti.gr](mailto:laaposto@iti.gr)", "section": "overview", "field": "contact"},
            ],
        },
        {
            "question": "What Python packages do I need?",
            "target_fields": ["use.software"],
            "ground_truth": [
                {"sentence": "Python, transformers", "section": "use", "field": "software"},
            ],
        },
        {
            "question": "What GPU do I need to run it?",
            "target_fields": ["use.hardware"],
            "ground_truth": [
                {"sentence": "The model runs on an Intel Xeon CPU E5-2620 0 @ 2.00GHz", "section": "use", "field": "hardware"},
            ],
        },
        {
            "question": "What does the model take as input, and what does it return?",
            "target_fields": ["use.inputs_outputs"],
            "ground_truth": [
                {"sentence": "Input: URL -> Output: model card", "section": "use", "field": "inputs_outputs"},
            ],
        },
        {
            "question": "How do I load and run the model on data?",
            "target_fields": ["use.instructions"],
            "ground_truth": [
                {"sentence": "You can use this operation from any model card by navigating to the **Actions -> Import**\u00a0at the top right corner of the screen.", "section": "use", "field": "instructions"},
                {"sentence": "You can also find more information in our [handbook](https://trai.mever.gr/transparency/handbook.html).", "section": "use", "field": "instructions"},
                {"sentence": "Input: URL -> Output: model card", "section": "use", "field": "inputs_outputs"},
                {"sentence": "Python, transformers", "section": "use", "field": "software"},
            ],
        },
        {
            "question": "What could make its performance worse?",
            "target_fields": ["use.factors"],
            "ground_truth": [
                {"sentence": "The quality of the output directly depends on the quality of the information withing the provided URL.", "section": "use", "field": "factors"},
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
            ],
        },
        {
            "question": "What should this model not be used for?",
            "target_fields": ["use.out_of_scope_use"],
            "ground_truth": [
                {"sentence": "Do not use unrelated sources to import information", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "Who is this model for?",
            "target_fields": ["use.user_groups"],
            "ground_truth": [
                {"sentence": "Model card creators", "section": "use", "field": "user_groups"},
            ],
        },
        {
            "question": "Does a human need to review the outputs?",
            "target_fields": ["use.oversight"],
            "ground_truth": [
                {"sentence": "human-on-the-loop", "section": "use", "field": "oversight"},
                {"sentence": "Users should review all auto\u2011populated fields before publication.", "section": "safety", "field": "ethics"},
                {"sentence": "Wrong classification must be corrected by the user.", "section": "safety", "field": "caveats"},
            ],
        },
        {
            "question": "What does it say about its accuracy?",
            "target_fields": ["performance.metrics"],
            "ground_truth": [
                {"sentence": "bge-small-en-v1.5 achieves an average of 62.17 over 7 tasks.", "section": "performance", "field": "analysis"},
                {"sentence": "Retrieval:\u00a051.68", "section": "performance", "field": "metrics"},
                {"sentence": "Clustering:\u00a043.82", "section": "performance", "field": "metrics"},
                {"sentence": "Pair Classification:\u00a084.92", "section": "performance", "field": "metrics"},
                {"sentence": "Reranking:\u00a058.36", "section": "performance", "field": "metrics"},
                {"sentence": "STS:\u00a081.59", "section": "performance", "field": "metrics"},
                {"sentence": "Summarization:\u00a030.12", "section": "performance", "field": "metrics"},
                {"sentence": "Classification:\u00a074.14\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "**Average:\u00a062.17**", "section": "performance", "field": "metrics"},
            ],
        },
        {
            "question": "What threshold is used to make predictions?",
            "target_fields": ["performance.thresholds"],
            "ground_truth": [
                {"sentence": "**0.337** minimum matching.", "section": "performance", "field": "thresholds"},
                {"sentence": "Semantic similarity lesser than this is considered irrelevant", "section": "performance", "field": "thresholds"},
            ],
        },
        {
            "question": "What could go wrong if I use this model?",
            "target_fields": ["safety.risks"],
            "ground_truth": [
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
                {"sentence": "The system lacks automated validation step.", "section": "safety", "field": "caveats"},
                {"sentence": "Wrong classification must be corrected by the user.", "section": "safety", "field": "caveats"},
                {"sentence": "The system extracts and classifies content from third-party URLs without human oversight, which may lead to misrepresentation of information.", "section": "safety", "field": "ethics"},
                {"sentence": "The quality of the output directly depends on the quality of the information withing the provided URL.", "section": "use", "field": "factors"},
            ],
        },
        {
            "question": "Are there ethical concerns with using this?",
            "target_fields": ["safety.ethics"],
            "ground_truth": [
                {"sentence": "The system extracts and classifies content from third-party URLs without human oversight, which may lead to misrepresentation of information.", "section": "safety", "field": "ethics"},
                {"sentence": "Users should review all auto\u2011populated fields before publication.", "section": "safety", "field": "ethics"},
            ],
        },
        {
            # Empty GT → excluded from scoring.
            "question": "How much energy does it consume?",
            "target_fields": [],
            "ground_truth": [],
        },
        {
            "question": "Is it compliant with any security standard?",
            "target_fields": ["safety.security"],
            "ground_truth": [
                {"sentence": "The system is designed to prevent malicious content like\u00a0JavaScript injection.", "section": "safety", "field": "security"},
                {"sentence": "However, no red teaming has been performed.", "section": "safety", "field": "security"},
            ],
        },
        {
            "question": "Is the model fair across subgroups?",
            "target_fields": ["safety.fairness"],
            "ground_truth": [
                {"sentence": "BGE models are state-of-the-art and trained on diverse datasets, making them strong candidates for more robust and fair inference.", "section": "safety", "field": "fairness"},
                {"sentence": "However, fairness is not a concern in this system, as sensitive attributes such as gender, ethnicity, disabilities, and others are not relevant to the task.", "section": "safety", "field": "fairness"},
                {"sentence": "There are no official documented bias metrics for\u00a0bge-small-en-v1.5", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "What are its known limitations?",
            "target_fields": ["safety.caveats"],
            "ground_truth": [
                {"sentence": "The system lacks automated validation step.", "section": "safety", "field": "caveats"},
                {"sentence": "Wrong classification must be corrected by the user.", "section": "safety", "field": "caveats"},
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
                {"sentence": "The quality of the output directly depends on the quality of the information withing the provided URL.", "section": "use", "field": "factors"},
            ],
        },
        {
            # FLAG: cross-field (training.datasets + evaluation.datasets). Move or split.
            "question": "What datasets was it trained and evaluated on?",
            "target_fields": ["training.datasets", "evaluation.datasets"],
            "ground_truth": [
                {"sentence": "The system uses the [bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)\u00a0base model.", "section": "training", "field": "datasets"},
                {"sentence": "No fine tuning was made.", "section": "training", "field": "datasets"},
                {"sentence": "FlagEmbedding models are evaluated on a comprehensive suite of established information retrieval and text embedding benchmarks.", "section": "evaluation", "field": "datasets"},
                {"sentence": "These include MTEB (Massive Text Embedding Benchmark) for English tasks and C-MTEB for Chinese tasks, BEIR (Benchmarking IR), MSMARCO, MIRACL, MLDR, MKQA, AIR-Bench, BRIGHT, and others.", "section": "evaluation", "field": "datasets"},
            ],
        },
        {
            # FLAG: cross-field (performance.methodology + evaluation.motivation + evaluation.datasets). Move or split.
            "question": "How was the model evaluated?",
            "target_fields": ["performance.methodology", "evaluation.motivation", "evaluation.datasets"],
            "ground_truth": [
                {"sentence": "For more information see [FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding/tree/master)", "section": "performance", "field": "methodology"},
                {"sentence": "The primary motivation is to provide a standardized and holistic evaluation of the model's ability to generate embeddings for a wide range of tasks, including retrieval, classification, clustering, pair classification, reranking, and semantic textual similarity (STS).", "section": "evaluation", "field": "motivation"},
                {"sentence": "FlagEmbedding models are evaluated on a comprehensive suite of established information retrieval and text embedding benchmarks.", "section": "evaluation", "field": "datasets"},
            ],
        },
        {
            # FLAG: cross-field (training.standards + evaluation.standards). Move or split.
            "question": "What standards does it follow?",
            "target_fields": [],
            "ground_truth": [
                {"sentence": "", "section": "training", "field": "standards"},
                {"sentence": "", "section": "evaluation", "field": "standards"},
            ],
        },
    ],

    "cross_field": [
        {
            "question": "Who created this model and what kind of model is it?",
            "target_fields": ["overview.creator", "overview.type"],
            "ground_truth": [
                {"sentence": "CERTH - The Centre for Research & Technology, Hellas", "section": "overview", "field": "creator"},
                {"sentence": "Transformer", "section": "overview", "field": "type"},
                {"sentence": "This function is powered by the BGE model.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "What is the model's task and its intended use?",
            "target_fields": ["overview.task", "use.use_cases"],
            "ground_truth": [
                {"sentence": "Model Card Auto-Fill", "section": "overview", "field": "task"},
                {"sentence": "This operation enables the automated retrieval of information from a specified URL and the autocompletion of model card fields.", "section": "overview", "field": "description"},
                {"sentence": "Import external information into a model card", "section": "use", "field": "use_cases"},
            ],
        },
        {
            "question": "When was the model released and what version is it?",
            "target_fields": ["overview.date", "overview.version"],
            "ground_truth": [
                {"sentence": "2025-11-11", "section": "overview", "field": "date"},
                {"sentence": "1.0", "section": "overview", "field": "version"},
            ],
        },
        {
            "question": "What hardware and software do I need to run this model?",
            "target_fields": ["use.hardware", "use.software"],
            "ground_truth": [
                {"sentence": "The model runs on an Intel Xeon CPU E5-2620 0 @ 2.00GHz", "section": "use", "field": "hardware"},
                {"sentence": "Python, transformers", "section": "use", "field": "software"},
            ],
        },
        {
            "question": "What are the risks and ethical concerns of using this model?",
            "target_fields": ["safety.risks", "safety.ethics"],
            "ground_truth": [
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
                {"sentence": "The system extracts and classifies content from third-party URLs without human oversight, which may lead to misrepresentation of information.", "section": "safety", "field": "ethics"},
                {"sentence": "Users should review all auto\u2011populated fields before publication.", "section": "safety", "field": "ethics"},
                {"sentence": "The system lacks automated validation step.", "section": "safety", "field": "caveats"},
                {"sentence": "Wrong classification must be corrected by the user.", "section": "safety", "field": "caveats"},
            ],
        },
        {
            # Empty GT → excluded from scoring.
            "question": "What is the energy consumption and environmental impact?",
            "target_fields": [],
            "ground_truth": [],
        },
        {
            "question": "Who are the intended users and what oversight is required?",
            "target_fields": ["use.user_groups", "use.oversight"],
            "ground_truth": [
                {"sentence": "Model card creators", "section": "use", "field": "user_groups"},
                {"sentence": "human-on-the-loop", "section": "use", "field": "oversight"},
                {"sentence": "Users should review all auto\u2011populated fields before publication.", "section": "safety", "field": "ethics"},
            ],
        },
        {
            "question": "What are the caveats and out-of-scope uses?",
            "target_fields": ["safety.caveats", "use.out_of_scope_use"],
            "ground_truth": [
                {"sentence": "The system lacks automated validation step.", "section": "safety", "field": "caveats"},
                {"sentence": "Wrong classification must be corrected by the user.", "section": "safety", "field": "caveats"},
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
                {"sentence": "The quality of the output directly depends on the quality of the information withing the provided URL.", "section": "use", "field": "factors"},
                {"sentence": "Do not use unrelated sources to import information", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "How was the model trained and evaluated?",
            "target_fields": [
                "training.datasets", "training.motivation", "training.preprocessing",
                "evaluation.datasets", "evaluation.motivation",
                "performance.methodology",
            ],
            "ground_truth": [
                {"sentence": "The system uses the [bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)\u00a0base model.", "section": "training", "field": "datasets"},
                {"sentence": "No fine tuning was made.", "section": "training", "field": "datasets"},
                {"sentence": "N/A", "section": "training", "field": "motivation"},
                {"sentence": "N/A", "section": "training", "field": "preprocessing"},
                {"sentence": "FlagEmbedding models are evaluated on a comprehensive suite of established information retrieval and text embedding benchmarks.", "section": "evaluation", "field": "datasets"},
                {"sentence": "These include MTEB (Massive Text Embedding Benchmark) for English tasks and C-MTEB for Chinese tasks, BEIR (Benchmarking IR), MSMARCO, MIRACL, MLDR, MKQA, AIR-Bench, BRIGHT, and others.", "section": "evaluation", "field": "datasets"},
                {"sentence": "The primary motivation is to provide a standardized and holistic evaluation of the model's ability to generate embeddings for a wide range of tasks, including retrieval, classification, clustering, pair classification, reranking, and semantic textual similarity (STS).", "section": "evaluation", "field": "motivation"},
                {"sentence": "For more information see [FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding/tree/master)", "section": "performance", "field": "methodology"},
            ],
        },
        {
            "question": "What are the input/output formats, and how do I run the model?",
            "target_fields": ["use.inputs_outputs", "use.instructions"],
            "ground_truth": [
                {"sentence": "Input: URL -> Output: model card", "section": "use", "field": "inputs_outputs"},
                {"sentence": "You can use this operation from any model card by navigating to the **Actions -> Import**\u00a0at the top right corner of the screen.", "section": "use", "field": "instructions"},
                {"sentence": "You can also find more information in our [handbook](https://trai.mever.gr/transparency/handbook.html).", "section": "use", "field": "instructions"},
                {"sentence": "Python, transformers", "section": "use", "field": "software"},
            ],
        },
        {
            "question": "What technical or ethical standards does the model follow?",
            "target_fields": ["safety.ethics"],
            "ground_truth": [
                {"sentence": "", "section": "training", "field": "standards"},
                {"sentence": "", "section": "evaluation", "field": "standards"},
                {"sentence": "The system extracts and classifies content from third-party URLs without human oversight, which may lead to misrepresentation of information.", "section": "safety", "field": "ethics"},
                {"sentence": "Users should review all auto\u2011populated fields before publication.", "section": "safety", "field": "ethics"},
            ],
        },
        {
            "question": "What factors could degrade performance, and what are the known caveats?",
            "target_fields": ["use.factors", "safety.risks", "safety.caveats"],
            "ground_truth": [
                {"sentence": "The quality of the output directly depends on the quality of the information withing the provided URL.", "section": "use", "field": "factors"},
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
                {"sentence": "The system lacks automated validation step.", "section": "safety", "field": "caveats"},
                {"sentence": "Wrong classification must be corrected by the user.", "section": "safety", "field": "caveats"},
            ],
        },
        {
            "question": "How do I install the software, and what hardware does it need?",
            "target_fields": ["use.software", "use.hardware"],
            "ground_truth": [
                {"sentence": "Python, transformers", "section": "use", "field": "software"},
                {"sentence": "The model runs on an Intel Xeon CPU E5-2620 0 @ 2.00GHz", "section": "use", "field": "hardware"},
            ],
        },
        {
            "question": "Who should use this model, and what should they not do with it?",
            "target_fields": ["use.user_groups", "use.use_cases", "use.out_of_scope_use"],
            "ground_truth": [
                {"sentence": "Model card creators", "section": "use", "field": "user_groups"},
                {"sentence": "Import external information into a model card", "section": "use", "field": "use_cases"},
                {"sentence": "Do not use unrelated sources to import information", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "What is the model's license and how do I cite it?",
            "target_fields": ["overview.license", "overview.citation"],
            "ground_truth": [
                {"sentence": "TBD", "section": "overview", "field": "license"},
                {"sentence": "Use this model card as a citation", "section": "overview", "field": "citation"},
            ],
        },
    ],

}