GROUND_TRUTH = {
    "overview": [
        {
            "question": "What is the name of this model?",
            "target_fields": ["overview.name"],
            "ground_truth": [
                {"sentence": "Video-FaceSwap Detector", "section": "overview", "field": "name"},
            ],
        },
        {
            "question": "What is this model used for?",
            "target_fields": ["use.use_cases"],
            "ground_truth": [
                {"sentence": "This model is designed for Video Deepfake Detection tasks, specialized in detecting\u00a0face-swap and face-reenactment manipulations, not fully AI-generated videos.", "section": "overview", "field": "description"},
                {"sentence": "It focuses on the participants faces and by utilizing only the vision stream of the video (not the audio) determines whether a person\u2019s face has been replaced or manipulated within the video.", "section": "overview", "field": "description"},
                {"sentence": "Detection of face-swap or face-reenactment manipulations in a video.", "section": "use", "field": "use_cases"},
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
                {"sentence": "2026-03-20", "section": "overview", "field": "date"},
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
            ],
        },
        {
            # Empty GT → excluded from scoring.
            "question": "How many parameters does this model have?",
            "target_fields": [],
            "ground_truth": [],
        },
        {
            "question": "What is the task of this model?",
            "target_fields": ["overview.task"],
            "ground_truth": [
                {"sentence": "Video Classification", "section": "overview", "field": "task"},
                {"sentence": "This model is designed for Video Deepfake Detection tasks, specialized in detecting\u00a0face-swap and face-reenactment manipulations, not fully AI-generated videos.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "What is the license of this model?",
            "target_fields": ["overview.license"],
            "ground_truth": [
                {"sentence": "Apache-2.0", "section": "overview", "field": "license"},
            ],
        },
        {
            # Empty GT → excluded from scoring.
            "question": "Where can I find this model?",
            "target_fields": [],
            "ground_truth": [],
        },
        {
            "question": "Who can I contact about this model?",
            "target_fields": ["overview.contact"],
            "ground_truth": [
                {"sentence": "Stelios Mylonas: [smylonas@iti.gr](mailto:smylonas@iti.gr)", "section": "overview", "field": "contact"},
            ],
        },
        {
            # Empty GT → excluded from scoring.
            "question": "How should I cite this model?",
            "target_fields": [],
            "ground_truth": [],
        },
    ],

    "use": [
        {
            "question": "What are the intended use cases?",
            "target_fields": ["use.use_cases"],
            "ground_truth": [
                {"sentence": "Detection of face-swap or face-reenactment manipulations in a video.", "section": "use", "field": "use_cases"},
                {"sentence": "This model is designed for Video Deepfake Detection tasks, specialized in detecting\u00a0face-swap and face-reenactment manipulations, not fully AI-generated videos.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "What level of human oversight is required?",
            "target_fields": ["use.oversight"],
            "ground_truth": [
                {"sentence": "human-in-the-loop", "section": "use", "field": "oversight"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Unsupervised decision making, Detection of AI-generated videos", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "Who are the intended user groups?",
            "target_fields": ["use.user_groups"],
            "ground_truth": [
                {"sentence": "Researchers, media professionals, fact-checkers", "section": "use", "field": "user_groups"},
            ],
        },
        {
            "question": "What is this model not intended for?",
            "target_fields": ["use.out_of_scope_use"],
            "ground_truth": [
                {"sentence": "Unsupervised decision making, Detection of AI-generated videos", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            # Empty GT → excluded from scoring.
            "question": "What software does this model require?",
            "target_fields": [],
            "ground_truth": [],
        },
        {
            # FLAG: GT is tagged use.inputs_outputs (no instructions sentence exists in this card).
            # Using use.instructions here because the question semantically asks for instructions.
            # Change to ["use.inputs_outputs"] to follow the GT tag literally.
            "question": "How do I run / use this model?",
            "target_fields": ["use.instructions"],
            "ground_truth": [
                {"sentence": "Input: Video\n\nOutput: Score in range \\[0,1\\] indicating whether the video has been manipulated or not", "section": "use", "field": "inputs_outputs"},
            ],
        },
        {
            "question": "What are the inputs and outputs of the model?",
            "target_fields": ["use.inputs_outputs"],
            "ground_truth": [
                {"sentence": "Input: Video\n\nOutput: Score in range \\[0,1\\] indicating whether the video has been manipulated or not", "section": "use", "field": "inputs_outputs"},
            ],
        },
        {
            "question": "What factors affect the model's performance?",
            "target_fields": ["use.factors"],
            "ground_truth": [
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
            ],
        },
        {
            # Empty GT → excluded from scoring.
            "question": "What hardware is required?",
            "target_fields": [],
            "ground_truth": [],
        },
    ],

    "training": [
        {
            "question": "What datasets were used for training?",
            "target_fields": ["training.datasets"],
            "ground_truth": [
                {"sentence": "FaceForensics++, CelebDF-v2, DFDC,\u00a0ForgeryNet", "section": "training", "field": "datasets"},
            ],
        },
        {
            "question": "Why were these training datasets chosen?",
            "target_fields": ["training.motivation"],
            "ground_truth": [
                {"sentence": "These datasets cover a wide range of manipulation techniques spanning multiple context and filming conditions", "section": "training", "field": "motivation"},
            ],
        },
        {
            "question": "What preprocessing was applied during training?",
            "target_fields": ["training.preprocessing"],
            "ground_truth": [
                {"sentence": "\\- Face detection  \n\\- Enlarge faces by a factor of 1.3  \n\\- Crop faces and resize to 224x224  \n\\- Data augmentation during training (random resized crop, random flipping, color jittering, cutout)", "section": "training", "field": "preprocessing"},
            ],
        },
        {
            "question": "What standards were followed during training?",
            "target_fields": ["training.standards"],
            "ground_truth": [
                {"sentence": "IEEE", "section": "training", "field": "standards"},
            ],
        },
        {
            "question": "Is the training data up to date?",
            "target_fields": ["training.update"],
            "ground_truth": [
                {"sentence": "yes", "section": "training", "field": "update"},
            ],
        },
    ],

    "evaluation": [
        {
            "question": "What datasets were used for evaluation?",
            "target_fields": ["evaluation.datasets"],
            "ground_truth": [
                {"sentence": "Celeb-DF-v3, DF40, DeepSpeak-v1, DeepSpeak-v2, WDF,\u00a0Deepfake-Eval-2024", "section": "evaluation", "field": "datasets"},
            ],
        },
        {
            "question": "Why were these evaluation datasets chosen?",
            "target_fields": ["evaluation.motivation"],
            "ground_truth": [
                {"sentence": "The evaluation set covers multiple recent datasets reflecting the wide diversity of manipulation techniques currently available.", "section": "evaluation", "field": "motivation"},
                {"sentence": "It also includes two 'in-the-wild' datasets helping us to measure the model's performance on real and unrestricted conditions.", "section": "evaluation", "field": "motivation"},
            ],
        },
        {
            "question": "What preprocessing was applied during evaluation?",
            "target_fields": ["evaluation.preprocessing"],
            "ground_truth": [
                {"sentence": "\\- Sample the video at 1 FPS\n\n\\- Face detection\n\n\\- Enlarge faces by a factor of 1.3\n\n\\- Crop faces and resize to 224x224", "section": "evaluation", "field": "preprocessing"},
            ],
        },
        {
            "question": "What standards were followed during evaluation?",
            "target_fields": ["evaluation.standards"],
            "ground_truth": [
                {"sentence": "IEEE", "section": "evaluation", "field": "standards"},
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
                {"sentence": "We present video-level AUC scores and Average Precision (AP) for each dataset.", "section": "performance", "field": "analysis"},
            ],
        },
        {
            "question": "What are the benchmark metrics?",
            "target_fields": ["performance.metrics"],
            "ground_truth": [
                {"sentence": "\u00a0 \u00a0 \u00a0Dataset\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0AUC(%)\u00a0 \u00a0 \u00a0AP(%)  \n\u00a0 \u00a0 -----------------------------------------------------", "section": "performance", "field": "metrics"},
                {"sentence": "*   Celeb-DF-v3:\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a086.7\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 89.9", "section": "performance", "field": "metrics"},
                {"sentence": "*   DF40:\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a087.6\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 95.1\u00a0\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "*   DeepSpeak-v1:\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 91.5\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 93.4", "section": "performance", "field": "metrics"},
                {"sentence": "*   DeepSpeak-v2:\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 77.5\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 77.4", "section": "performance", "field": "metrics"},
                {"sentence": "*   WDF:\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 94.9\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 93.6", "section": "performance", "field": "metrics"},
                {"sentence": "*   DeepFake-Eval-2024:\u00a0 62.8\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 92.8", "section": "performance", "field": "metrics"},
            ],
        },
        {
            "question": "What decision thresholds are used?",
            "target_fields": ["performance.thresholds"],
            "ground_truth": [
                {"sentence": "AUC and AP do not need any calibration threshold", "section": "performance", "field": "thresholds"},
            ],
        },
        {
            "question": "What is the evaluation methodology?",
            "target_fields": ["performance.methodology"],
            "ground_truth": [
                {"sentence": "For Celeb-DF-v3 and DF40, the scores presented are averaged across the different manipulation methods.", "section": "performance", "field": "methodology"},
            ],
        },
        {
            # GT is tagged performance.environmental_impact, not energy_consumption.
            "question": "What is the energy consumption?",
            "target_fields": ["performance.environmental_impact"],
            "ground_truth": [
                {"sentence": "Energy consumptions depends on input size and hardware.", "section": "performance", "field": "environmental_impact"},
            ],
        },
        {
            "question": "What is the environmental impact?",
            "target_fields": ["performance.environmental_impact"],
            "ground_truth": [
                {"sentence": "Energy consumptions depends on input size and hardware.", "section": "performance", "field": "environmental_impact"},
            ],
        },
        {
            "question": "Was the model tested for bias?",
            "target_fields": ["performance.bias"],
            "ground_truth": [
                {"sentence": "The model was not tested for its bias across various demographic groups.", "section": "performance", "field": "bias"},
                {"sentence": "Fairness is defined as the property that the model\u2019s prediction error rates (false positives and false negatives) remain consistent across different\u00a0 demographic subgroups.", "section": "safety", "field": "fairness"},
            ],
        },
    ],

    "safety": [
        {
            "question": "What are the ethical considerations?",
            "target_fields": ["safety.ethics"],
            "ground_truth": [
                {"sentence": "Risk of false positives: mislabeling authentic videos as fake could undermine trust in legitimate sources or individuals.", "section": "safety", "field": "ethics"},
                {"sentence": "It is recommended to cross-validate your results with several deepfake detectors.", "section": "safety", "field": "ethics"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
            ],
        },
        {
            "question": "How is fairness defined / assessed?",
            "target_fields": ["safety.fairness"],
            "ground_truth": [
                {"sentence": "Fairness is defined as the property that the model\u2019s prediction error rates (false positives and false negatives) remain consistent across different\u00a0 demographic subgroups.", "section": "safety", "field": "fairness"},
                {"sentence": "The model was not tested for its bias across various demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "What are the risks of this model?",
            "target_fields": ["safety.risks"],
            "ground_truth": [
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Risk of false positives: mislabeling authentic videos as fake could undermine trust in legitimate sources or individuals.", "section": "safety", "field": "ethics"},
                {"sentence": "The Video FaceSwap detector is not future-proof and it may have low accuracy on new face manipulation methods without fine-tuning.", "section": "safety", "field": "caveats"},
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
            ],
        },
        {
            "question": "Is the model secure / compliant with security standards?",
            "target_fields": ["safety.security"],
            "ground_truth": [
                {"sentence": "The model does not take into account any cybersecurity standards", "section": "safety", "field": "security"},
            ],
        },
        {
            "question": "What are the caveats of this model?",
            "target_fields": ["safety.caveats"],
            "ground_truth": [
                {"sentence": "The Video FaceSwap detector is not future-proof and it may have low accuracy on new face manipulation methods without fine-tuning.", "section": "safety", "field": "caveats"},
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
                {"sentence": "The model was not tested for its bias across various demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
    ],

    "paraphrased": [
        {
            "question": "What is the purpose of this model?",
            "target_fields": ["use.use_cases"],
            "ground_truth": [
                {"sentence": "This model is designed for Video Deepfake Detection tasks, specialized in detecting\u00a0face-swap and face-reenactment manipulations, not fully AI-generated videos.", "section": "overview", "field": "description"},
                {"sentence": "It focuses on the participants faces and by utilizing only the vision stream of the video (not the audio) determines whether a person\u2019s face has been replaced or manipulated within the video.", "section": "overview", "field": "description"},
                {"sentence": "Detection of face-swap or face-reenactment manipulations in a video.", "section": "use", "field": "use_cases"},
            ],
        },
        {
            "question": "What does this model do?",
            "target_fields": ["overview.description"],
            "ground_truth": [
                {"sentence": "This model is designed for Video Deepfake Detection tasks, specialized in detecting\u00a0face-swap and face-reenactment manipulations, not fully AI-generated videos.", "section": "overview", "field": "description"},
                {"sentence": "It focuses on the participants faces and by utilizing only the vision stream of the video (not the audio) determines whether a person\u2019s face has been replaced or manipulated within the video.", "section": "overview", "field": "description"},
                {"sentence": "Detection of face-swap or face-reenactment manipulations in a video.", "section": "use", "field": "use_cases"},
                {"sentence": "Input: Video\n\nOutput: Score in range \\[0,1\\] indicating whether the video has been manipulated or not", "section": "use", "field": "inputs_outputs"},
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
                {"sentence": "2026-03-20", "section": "overview", "field": "date"},
            ],
        },
        {
            "question": "What kind of architecture is used?",
            "target_fields": ["overview.type"],
            "ground_truth": [
                {"sentence": "Transformer", "section": "overview", "field": "type"},
            ],
        },
        {
            # Empty GT → excluded from scoring.
            "question": "What is the size of the model?",
            "target_fields": [],
            "ground_truth": [],
        },
        {
            # Empty GT → excluded from scoring.
            "question": "Where do I download it from?",
            "target_fields": [],
            "ground_truth": [],
        },
        {
            "question": "Who should I email about it?",
            "target_fields": ["overview.contact"],
            "ground_truth": [
                {"sentence": "Stelios Mylonas: [smylonas@iti.gr](mailto:smylonas@iti.gr)", "section": "overview", "field": "contact"},
            ],
        },
        {
            # Empty GT → excluded from scoring.
            "question": "What Python packages do I need?",
            "target_fields": [],
            "ground_truth": [],
        },
        {
            # Empty GT → excluded from scoring.
            "question": "What GPU do I need to run it?",
            "target_fields": [],
            "ground_truth": [],
        },
        {
            "question": "What does the model take as input, and what does it return?",
            "target_fields": ["use.inputs_outputs"],
            "ground_truth": [
                {"sentence": "Input: Video\n\nOutput: Score in range \\[0,1\\] indicating whether the video has been manipulated or not", "section": "use", "field": "inputs_outputs"},
            ],
        },
        {
            # FLAG: same as "How do I run / use this model?" — GT tagged use.inputs_outputs, question asks for instructions.
            "question": "How do I load and run the model on data?",
            "target_fields": ["use.instructions"],
            "ground_truth": [
                {"sentence": "Input: Video\n\nOutput: Score in range \\[0,1\\] indicating whether the video has been manipulated or not", "section": "use", "field": "inputs_outputs"},
            ],
        },
        {
            "question": "What could make its performance worse?",
            "target_fields": ["use.factors"],
            "ground_truth": [
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
                {"sentence": "The Video FaceSwap detector is not future-proof and it may have low accuracy on new face manipulation methods without fine-tuning.", "section": "safety", "field": "caveats"},
            ],
        },
        {
            "question": "What should this model not be used for?",
            "target_fields": ["use.out_of_scope_use"],
            "ground_truth": [
                {"sentence": "Unsupervised decision making, Detection of AI-generated videos", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "Who is this model for?",
            "target_fields": ["use.user_groups"],
            "ground_truth": [
                {"sentence": "Researchers, media professionals, fact-checkers", "section": "use", "field": "user_groups"},
            ],
        },
        {
            "question": "Does a human need to review the outputs?",
            "target_fields": ["use.oversight"],
            "ground_truth": [
                {"sentence": "human-in-the-loop", "section": "use", "field": "oversight"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Unsupervised decision making, Detection of AI-generated videos", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "What does it say about its accuracy?",
            "target_fields": ["performance.metrics"],
            "ground_truth": [
                {"sentence": "We present video-level AUC scores and Average Precision (AP) for each dataset.", "section": "performance", "field": "analysis"},
                {"sentence": "\u00a0 \u00a0 \u00a0Dataset\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0AUC(%)\u00a0 \u00a0 \u00a0AP(%)  \n\u00a0 \u00a0 -----------------------------------------------------", "section": "performance", "field": "metrics"},
                {"sentence": "*   Celeb-DF-v3:\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a086.7\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 89.9", "section": "performance", "field": "metrics"},
                {"sentence": "*   DF40:\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a087.6\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 95.1\u00a0\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "*   DeepSpeak-v1:\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 91.5\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 93.4", "section": "performance", "field": "metrics"},
                {"sentence": "*   DeepSpeak-v2:\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 77.5\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 77.4", "section": "performance", "field": "metrics"},
                {"sentence": "*   WDF:\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 94.9\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 93.6", "section": "performance", "field": "metrics"},
                {"sentence": "*   DeepFake-Eval-2024:\u00a0 62.8\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 92.8", "section": "performance", "field": "metrics"},
            ],
        },
        {
            "question": "What threshold is used to make predictions?",
            "target_fields": ["performance.thresholds"],
            "ground_truth": [
                {"sentence": "AUC and AP do not need any calibration threshold", "section": "performance", "field": "thresholds"},
            ],
        },
        {
            "question": "What could go wrong if I use this model?",
            "target_fields": ["safety.risks"],
            "ground_truth": [
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Risk of false positives: mislabeling authentic videos as fake could undermine trust in legitimate sources or individuals.", "section": "safety", "field": "ethics"},
                {"sentence": "The Video FaceSwap detector is not future-proof and it may have low accuracy on new face manipulation methods without fine-tuning.", "section": "safety", "field": "caveats"},
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
            ],
        },
        {
            "question": "Are there ethical concerns with using this?",
            "target_fields": ["safety.ethics"],
            "ground_truth": [
                {"sentence": "Risk of false positives: mislabeling authentic videos as fake could undermine trust in legitimate sources or individuals.", "section": "safety", "field": "ethics"},
                {"sentence": "It is recommended to cross-validate your results with several deepfake detectors.", "section": "safety", "field": "ethics"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
            ],
        },
        {
            "question": "How much energy does it consume?",
            "target_fields": ["performance.environmental_impact"],
            "ground_truth": [
                {"sentence": "Energy consumptions depends on input size and hardware.", "section": "performance", "field": "environmental_impact"},
            ],
        },
        {
            "question": "Is it compliant with any security standard?",
            "target_fields": ["safety.security"],
            "ground_truth": [
                {"sentence": "The model does not take into account any cybersecurity standards", "section": "safety", "field": "security"},
            ],
        },
        {
            "question": "Is the model fair across subgroups?",
            "target_fields": ["safety.fairness"],
            "ground_truth": [
                {"sentence": "Fairness is defined as the property that the model\u2019s prediction error rates (false positives and false negatives) remain consistent across different\u00a0 demographic subgroups.", "section": "safety", "field": "fairness"},
                {"sentence": "The model was not tested for its bias across various demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "What are its known limitations?",
            "target_fields": ["safety.caveats"],
            "ground_truth": [
                {"sentence": "The Video FaceSwap detector is not future-proof and it may have low accuracy on new face manipulation methods without fine-tuning.", "section": "safety", "field": "caveats"},
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
                {"sentence": "The model was not tested for its bias across various demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            # FLAG: semantically cross-field (training.datasets + evaluation.datasets). Move to cross_field or split.
            "question": "What datasets was it trained and evaluated on?",
            "target_fields": ["training.datasets", "evaluation.datasets"],
            "ground_truth": [
                {"sentence": "FaceForensics++, CelebDF-v2, DFDC,\u00a0ForgeryNet", "section": "training", "field": "datasets"},
                {"sentence": "Celeb-DF-v3, DF40, DeepSpeak-v1, DeepSpeak-v2, WDF,\u00a0Deepfake-Eval-2024", "section": "evaluation", "field": "datasets"},
            ],
        },
        {
            # FLAG: GT includes performance.analysis (not methodology). Using the actual GT tags.
            "question": "How was the model evaluated?",
            "target_fields": ["performance.analysis", "performance.thresholds", "performance.methodology"],
            "ground_truth": [
                {"sentence": "We present video-level AUC scores and Average Precision (AP) for each dataset.", "section": "performance", "field": "analysis"},
                {"sentence": "AUC and AP do not need any calibration threshold", "section": "performance", "field": "thresholds"},
                {"sentence": "For Celeb-DF-v3 and DF40, the scores presented are averaged across the different manipulation methods.", "section": "performance", "field": "methodology"},
            ],
        },
        {
            # FLAG: semantically cross-field (training.standards + evaluation.standards). Move to cross_field or split.
            "question": "What standards does it follow?",
            "target_fields": ["training.standards", "evaluation.standards"],
            "ground_truth": [
                {"sentence": "IEEE", "section": "training", "field": "standards"},
                {"sentence": "IEEE", "section": "evaluation", "field": "standards"},
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
            ],
        },
        {
            "question": "What is the model's task and its intended use?",
            "target_fields": ["overview.task", "use.use_cases"],
            "ground_truth": [
                {"sentence": "Video Classification", "section": "overview", "field": "task"},
                {"sentence": "This model is designed for Video Deepfake Detection tasks, specialized in detecting\u00a0face-swap and face-reenactment manipulations, not fully AI-generated videos.", "section": "overview", "field": "description"},
                {"sentence": "Detection of face-swap or face-reenactment manipulations in a video.", "section": "use", "field": "use_cases"},
            ],
        },
        {
            "question": "When was the model released and what version is it?",
            "target_fields": ["overview.date", "overview.version"],
            "ground_truth": [
                {"sentence": "2026-03-20", "section": "overview", "field": "date"},
                {"sentence": "1.0", "section": "overview", "field": "version"},
            ],
        },
        {
            # Empty GT → excluded from scoring.
            "question": "What hardware and software do I need to run this model?",
            "target_fields": [],
            "ground_truth": [],
        },
        {
            "question": "What are the risks and ethical concerns of using this model?",
            "target_fields": ["safety.risks", "safety.ethics"],
            "ground_truth": [
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Risk of false positives: mislabeling authentic videos as fake could undermine trust in legitimate sources or individuals.", "section": "safety", "field": "ethics"},
                {"sentence": "It is recommended to cross-validate your results with several deepfake detectors.", "section": "safety", "field": "ethics"},
            ],
        },
        {
            # Single target because both aspects live in environmental_impact.
            "question": "What is the energy consumption and environmental impact?",
            "target_fields": ["performance.environmental_impact"],
            "ground_truth": [
                {"sentence": "Energy consumptions depends on input size and hardware.", "section": "performance", "field": "environmental_impact"},
            ],
        },
        {
            "question": "Who are the intended users and what oversight is required?",
            "target_fields": ["use.user_groups", "use.oversight"],
            "ground_truth": [
                {"sentence": "Researchers, media professionals, fact-checkers", "section": "use", "field": "user_groups"},
                {"sentence": "human-in-the-loop", "section": "use", "field": "oversight"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
            ],
        },
        {
            "question": "What are the caveats and out-of-scope uses?",
            "target_fields": ["safety.caveats", "use.factors", "performance.bias", "use.out_of_scope_use"],
            "ground_truth": [
                {"sentence": "The Video FaceSwap detector is not future-proof and it may have low accuracy on new face manipulation methods without fine-tuning.", "section": "safety", "field": "caveats"},
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
                {"sentence": "The model was not tested for its bias across various demographic groups.", "section": "performance", "field": "bias"},
                {"sentence": "Unsupervised decision making, Detection of AI-generated videos", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "How was the model trained and evaluated?",
            "target_fields": [
                "training.datasets", "training.motivation", "training.preprocessing",
                "evaluation.datasets", "evaluation.motivation", "evaluation.preprocessing",
                "performance.analysis", "performance.methodology",
            ],
            "ground_truth": [
                {"sentence": "FaceForensics++, CelebDF-v2, DFDC,\u00a0ForgeryNet", "section": "training", "field": "datasets"},
                {"sentence": "These datasets cover a wide range of manipulation techniques spanning multiple context and filming conditions", "section": "training", "field": "motivation"},
                {"sentence": "\\- Face detection  \n\\- Enlarge faces by a factor of 1.3  \n\\- Crop faces and resize to 224x224  \n\\- Data augmentation during training (random resized crop, random flipping, color jittering, cutout)", "section": "training", "field": "preprocessing"},
                {"sentence": "Celeb-DF-v3, DF40, DeepSpeak-v1, DeepSpeak-v2, WDF,\u00a0Deepfake-Eval-2024", "section": "evaluation", "field": "datasets"},
                {"sentence": "The evaluation set covers multiple recent datasets reflecting the wide diversity of manipulation techniques currently available.", "section": "evaluation", "field": "motivation"},
                {"sentence": "It also includes two 'in-the-wild' datasets helping us to measure the model's performance on real and unrestricted conditions.", "section": "evaluation", "field": "motivation"},
                {"sentence": "\\- Sample the video at 1 FPS\n\n\\- Face detection\n\n\\- Enlarge faces by a factor of 1.3\n\n\\- Crop faces and resize to 224x224", "section": "evaluation", "field": "preprocessing"},
                {"sentence": "We present video-level AUC scores and Average Precision (AP) for each dataset.", "section": "performance", "field": "analysis"},
                {"sentence": "For Celeb-DF-v3 and DF40, the scores presented are averaged across the different manipulation methods.", "section": "performance", "field": "methodology"},
            ],
        },
        {
            # FLAG: GT only has use.inputs_outputs. Added use.instructions because the question asks for both.
            # If you want strict GT-tag adherence, drop "use.instructions".
            "question": "What are the input/output formats, and how do I run the model?",
            "target_fields": ["use.inputs_outputs", "use.instructions"],
            "ground_truth": [
                {"sentence": "Input: Video\n\nOutput: Score in range \\[0,1\\] indicating whether the video has been manipulated or not", "section": "use", "field": "inputs_outputs"},
            ],
        },
        {
            "question": "What technical or ethical standards does the model follow?",
            "target_fields": ["training.standards", "evaluation.standards", "safety.ethics"],
            "ground_truth": [
                {"sentence": "IEEE", "section": "training", "field": "standards"},
                {"sentence": "IEEE", "section": "evaluation", "field": "standards"},
                {"sentence": "Risk of false positives: mislabeling authentic videos as fake could undermine trust in legitimate sources or individuals.", "section": "safety", "field": "ethics"},
                {"sentence": "It is recommended to cross-validate your results with several deepfake detectors.", "section": "safety", "field": "ethics"},
            ],
        },
        {
            "question": "What factors could degrade performance, and what are the known caveats?",
            "target_fields": ["use.factors", "safety.caveats", "performance.bias"],
            "ground_truth": [
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
                {"sentence": "The Video FaceSwap detector is not future-proof and it may have low accuracy on new face manipulation methods without fine-tuning.", "section": "safety", "field": "caveats"},
                {"sentence": "The model was not tested for its bias across various demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            # Empty GT → excluded from scoring.
            "question": "How do I install the software, and what hardware does it need?",
            "target_fields": [],
            "ground_truth": [],
        },
        {
            "question": "Who should use this model, and what should they not do with it?",
            "target_fields": ["use.user_groups", "use.use_cases", "use.out_of_scope_use"],
            "ground_truth": [
                {"sentence": "Researchers, media professionals, fact-checkers", "section": "use", "field": "user_groups"},
                {"sentence": "Detection of face-swap or face-reenactment manipulations in a video.", "section": "use", "field": "use_cases"},
                {"sentence": "Unsupervised decision making, Detection of AI-generated videos", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            # Single target: citation is empty in this card. Validator will flag cross_field with <2 targets.
            "question": "What is the model's license and how do I cite it?",
            "target_fields": ["overview.license"],
            "ground_truth": [
                {"sentence": "Apache-2.0", "section": "overview", "field": "license"},
            ],
        },
    ],
}