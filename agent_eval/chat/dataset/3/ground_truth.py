GROUND_TRUTH = {
    "overview": [
        {
            "question": "What is the name of this model?",
            "ground_truth": [
                {"sentence": "TrAI-Import", "section": "overview", "field": "name"},
            ],
        },
        {
            "question": "What is this model used for?",
            "ground_truth": [
                {"sentence": "This operation enables the automated retrieval of information from a specified URL and the autocompletion of model card fields.", "section": "overview", "field": "description"},
                {"sentence": "Import external information into a model card", "section": "use", "field": "use_cases"},
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
                {"sentence": "2025-11-11", "section": "overview", "field": "date"},
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
                {"sentence": "This function is powered by the BGE model.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "How many parameters does this model have?",
            "ground_truth": [
                {"sentence": "The model is highly efficient, using 33 million parameters to produce 384-dimension vectors at 130MB runtime memory", "section": "performance", "field": "analysis"},
            ],
        },
        {
            "question": "What is the task of this model?",
            "ground_truth": [
                {"sentence": "Model Card Auto-Fill", "section": "overview", "field": "task"},
                {"sentence": "This operation enables the automated retrieval of information from a specified URL and the autocompletion of model card fields.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "What is the license of this model?",
            "ground_truth": [
                {"sentence": "TBD", "section": "overview", "field": "license"},
            ],
        },
        {
            "question": "Where can I find this model?",
            "ground_truth": [
                {"sentence": "[https://trai.mever.gr](https://trai.mever.gr/)", "section": "overview", "field": "home"},
            ],
        },
        {
            "question": "Who can I contact about this model?",
            "ground_truth": [
                {"sentence": "[gnikoul@iti.gr](mailto:gnikoul@iti.gr),\u00a0[maniospas@iti.gr](mailto:maniospas@iti.gr),\u00a0[laaposto@iti.gr](mailto:laaposto@iti.gr)", "section": "overview", "field": "contact"},
            ],
        },
        {
            "question": "How should I cite this model?",
            "ground_truth": [
                {"sentence": "Use this model card as a citation", "section": "overview", "field": "citation"},
            ],
        },
    ],

    "use": [
        {
            "question": "What are the intended use cases?",
            "ground_truth": [
                {"sentence": "Import external information into a model card", "section": "use", "field": "use_cases"},
                {"sentence": "This operation enables the automated retrieval of information from a specified URL and the autocompletion of model card fields.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "What level of human oversight is required?",
            "ground_truth": [
                {"sentence": "human-on-the-loop", "section": "use", "field": "oversight"},
                {"sentence": "Users should review all auto\u2011populated fields before publication.", "section": "safety", "field": "ethics"},
            ],
        },
        {
            "question": "Who are the intended user groups?",
            "ground_truth": [
                {"sentence": "Model card creators", "section": "use", "field": "user_groups"},
            ],
        },
        {
            "question": "What is this model not intended for?",
            "ground_truth": [
                {"sentence": "Do not use unrelated sources to import information", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "What software does this model require?",
            "ground_truth": [
                {"sentence": "Python, transformers", "section": "use", "field": "software"},
            ],
        },
        {
            "question": "How do I run / use this model?",
            "ground_truth": [
                {"sentence": "You can use this operation from any model card by navigating to the **Actions -> Import**\u00a0at the top right corner of the screen.", "section": "use", "field": "instructions"},
                {"sentence": "You can also find more information in our [handbook](https://trai.mever.gr/transparency/handbook.html).", "section": "use", "field": "instructions"},
                {"sentence": "Input: URL -> Output: model card", "section": "use", "field": "inputs_outputs"},
                {"sentence": "Python, transformers", "section": "use", "field": "software"},
            ],
        },
        {
            "question": "What are the inputs and outputs of the model?",
            "ground_truth": [
                {"sentence": "Input: URL -> Output: model card", "section": "use", "field": "inputs_outputs"},
                {"sentence": "This operation enables the automated retrieval of information from a specified URL and the autocompletion of model card fields.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "What factors affect the model's performance?",
            "ground_truth": [
                {"sentence": "The quality of the output directly depends on the quality of the information withing the provided URL.", "section": "use", "field": "factors"},
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
            ],
        },
        {
            "question": "What hardware is required?",
            "ground_truth": [
                {"sentence": "The model runs on an Intel Xeon CPU E5-2620 0 @ 2.00GHz", "section": "use", "field": "hardware"},
            ],
        },
    ],

    "training": [
        {
            "question": "What datasets were used for training?",
            "ground_truth": [
                {"sentence": "The system uses the [bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)\u00a0base model.", "section": "training", "field": "datasets"},
                {"sentence": "No fine tuning was made.", "section": "training", "field": "datasets"},
                {"sentence": "This function is powered by the BGE model.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "Why were these training datasets chosen?",
            "ground_truth": [
                {"sentence": "N/A", "section": "training", "field": "motivation"},
            ],
        },
        {
            "question": "What preprocessing was applied during training?",
            "ground_truth": [
                {"sentence": "N/A", "section": "training", "field": "preprocessing"},
            ],
        },
        {
            "question": "What standards were followed during training?",
            "ground_truth": [
                {"sentence": "N/A", "section": "training", "field": "standards"},
            ],
        },
        {
            "question": "Is the training data up to date?",
            "ground_truth": [
                {"sentence": "N/A", "section": "training", "field": "update"},
            ],
        },
    ],

    "evaluation": [
        {
            "question": "What datasets were used for evaluation?",
            "ground_truth": [
                {"sentence": "FlagEmbedding models are evaluated on a comprehensive suite of established information retrieval and text embedding benchmarks.", "section": "evaluation", "field": "datasets"},
                {"sentence": "These include MTEB (Massive Text Embedding Benchmark) for English tasks and C-MTEB for Chinese tasks, BEIR (Benchmarking IR), MSMARCO, MIRACL, MLDR, MKQA, AIR-Bench, BRIGHT, and others.", "section": "evaluation", "field": "datasets"},
            ],
        },
        {
            "question": "Why were these evaluation datasets chosen?",
            "ground_truth": [
                {"sentence": "The primary motivation is to provide a standardized and holistic evaluation of the model's ability to generate embeddings for a wide range of tasks, including retrieval, classification, clustering, pair classification, reranking, and semantic textual similarity (STS).", "section": "evaluation", "field": "motivation"},
            ],
        },
        {
            "question": "What preprocessing was applied during evaluation?",
            "ground_truth": [],
        },
        {
            "question": "What standards were followed during evaluation?",
            "ground_truth": [
                {"sentence": "unknown", "section": "evaluation", "field": "standards"},
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
                {"sentence": "bge-small-en-v1.5 achieves an average of 62.17 over 7 tasks.", "section": "performance", "field": "analysis"},
                {"sentence": "The model is highly efficient, using 33 million parameters to produce 384-dimension vectors at 130MB runtime memory", "section": "performance", "field": "analysis"},
            ],
        },
        {
            "question": "What are the benchmark metrics?",
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
            "ground_truth": [
                {"sentence": "**0.337** minimum matching.", "section": "performance", "field": "thresholds"},
                {"sentence": "Semantic similarity lesser than this is considered irrelevant", "section": "performance", "field": "thresholds"},
            ],
        },
        {
            "question": "What is the evaluation methodology?",
            "ground_truth": [
                {"sentence": "For more information see [FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding/tree/master)", "section": "performance", "field": "methodology"},
                {"sentence": "The primary motivation is to provide a standardized and holistic evaluation of the model's ability to generate embeddings for a wide range of tasks, including retrieval, classification, clustering, pair classification, reranking, and semantic textual similarity (STS).", "section": "evaluation", "field": "motivation"},
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
                {"sentence": "There are no official documented bias metrics for\u00a0bge-small-en-v1.5", "section": "performance", "field": "bias"},
                {"sentence": "BGE models are state-of-the-art and trained on diverse datasets, making them strong candidates for more robust and fair inference.", "section": "safety", "field": "fairness"},
                {"sentence": "However, fairness is not a concern in this system, as sensitive attributes such as gender, ethnicity, disabilities, and others are not relevant to the task.", "section": "safety", "field": "fairness"},
            ],
        },
    ],

    "safety": [
        {
            "question": "What are the ethical considerations?",
            "ground_truth": [
                {"sentence": "The system extracts and classifies content from third-party URLs without human oversight, which may lead to misrepresentation of information.", "section": "safety", "field": "ethics"},
                {"sentence": "Users should review all auto\u2011populated fields before publication.", "section": "safety", "field": "ethics"},
            ],
        },
        {
            "question": "How is fairness defined / assessed?",
            "ground_truth": [
                {"sentence": "BGE models are state-of-the-art and trained on diverse datasets, making them strong candidates for more robust and fair inference.", "section": "safety", "field": "fairness"},
                {"sentence": "However, fairness is not a concern in this system, as sensitive attributes such as gender, ethnicity, disabilities, and others are not relevant to the task.", "section": "safety", "field": "fairness"},
                {"sentence": "There are no official documented bias metrics for\u00a0bge-small-en-v1.5", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "What are the risks of this model?",
            "ground_truth": [
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
                {"sentence": "The system lacks automated validation step.", "section": "safety", "field": "caveats"},
                {"sentence": "Wrong classification must be corrected by the user.", "section": "safety", "field": "caveats"},
                {"sentence": "The system extracts and classifies content from third-party URLs without human oversight, which may lead to misrepresentation of information.", "section": "safety", "field": "ethics"},
            ],
        },
        {
            "question": "Is the model secure / compliant with security standards?",
            "ground_truth": [
                {"sentence": "The system is designed to prevent malicious content like\u00a0JavaScript injection.", "section": "safety", "field": "security"},
                {"sentence": "However, no red teaming has been performed.", "section": "safety", "field": "security"},
            ],
        },
        {
            "question": "What are the caveats of this model?",
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
            "ground_truth": [
                {"sentence": "This operation enables the automated retrieval of information from a specified URL and the autocompletion of model card fields.", "section": "overview", "field": "description"},
                {"sentence": "Import external information into a model card", "section": "use", "field": "use_cases"},
            ],
        },
        {
            "question": "What does this model do?",
            "ground_truth": [
                {"sentence": "This operation enables the automated retrieval of information from a specified URL and the autocompletion of model card fields.", "section": "overview", "field": "description"},
                {"sentence": "Initially, the system fetches textual and image content from the provided URL.", "section": "overview", "field": "description"},
                {"sentence": "The BGE extracts the text and image embeddings which then gets classified into the model card fields by comparing the field description embeddings.", "section": "overview", "field": "description"},
                {"sentence": "Import external information into a model card", "section": "use", "field": "use_cases"},
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
                {"sentence": "2025-11-11", "section": "overview", "field": "date"},
            ],
        },
        {
            "question": "What kind of architecture is used?",
            "ground_truth": [
                {"sentence": "Transformer", "section": "overview", "field": "type"},
                {"sentence": "This function is powered by the BGE model.", "section": "overview", "field": "description"},
                {"sentence": "The system uses the [bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)\u00a0base model.", "section": "training", "field": "datasets"},
            ],
        },
        {
            "question": "What is the size of the model?",
            "ground_truth": [
                {"sentence": "The model is highly efficient, using 33 million parameters to produce 384-dimension vectors at 130MB runtime memory", "section": "performance", "field": "analysis"},
            ],
        },
        {
            "question": "Where do I download it from?",
            "ground_truth": [
                {"sentence": "[https://trai.mever.gr](https://trai.mever.gr/)", "section": "overview", "field": "home"},
                {"sentence": "The system uses the [bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)\u00a0base model.", "section": "training", "field": "datasets"},
            ],
        },
        {
            "question": "Who should I email about it?",
            "ground_truth": [
                {"sentence": "[gnikoul@iti.gr](mailto:gnikoul@iti.gr),\u00a0[maniospas@iti.gr](mailto:maniospas@iti.gr),\u00a0[laaposto@iti.gr](mailto:laaposto@iti.gr)", "section": "overview", "field": "contact"},
            ],
        },
        {
            "question": "What Python packages do I need?",
            "ground_truth": [
                {"sentence": "Python, transformers", "section": "use", "field": "software"},
            ],
        },
        {
            "question": "What GPU do I need to run it?",
            "ground_truth": [
                {"sentence": "The model runs on an Intel Xeon CPU E5-2620 0 @ 2.00GHz", "section": "use", "field": "hardware"},
            ],
        },
        {
            "question": "What does the model take as input, and what does it return?",
            "ground_truth": [
                {"sentence": "Input: URL -> Output: model card", "section": "use", "field": "inputs_outputs"},
            ],
        },
        {
            "question": "How do I load and run the model on data?",
            "ground_truth": [
                {"sentence": "You can use this operation from any model card by navigating to the **Actions -> Import**\u00a0at the top right corner of the screen.", "section": "use", "field": "instructions"},
                {"sentence": "You can also find more information in our [handbook](https://trai.mever.gr/transparency/handbook.html).", "section": "use", "field": "instructions"},
                {"sentence": "Input: URL -> Output: model card", "section": "use", "field": "inputs_outputs"},
                {"sentence": "Python, transformers", "section": "use", "field": "software"},
            ],
        },
        {
            "question": "What could make its performance worse?",
            "ground_truth": [
                {"sentence": "The quality of the output directly depends on the quality of the information withing the provided URL.", "section": "use", "field": "factors"},
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
            ],
        },
        {
            "question": "What should this model not be used for?",
            "ground_truth": [
                {"sentence": "Do not use unrelated sources to import information", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "Who is this model for?",
            "ground_truth": [
                {"sentence": "Model card creators", "section": "use", "field": "user_groups"},
            ],
        },
        {
            "question": "Does a human need to review the outputs?",
            "ground_truth": [
                {"sentence": "human-on-the-loop", "section": "use", "field": "oversight"},
                {"sentence": "Users should review all auto\u2011populated fields before publication.", "section": "safety", "field": "ethics"},
                {"sentence": "Wrong classification must be corrected by the user.", "section": "safety", "field": "caveats"},
            ],
        },
        {
            "question": "What does it say about its accuracy?",
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
            "ground_truth": [
                {"sentence": "**0.337** minimum matching.", "section": "performance", "field": "thresholds"},
                {"sentence": "Semantic similarity lesser than this is considered irrelevant", "section": "performance", "field": "thresholds"},
            ],
        },
        {
            "question": "What could go wrong if I use this model?",
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
            "ground_truth": [
                {"sentence": "The system extracts and classifies content from third-party URLs without human oversight, which may lead to misrepresentation of information.", "section": "safety", "field": "ethics"},
                {"sentence": "Users should review all auto\u2011populated fields before publication.", "section": "safety", "field": "ethics"},
            ],
        },
        {
            "question": "How much energy does it consume?",
            "ground_truth": [],
        },
        {
            "question": "Is it compliant with any security standard?",
            "ground_truth": [
                {"sentence": "The system is designed to prevent malicious content like\u00a0JavaScript injection.", "section": "safety", "field": "security"},
                {"sentence": "However, no red teaming has been performed.", "section": "safety", "field": "security"},
            ],
        },
        {
            "question": "Is the model fair across subgroups?",
            "ground_truth": [
                {"sentence": "BGE models are state-of-the-art and trained on diverse datasets, making them strong candidates for more robust and fair inference.", "section": "safety", "field": "fairness"},
                {"sentence": "However, fairness is not a concern in this system, as sensitive attributes such as gender, ethnicity, disabilities, and others are not relevant to the task.", "section": "safety", "field": "fairness"},
                {"sentence": "There are no official documented bias metrics for\u00a0bge-small-en-v1.5", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "What are its known limitations?",
            "ground_truth": [
                {"sentence": "The system lacks automated validation step.", "section": "safety", "field": "caveats"},
                {"sentence": "Wrong classification must be corrected by the user.", "section": "safety", "field": "caveats"},
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
                {"sentence": "The quality of the output directly depends on the quality of the information withing the provided URL.", "section": "use", "field": "factors"},
            ],
        },
        {
            "question": "What datasets was it trained and evaluated on?",
            "ground_truth": [
                {"sentence": "The system uses the [bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)\u00a0base model.", "section": "training", "field": "datasets"},
                {"sentence": "No fine tuning was made.", "section": "training", "field": "datasets"},
                {"sentence": "FlagEmbedding models are evaluated on a comprehensive suite of established information retrieval and text embedding benchmarks.", "section": "evaluation", "field": "datasets"},
                {"sentence": "These include MTEB (Massive Text Embedding Benchmark) for English tasks and C-MTEB for Chinese tasks, BEIR (Benchmarking IR), MSMARCO, MIRACL, MLDR, MKQA, AIR-Bench, BRIGHT, and others.", "section": "evaluation", "field": "datasets"},
            ],
        },
        {
            "question": "How was the model evaluated?",
            "ground_truth": [
                {"sentence": "For more information see [FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding/tree/master)", "section": "performance", "field": "methodology"},
                {"sentence": "The primary motivation is to provide a standardized and holistic evaluation of the model's ability to generate embeddings for a wide range of tasks, including retrieval, classification, clustering, pair classification, reranking, and semantic textual similarity (STS).", "section": "evaluation", "field": "motivation"},
                {"sentence": "FlagEmbedding models are evaluated on a comprehensive suite of established information retrieval and text embedding benchmarks.", "section": "evaluation", "field": "datasets"},
            ],
        },
        {
            "question": "What standards does it follow?",
            "ground_truth": [
                {"sentence": "N/A", "section": "training", "field": "standards"},
                {"sentence": "unknown", "section": "evaluation", "field": "standards"},
            ],
        },
    ],

    "cross_field": [
        {
            "question": "Who created this model and what kind of model is it?",
            "ground_truth": [
                {"sentence": "CERTH - The Centre for Research & Technology, Hellas", "section": "overview", "field": "creator"},
                {"sentence": "Transformer", "section": "overview", "field": "type"},
                {"sentence": "This function is powered by the BGE model.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "What is the model's task and its intended use?",
            "ground_truth": [
                {"sentence": "Model Card Auto-Fill", "section": "overview", "field": "task"},
                {"sentence": "This operation enables the automated retrieval of information from a specified URL and the autocompletion of model card fields.", "section": "overview", "field": "description"},
                {"sentence": "Import external information into a model card", "section": "use", "field": "use_cases"},
            ],
        },
        {
            "question": "When was the model released and what version is it?",
            "ground_truth": [
                {"sentence": "2025-11-11", "section": "overview", "field": "date"},
                {"sentence": "1.0", "section": "overview", "field": "version"},
            ],
        },
        {
            "question": "What hardware and software do I need to run this model?",
            "ground_truth": [
                {"sentence": "The model runs on an Intel Xeon CPU E5-2620 0 @ 2.00GHz", "section": "use", "field": "hardware"},
                {"sentence": "Python, transformers", "section": "use", "field": "software"},
            ],
        },
        {
            "question": "What are the risks and ethical concerns of using this model?",
            "ground_truth": [
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
                {"sentence": "The system extracts and classifies content from third-party URLs without human oversight, which may lead to misrepresentation of information.", "section": "safety", "field": "ethics"},
                {"sentence": "Users should review all auto\u2011populated fields before publication.", "section": "safety", "field": "ethics"},
                {"sentence": "The system lacks automated validation step.", "section": "safety", "field": "caveats"},
                {"sentence": "Wrong classification must be corrected by the user.", "section": "safety", "field": "caveats"},
            ],
        },
        {
            "question": "What is the energy consumption and environmental impact?",
            "ground_truth": [],
        },
        {
            "question": "Who are the intended users and what oversight is required?",
            "ground_truth": [
                {"sentence": "Model card creators", "section": "use", "field": "user_groups"},
                {"sentence": "human-on-the-loop", "section": "use", "field": "oversight"},
                {"sentence": "Users should review all auto\u2011populated fields before publication.", "section": "safety", "field": "ethics"},
            ],
        },
        {
            "question": "What are the caveats and out-of-scope uses?",
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
            "ground_truth": [
                {"sentence": "Input: URL -> Output: model card", "section": "use", "field": "inputs_outputs"},
                {"sentence": "You can use this operation from any model card by navigating to the **Actions -> Import**\u00a0at the top right corner of the screen.", "section": "use", "field": "instructions"},
                {"sentence": "You can also find more information in our [handbook](https://trai.mever.gr/transparency/handbook.html).", "section": "use", "field": "instructions"},
                {"sentence": "Python, transformers", "section": "use", "field": "software"},
            ],
        },
        {
            "question": "What technical or ethical standards does the model follow?",
            "ground_truth": [
                {"sentence": "N/A", "section": "training", "field": "standards"},
                {"sentence": "unknown", "section": "evaluation", "field": "standards"},
                {"sentence": "The system extracts and classifies content from third-party URLs without human oversight, which may lead to misrepresentation of information.", "section": "safety", "field": "ethics"},
                {"sentence": "Users should review all auto\u2011populated fields before publication.", "section": "safety", "field": "ethics"},
            ],
        },
        {
            "question": "What factors could degrade performance, and what are the known caveats?",
            "ground_truth": [
                {"sentence": "The quality of the output directly depends on the quality of the information withing the provided URL.", "section": "use", "field": "factors"},
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
                {"sentence": "The system lacks automated validation step.", "section": "safety", "field": "caveats"},
                {"sentence": "Wrong classification must be corrected by the user.", "section": "safety", "field": "caveats"},
            ],
        },
        {
            "question": "How do I install the software, and what hardware does it need?",
            "ground_truth": [
                {"sentence": "Python, transformers", "section": "use", "field": "software"},
                {"sentence": "The model runs on an Intel Xeon CPU E5-2620 0 @ 2.00GHz", "section": "use", "field": "hardware"},
            ],
        },
        {
            "question": "Who should use this model, and what should they not do with it?",
            "ground_truth": [
                {"sentence": "Model card creators", "section": "use", "field": "user_groups"},
                {"sentence": "Import external information into a model card", "section": "use", "field": "use_cases"},
                {"sentence": "Do not use unrelated sources to import information", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "What is the model's license and how do I cite it?",
            "ground_truth": [
                {"sentence": "TBD", "section": "overview", "field": "license"},
                {"sentence": "Use this model card as a citation", "section": "overview", "field": "citation"},
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
                {"sentence": "However, fairness is not a concern in this system, as sensitive attributes such as gender, ethnicity, disabilities, and others are not relevant to the task.", "section": "safety", "field": "fairness"},
                {"sentence": "There are no official documented bias metrics for\u00a0bge-small-en-v1.5", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "What is the model's robustness to adversarial attacks?",
            "ground_truth": [
                {"sentence": "The system is designed to prevent malicious content like\u00a0JavaScript injection.", "section": "safety", "field": "security"},
                {"sentence": "However, no red teaming has been performed.", "section": "safety", "field": "security"},
            ],
        },
        {
            "question": "What is the model's water usage?",
            "ground_truth": [],
        },
        {
            "question": "Who are the individual authors (not the institution)?",
            "ground_truth": [
                {"sentence": "[gnikoul@iti.gr](mailto:gnikoul@iti.gr),\u00a0[maniospas@iti.gr](mailto:maniospas@iti.gr),\u00a0[laaposto@iti.gr](mailto:laaposto@iti.gr)", "section": "overview", "field": "contact"},
            ],
        },
        {
            "question": "Can you provide the citation in BibTeX format?",
            "ground_truth": [],
        },
        {
            "question": "What is the inference latency per request?",
            "ground_truth": [],
        },
        {
            "question": "What is the model file size on disk?",
            "ground_truth": [
                {"sentence": "The model is highly efficient, using 33 million parameters to produce 384-dimension vectors at 130MB runtime memory", "section": "performance", "field": "analysis"},
            ],
        },
        {
            "question": "What data privacy measures are in place?",
            "ground_truth": [
                {"sentence": "The system extracts and classifies content from third-party URLs without human oversight, which may lead to misrepresentation of information.", "section": "safety", "field": "ethics"},
            ],
        },
        {
            "question": "Is the model explainable / interpretable?",
            "ground_truth": [
                {"sentence": "The BGE extracts the text and image embeddings which then gets classified into the model card fields by comparing the field description embeddings.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "Does the model handle audio / video modalities (if not applicable)?",
            "ground_truth": [
                {"sentence": "Initially, the system fetches textual and image content from the provided URL.", "section": "overview", "field": "description"},
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
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
                {"sentence": "The system extracts and classifies content from third-party URLs without human oversight, which may lead to misrepresentation of information.", "section": "safety", "field": "ethics"},
                {"sentence": "Users should review all auto\u2011populated fields before publication.", "section": "safety", "field": "ethics"},
                {"sentence": "The system lacks automated validation step.", "section": "safety", "field": "caveats"},
                {"sentence": "Wrong classification must be corrected by the user.", "section": "safety", "field": "caveats"},
                {"sentence": "The system is designed to prevent malicious content like\u00a0JavaScript injection.", "section": "safety", "field": "security"},
                {"sentence": "However, no red teaming has been performed.", "section": "safety", "field": "security"},
            ],
        },
        {
            "question": "What are the limitations of this model?",
            "ground_truth": [
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
                {"sentence": "The system lacks automated validation step.", "section": "safety", "field": "caveats"},
                {"sentence": "Wrong classification must be corrected by the user.", "section": "safety", "field": "caveats"},
                {"sentence": "The quality of the output directly depends on the quality of the information withing the provided URL.", "section": "use", "field": "factors"},
                {"sentence": "The system extracts and classifies content from third-party URLs without human oversight, which may lead to misrepresentation of information.", "section": "safety", "field": "ethics"},
            ],
        },
        {
            "question": "Is this model accurate?",
            "ground_truth": [
                {"sentence": "bge-small-en-v1.5 achieves an average of 62.17 over 7 tasks.", "section": "performance", "field": "analysis"},
                {"sentence": "**Average:\u00a062.17**", "section": "performance", "field": "metrics"},
            ],
        },
        {
            "question": "Is this model good?",
            "ground_truth": [
                {"sentence": "bge-small-en-v1.5 achieves an average of 62.17 over 7 tasks.", "section": "performance", "field": "analysis"},
                {"sentence": "The model is highly efficient, using 33 million parameters to produce 384-dimension vectors at 130MB runtime memory", "section": "performance", "field": "analysis"},
                {"sentence": "**Average:\u00a062.17**", "section": "performance", "field": "metrics"},
                {"sentence": "BGE models are state-of-the-art and trained on diverse datasets, making them strong candidates for more robust and fair inference.", "section": "safety", "field": "fairness"},
            ],
        },
        {
            "question": "How does this model work?",
            "ground_truth": [
                {"sentence": "This operation enables the automated retrieval of information from a specified URL and the autocompletion of model card fields.", "section": "overview", "field": "description"},
                {"sentence": "This function is powered by the BGE model.", "section": "overview", "field": "description"},
                {"sentence": "Initially, the system fetches textual and image content from the provided URL.", "section": "overview", "field": "description"},
                {"sentence": "The BGE extracts the text and image embeddings which then gets classified into the model card fields by comparing the field description embeddings.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "Is this model trustworthy?",
            "ground_truth": [
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
                {"sentence": "The system lacks automated validation step.", "section": "safety", "field": "caveats"},
                {"sentence": "Wrong classification must be corrected by the user.", "section": "safety", "field": "caveats"},
                {"sentence": "The system extracts and classifies content from third-party URLs without human oversight, which may lead to misrepresentation of information.", "section": "safety", "field": "ethics"},
                {"sentence": "Users should review all auto\u2011populated fields before publication.", "section": "safety", "field": "ethics"},
                {"sentence": "However, no red teaming has been performed.", "section": "safety", "field": "security"},
            ],
        },
        {
            "question": "What is this model's main contribution?",
            "ground_truth": [
                {"sentence": "This operation enables the automated retrieval of information from a specified URL and the autocompletion of model card fields.", "section": "overview", "field": "description"},
                {"sentence": "Initially, the system fetches textual and image content from the provided URL.", "section": "overview", "field": "description"},
                {"sentence": "The BGE extracts the text and image embeddings which then gets classified into the model card fields by comparing the field description embeddings.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "Is this model reliable?",
            "ground_truth": [
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
                {"sentence": "The system lacks automated validation step.", "section": "safety", "field": "caveats"},
                {"sentence": "Wrong classification must be corrected by the user.", "section": "safety", "field": "caveats"},
                {"sentence": "The quality of the output directly depends on the quality of the information withing the provided URL.", "section": "use", "field": "factors"},
            ],
        },
        {
            "question": "What makes this model novel?",
            "ground_truth": [
                {"sentence": "This operation enables the automated retrieval of information from a specified URL and the autocompletion of model card fields.", "section": "overview", "field": "description"},
                {"sentence": "Initially, the system fetches textual and image content from the provided URL.", "section": "overview", "field": "description"},
                {"sentence": "The BGE extracts the text and image embeddings which then gets classified into the model card fields by comparing the field description embeddings.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "Is this model ready for production?",
            "ground_truth": [
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
                {"sentence": "The system lacks automated validation step.", "section": "safety", "field": "caveats"},
                {"sentence": "Wrong classification must be corrected by the user.", "section": "safety", "field": "caveats"},
            ],
        },
        {
            "question": "Is this model eco-friendly?",
            "ground_truth": [],
        },
        {
            "question": "How do I use this model?",
            "ground_truth": [
                {"sentence": "You can use this operation from any model card by navigating to the **Actions -> Import**\u00a0at the top right corner of the screen.", "section": "use", "field": "instructions"},
                {"sentence": "You can also find more information in our [handbook](https://trai.mever.gr/transparency/handbook.html).", "section": "use", "field": "instructions"},
                {"sentence": "Input: URL -> Output: model card", "section": "use", "field": "inputs_outputs"},
                {"sentence": "Python, transformers", "section": "use", "field": "software"},
                {"sentence": "The model runs on an Intel Xeon CPU E5-2620 0 @ 2.00GHz", "section": "use", "field": "hardware"},
            ],
        },
        {
            "question": "What should I know before using this model?",
            "ground_truth": [
                {"sentence": "The system is designed for HuggingFace\u2011style documentation pages and may fail on other website layouts, producing empty or incorrect fields.", "section": "safety", "field": "risks"},
                {"sentence": "The system lacks automated validation step.", "section": "safety", "field": "caveats"},
                {"sentence": "Wrong classification must be corrected by the user.", "section": "safety", "field": "caveats"},
                {"sentence": "The system extracts and classifies content from third-party URLs without human oversight, which may lead to misrepresentation of information.", "section": "safety", "field": "ethics"},
                {"sentence": "Users should review all auto\u2011populated fields before publication.", "section": "safety", "field": "ethics"},
                {"sentence": "The quality of the output directly depends on the quality of the information withing the provided URL.", "section": "use", "field": "factors"},
                {"sentence": "However, no red teaming has been performed.", "section": "safety", "field": "security"},
                {"sentence": "Do not use unrelated sources to import information", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "Can I use this model commercially?",
            "ground_truth": [
                {"sentence": "TBD", "section": "overview", "field": "license"},
            ],
        },
        {
            "question": "What are the main takeaways about this model?",
            "ground_truth": [
                {"sentence": "This operation enables the automated retrieval of information from a specified URL and the autocompletion of model card fields.", "section": "overview", "field": "description"},
                {"sentence": "This function is powered by the BGE model.", "section": "overview", "field": "description"},
                {"sentence": "Initially, the system fetches textual and image content from the provided URL.", "section": "overview", "field": "description"},
                {"sentence": "The BGE extracts the text and image embeddings which then gets classified into the model card fields by comparing the field description embeddings.", "section": "overview", "field": "description"},
                {"sentence": "bge-small-en-v1.5 achieves an average of 62.17 over 7 tasks.", "section": "performance", "field": "analysis"},
                {"sentence": "The model is highly efficient, using 33 million parameters to produce 384-dimension vectors at 130MB runtime memory", "section": "performance", "field": "analysis"},
                {"sentence": "The system lacks automated validation step.", "section": "safety", "field": "caveats"},
                {"sentence": "Wrong classification must be corrected by the user.", "section": "safety", "field": "caveats"},
            ],
        },
    ],
}