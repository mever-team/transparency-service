GROUND_TRUTH = {
    "overview": [
        {
            "question": "What is the name of this model?",
            "ground_truth": [
                {"sentence": "Video-FaceSwap Detector", "section": "overview", "field": "name"},
            ],
        },
        {
            "question": "What is this model used for?",
            "ground_truth": [
                {"sentence": "This model is designed for Video Deepfake Detection tasks, specialized in detecting\u00a0face-swap and face-reenactment manipulations, not fully AI-generated videos.", "section": "overview", "field": "description"},
                {"sentence": "It focuses on the participants faces and by utilizing only the vision stream of the video (not the audio) determines whether a person\u2019s face has been replaced or manipulated within the video.", "section": "overview", "field": "description"},
                {"sentence": "Detection of face-swap or face-reenactment manipulations in a video.", "section": "use", "field": "use_cases"},
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
                {"sentence": "2026-03-20", "section": "overview", "field": "date"},
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
                {"sentence": "Video Classification", "section": "overview", "field": "task"},
                {"sentence": "This model is designed for Video Deepfake Detection tasks, specialized in detecting\u00a0face-swap and face-reenactment manipulations, not fully AI-generated videos.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "What is the license of this model?",
            "ground_truth": [
                {"sentence": "Apache-2.0", "section": "overview", "field": "license"},
            ],
        },
        {
            "question": "Where can I find this model?",
            "ground_truth": [],
        },
        {
            "question": "Who can I contact about this model?",
            "ground_truth": [
                {"sentence": "Stelios Mylonas: [smylonas@iti.gr](mailto:smylonas@iti.gr)", "section": "overview", "field": "contact"},
            ],
        },
        {
            "question": "How should I cite this model?",
            "ground_truth": [],
        },
    ],

    "use": [
        {
            "question": "What are the intended use cases?",
            "ground_truth": [
                {"sentence": "Detection of face-swap or face-reenactment manipulations in a video.", "section": "use", "field": "use_cases"},
                {"sentence": "This model is designed for Video Deepfake Detection tasks, specialized in detecting\u00a0face-swap and face-reenactment manipulations, not fully AI-generated videos.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "What level of human oversight is required?",
            "ground_truth": [
                {"sentence": "human-in-the-loop", "section": "use", "field": "oversight"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Unsupervised decision making, Detection of AI-generated videos", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "Who are the intended user groups?",
            "ground_truth": [
                {"sentence": "Researchers, media professionals, fact-checkers", "section": "use", "field": "user_groups"},
            ],
        },
        {
            "question": "What is this model not intended for?",
            "ground_truth": [
                {"sentence": "Unsupervised decision making, Detection of AI-generated videos", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "What software does this model require?",
            "ground_truth": [],
        },
        {
            "question": "How do I run / use this model?",
            "ground_truth": [
                {"sentence": "Input: Video\n\nOutput: Score in range \\[0,1\\] indicating whether the video has been manipulated or not", "section": "use", "field": "inputs_outputs"},
            ],
        },
        {
            "question": "What are the inputs and outputs of the model?",
            "ground_truth": [
                {"sentence": "Input: Video\n\nOutput: Score in range \\[0,1\\] indicating whether the video has been manipulated or not", "section": "use", "field": "inputs_outputs"},
            ],
        },
        {
            "question": "What factors affect the model's performance?",
            "ground_truth": [
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
            ],
        },
        {
            "question": "What hardware is required?",
            "ground_truth": [],
        },
    ],

    "training": [
        {
            "question": "What datasets were used for training?",
            "ground_truth": [
                {"sentence": "FaceForensics++, CelebDF-v2, DFDC,\u00a0ForgeryNet", "section": "training", "field": "datasets"},
            ],
        },
        {
            "question": "Why were these training datasets chosen?",
            "ground_truth": [
                {"sentence": "These datasets cover a wide range of manipulation techniques spanning multiple context and filming conditions", "section": "training", "field": "motivation"},
            ],
        },
        {
            "question": "What preprocessing was applied during training?",
            "ground_truth": [
                {"sentence": "\\- Face detection  \n\\- Enlarge faces by a factor of 1.3  \n\\- Crop faces and resize to 224x224  \n\\- Data augmentation during training (random resized crop, random flipping, color jittering, cutout)", "section": "training", "field": "preprocessing"},
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
                {"sentence": "Celeb-DF-v3, DF40, DeepSpeak-v1, DeepSpeak-v2, WDF,\u00a0Deepfake-Eval-2024", "section": "evaluation", "field": "datasets"},
            ],
        },
        {
            "question": "Why were these evaluation datasets chosen?",
            "ground_truth": [
                {"sentence": "The evaluation set covers multiple recent datasets reflecting the wide diversity of manipulation techniques currently available.", "section": "evaluation", "field": "motivation"},
                {"sentence": "It also includes two 'in-the-wild' datasets helping us to measure the model's performance on real and unrestricted conditions.", "section": "evaluation", "field": "motivation"},
            ],
        },
        {
            "question": "What preprocessing was applied during evaluation?",
            "ground_truth": [
                {"sentence": "\\- Sample the video at 1 FPS\n\n\\- Face detection\n\n\\- Enlarge faces by a factor of 1.3\n\n\\- Crop faces and resize to 224x224", "section": "evaluation", "field": "preprocessing"},
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
                {"sentence": "We present video-level AUC scores and Average Precision (AP) for each dataset.", "section": "performance", "field": "analysis"},
            ],
        },
        {
            "question": "What are the benchmark metrics?",
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
            "ground_truth": [
                {"sentence": "AUC and AP do not need any calibration threshold", "section": "performance", "field": "thresholds"},
            ],
        },
        {
            "question": "What is the evaluation methodology?",
            "ground_truth": [
                {"sentence": "For Celeb-DF-v3 and DF40, the scores presented are averaged across the different manipulation methods.", "section": "performance", "field": "methodology"},
            ],
        },
        {
            "question": "What is the energy consumption?",
            "ground_truth": [
                {"sentence": "Energy consumptions depends on input size and hardware.", "section": "performance", "field": "environmental_impact"},
            ],
        },
        {
            "question": "What is the environmental impact?",
            "ground_truth": [
                {"sentence": "Energy consumptions depends on input size and hardware.", "section": "performance", "field": "environmental_impact"},
            ],
        },
        {
            "question": "Was the model tested for bias?",
            "ground_truth": [
                {"sentence": "The model was not tested for its bias across various demographic groups.", "section": "performance", "field": "bias"},
                {"sentence": "Fairness is defined as the property that the model\u2019s prediction error rates (false positives and false negatives) remain consistent across different\u00a0 demographic subgroups.", "section": "safety", "field": "fairness"},
            ],
        },
    ],

    "safety": [
        {
            "question": "What are the ethical considerations?",
            "ground_truth": [
                {"sentence": "Risk of false positives: mislabeling authentic videos as fake could undermine trust in legitimate sources or individuals.", "section": "safety", "field": "ethics"},
                {"sentence": "It is recommended to cross-validate your results with several deepfake detectors.", "section": "safety", "field": "ethics"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
            ],
        },
        {
            "question": "How is fairness defined / assessed?",
            "ground_truth": [
                {"sentence": "Fairness is defined as the property that the model\u2019s prediction error rates (false positives and false negatives) remain consistent across different\u00a0 demographic subgroups.", "section": "safety", "field": "fairness"},
                {"sentence": "The model was not tested for its bias across various demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "What are the risks of this model?",
            "ground_truth": [
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Risk of false positives: mislabeling authentic videos as fake could undermine trust in legitimate sources or individuals.", "section": "safety", "field": "ethics"},
                {"sentence": "The Video FaceSwap detector is not future-proof and it may have low accuracy on new face manipulation methods without fine-tuning.", "section": "safety", "field": "caveats"},
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
            ],
        },
        {
            "question": "Is the model secure / compliant with security standards?",
            "ground_truth": [
                {"sentence": "The model does not take into account any cybersecurity standards", "section": "safety", "field": "security"},
            ],
        },
        {
            "question": "What are the caveats of this model?",
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
            "ground_truth": [
                {"sentence": "This model is designed for Video Deepfake Detection tasks, specialized in detecting\u00a0face-swap and face-reenactment manipulations, not fully AI-generated videos.", "section": "overview", "field": "description"},
                {"sentence": "It focuses on the participants faces and by utilizing only the vision stream of the video (not the audio) determines whether a person\u2019s face has been replaced or manipulated within the video.", "section": "overview", "field": "description"},
                {"sentence": "Detection of face-swap or face-reenactment manipulations in a video.", "section": "use", "field": "use_cases"},
            ],
        },
        {
            "question": "What does this model do?",
            "ground_truth": [
                {"sentence": "This model is designed for Video Deepfake Detection tasks, specialized in detecting\u00a0face-swap and face-reenactment manipulations, not fully AI-generated videos.", "section": "overview", "field": "description"},
                {"sentence": "It focuses on the participants faces and by utilizing only the vision stream of the video (not the audio) determines whether a person\u2019s face has been replaced or manipulated within the video.", "section": "overview", "field": "description"},
                {"sentence": "Detection of face-swap or face-reenactment manipulations in a video.", "section": "use", "field": "use_cases"},
                {"sentence": "Input: Video\n\nOutput: Score in range \\[0,1\\] indicating whether the video has been manipulated or not", "section": "use", "field": "inputs_outputs"},
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
                {"sentence": "2026-03-20", "section": "overview", "field": "date"},
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
            "ground_truth": [],
        },
        {
            "question": "Who should I email about it?",
            "ground_truth": [
                {"sentence": "Stelios Mylonas: [smylonas@iti.gr](mailto:smylonas@iti.gr)", "section": "overview", "field": "contact"},
            ],
        },
        {
            "question": "What Python packages do I need?",
            "ground_truth": [],
        },
        {
            "question": "What GPU do I need to run it?",
            "ground_truth": [],
        },
        {
            "question": "What does the model take as input, and what does it return?",
            "ground_truth": [
                {"sentence": "Input: Video\n\nOutput: Score in range \\[0,1\\] indicating whether the video has been manipulated or not", "section": "use", "field": "inputs_outputs"},
            ],
        },
        {
            "question": "How do I load and run the model on data?",
            "ground_truth": [
                {"sentence": "Input: Video\n\nOutput: Score in range \\[0,1\\] indicating whether the video has been manipulated or not", "section": "use", "field": "inputs_outputs"},
            ],
        },
        {
            "question": "What could make its performance worse?",
            "ground_truth": [
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
                {"sentence": "The Video FaceSwap detector is not future-proof and it may have low accuracy on new face manipulation methods without fine-tuning.", "section": "safety", "field": "caveats"},
            ],
        },
        {
            "question": "What should this model not be used for?",
            "ground_truth": [
                {"sentence": "Unsupervised decision making, Detection of AI-generated videos", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "Who is this model for?",
            "ground_truth": [
                {"sentence": "Researchers, media professionals, fact-checkers", "section": "use", "field": "user_groups"},
            ],
        },
        {
            "question": "Does a human need to review the outputs?",
            "ground_truth": [
                {"sentence": "human-in-the-loop", "section": "use", "field": "oversight"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Unsupervised decision making, Detection of AI-generated videos", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "What does it say about its accuracy?",
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
            "ground_truth": [
                {"sentence": "AUC and AP do not need any calibration threshold", "section": "performance", "field": "thresholds"},
            ],
        },
        {
            "question": "What could go wrong if I use this model?",
            "ground_truth": [
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Risk of false positives: mislabeling authentic videos as fake could undermine trust in legitimate sources or individuals.", "section": "safety", "field": "ethics"},
                {"sentence": "The Video FaceSwap detector is not future-proof and it may have low accuracy on new face manipulation methods without fine-tuning.", "section": "safety", "field": "caveats"},
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
            ],
        },
        {
            "question": "Are there ethical concerns with using this?",
            "ground_truth": [
                {"sentence": "Risk of false positives: mislabeling authentic videos as fake could undermine trust in legitimate sources or individuals.", "section": "safety", "field": "ethics"},
                {"sentence": "It is recommended to cross-validate your results with several deepfake detectors.", "section": "safety", "field": "ethics"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
            ],
        },
        {
            "question": "How much energy does it consume?",
            "ground_truth": [
                {"sentence": "Energy consumptions depends on input size and hardware.", "section": "performance", "field": "environmental_impact"},
            ],
        },
        {
            "question": "Is it compliant with any security standard?",
            "ground_truth": [
                {"sentence": "The model does not take into account any cybersecurity standards", "section": "safety", "field": "security"},
            ],
        },
        {
            "question": "Is the model fair across subgroups?",
            "ground_truth": [
                {"sentence": "Fairness is defined as the property that the model\u2019s prediction error rates (false positives and false negatives) remain consistent across different\u00a0 demographic subgroups.", "section": "safety", "field": "fairness"},
                {"sentence": "The model was not tested for its bias across various demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "What are its known limitations?",
            "ground_truth": [
                {"sentence": "The Video FaceSwap detector is not future-proof and it may have low accuracy on new face manipulation methods without fine-tuning.", "section": "safety", "field": "caveats"},
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
                {"sentence": "The model was not tested for its bias across various demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "What datasets was it trained and evaluated on?",
            "ground_truth": [
                {"sentence": "FaceForensics++, CelebDF-v2, DFDC,\u00a0ForgeryNet", "section": "training", "field": "datasets"},
                {"sentence": "Celeb-DF-v3, DF40, DeepSpeak-v1, DeepSpeak-v2, WDF,\u00a0Deepfake-Eval-2024", "section": "evaluation", "field": "datasets"},
            ],
        },
        {
            "question": "How was the model evaluated?",
            "ground_truth": [
                {"sentence": "We present video-level AUC scores and Average Precision (AP) for each dataset.", "section": "performance", "field": "analysis"},
                {"sentence": "AUC and AP do not need any calibration threshold", "section": "performance", "field": "thresholds"},
                {"sentence": "For Celeb-DF-v3 and DF40, the scores presented are averaged across the different manipulation methods.", "section": "performance", "field": "methodology"},
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
                {"sentence": "Video Classification", "section": "overview", "field": "task"},
                {"sentence": "This model is designed for Video Deepfake Detection tasks, specialized in detecting\u00a0face-swap and face-reenactment manipulations, not fully AI-generated videos.", "section": "overview", "field": "description"},
                {"sentence": "Detection of face-swap or face-reenactment manipulations in a video.", "section": "use", "field": "use_cases"},
            ],
        },
        {
            "question": "When was the model released and what version is it?",
            "ground_truth": [
                {"sentence": "2026-03-20", "section": "overview", "field": "date"},
                {"sentence": "1.0", "section": "overview", "field": "version"},
            ],
        },
        {
            "question": "What hardware and software do I need to run this model?",
            "ground_truth": [],
        },
        {
            "question": "What are the risks and ethical concerns of using this model?",
            "ground_truth": [
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Risk of false positives: mislabeling authentic videos as fake could undermine trust in legitimate sources or individuals.", "section": "safety", "field": "ethics"},
                {"sentence": "It is recommended to cross-validate your results with several deepfake detectors.", "section": "safety", "field": "ethics"},
            ],
        },
        {
            "question": "What is the energy consumption and environmental impact?",
            "ground_truth": [
                {"sentence": "Energy consumptions depends on input size and hardware.", "section": "performance", "field": "environmental_impact"},
            ],
        },
        {
            "question": "Who are the intended users and what oversight is required?",
            "ground_truth": [
                {"sentence": "Researchers, media professionals, fact-checkers", "section": "use", "field": "user_groups"},
                {"sentence": "human-in-the-loop", "section": "use", "field": "oversight"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
            ],
        },
        {
            "question": "What are the caveats and out-of-scope uses?",
            "ground_truth": [
                {"sentence": "The Video FaceSwap detector is not future-proof and it may have low accuracy on new face manipulation methods without fine-tuning.", "section": "safety", "field": "caveats"},
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
                {"sentence": "The model was not tested for its bias across various demographic groups.", "section": "performance", "field": "bias"},
                {"sentence": "Unsupervised decision making, Detection of AI-generated videos", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "How was the model trained and evaluated?",
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
            "question": "What are the input/output formats, and how do I run the model?",
            "ground_truth": [
                {"sentence": "Input: Video\n\nOutput: Score in range \\[0,1\\] indicating whether the video has been manipulated or not", "section": "use", "field": "inputs_outputs"},
            ],
        },
        {
            "question": "What technical or ethical standards does the model follow?",
            "ground_truth": [
                {"sentence": "IEEE", "section": "training", "field": "standards"},
                {"sentence": "IEEE", "section": "evaluation", "field": "standards"},
                {"sentence": "Risk of false positives: mislabeling authentic videos as fake could undermine trust in legitimate sources or individuals.", "section": "safety", "field": "ethics"},
                {"sentence": "It is recommended to cross-validate your results with several deepfake detectors.", "section": "safety", "field": "ethics"},
            ],
        },
        {
            "question": "What factors could degrade performance, and what are the known caveats?",
            "ground_truth": [
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
                {"sentence": "The Video FaceSwap detector is not future-proof and it may have low accuracy on new face manipulation methods without fine-tuning.", "section": "safety", "field": "caveats"},
                {"sentence": "The model was not tested for its bias across various demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "How do I install the software, and what hardware does it need?",
            "ground_truth": [],
        },
        {
            "question": "Who should use this model, and what should they not do with it?",
            "ground_truth": [
                {"sentence": "Researchers, media professionals, fact-checkers", "section": "use", "field": "user_groups"},
                {"sentence": "Detection of face-swap or face-reenactment manipulations in a video.", "section": "use", "field": "use_cases"},
                {"sentence": "Unsupervised decision making, Detection of AI-generated videos", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "What is the model's license and how do I cite it?",
            "ground_truth": [
                {"sentence": "Apache-2.0", "section": "overview", "field": "license"},
            ],
        },
    ],

    "negative": [
        {
            "question": "What is the CO₂ emissions footprint of training?",
            "ground_truth": [
                {"sentence": "Energy consumptions depends on input size and hardware.", "section": "performance", "field": "environmental_impact"},
            ],
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
                {"sentence": "The model was not tested for its bias across various demographic groups.", "section": "performance", "field": "bias"},
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
                {"sentence": "Stelios Mylonas: [smylonas@iti.gr](mailto:smylonas@iti.gr)", "section": "overview", "field": "contact"},
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
            "ground_truth": [],
        },
        {
            "question": "What data privacy measures are in place?",
            "ground_truth": [],
        },
        {
            "question": "Is the model explainable / interpretable?",
            "ground_truth": [],
        },
        {
            "question": "Does the model handle audio / video modalities (if not applicable)?",
            "ground_truth": [
                {"sentence": "This model is designed for Video Deepfake Detection tasks, specialized in detecting\u00a0face-swap and face-reenactment manipulations, not fully AI-generated videos.", "section": "overview", "field": "description"},
                {"sentence": "It focuses on the participants faces and by utilizing only the vision stream of the video (not the audio) determines whether a person\u2019s face has been replaced or manipulated within the video.", "section": "overview", "field": "description"},
                {"sentence": "Input: Video\n\nOutput: Score in range \\[0,1\\] indicating whether the video has been manipulated or not", "section": "use", "field": "inputs_outputs"},
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
                {"sentence": "Risk of false positives: mislabeling authentic videos as fake could undermine trust in legitimate sources or individuals.", "section": "safety", "field": "ethics"},
                {"sentence": "It is recommended to cross-validate your results with several deepfake detectors.", "section": "safety", "field": "ethics"},
                {"sentence": "The model does not take into account any cybersecurity standards", "section": "safety", "field": "security"},
                {"sentence": "The Video FaceSwap detector is not future-proof and it may have low accuracy on new face manipulation methods without fine-tuning.", "section": "safety", "field": "caveats"},
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
                {"sentence": "The model was not tested for its bias across various demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "What are the limitations of this model?",
            "ground_truth": [
                {"sentence": "The Video FaceSwap detector is not future-proof and it may have low accuracy on new face manipulation methods without fine-tuning.", "section": "safety", "field": "caveats"},
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
                {"sentence": "The model was not tested for its bias across various demographic groups.", "section": "performance", "field": "bias"},
                {"sentence": "The model does not take into account any cybersecurity standards", "section": "safety", "field": "security"},
            ],
        },
        {
            "question": "Is this model accurate?",
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
            "question": "Is this model good?",
            "ground_truth": [
                {"sentence": "We present video-level AUC scores and Average Precision (AP) for each dataset.", "section": "performance", "field": "analysis"},
                {"sentence": "*   Celeb-DF-v3:\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a086.7\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 89.9", "section": "performance", "field": "metrics"},
                {"sentence": "*   DF40:\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a087.6\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 95.1\u00a0\u00a0", "section": "performance", "field": "metrics"},
                {"sentence": "*   DeepSpeak-v1:\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 91.5\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 93.4", "section": "performance", "field": "metrics"},
                {"sentence": "*   DeepSpeak-v2:\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 77.5\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 77.4", "section": "performance", "field": "metrics"},
                {"sentence": "*   WDF:\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 94.9\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 93.6", "section": "performance", "field": "metrics"},
                {"sentence": "*   DeepFake-Eval-2024:\u00a0 62.8\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 92.8", "section": "performance", "field": "metrics"},
            ],
        },
        {
            "question": "How does this model work?",
            "ground_truth": [
                {"sentence": "This model is designed for Video Deepfake Detection tasks, specialized in detecting\u00a0face-swap and face-reenactment manipulations, not fully AI-generated videos.", "section": "overview", "field": "description"},
                {"sentence": "It focuses on the participants faces and by utilizing only the vision stream of the video (not the audio) determines whether a person\u2019s face has been replaced or manipulated within the video.", "section": "overview", "field": "description"},
                {"sentence": "Input: Video\n\nOutput: Score in range \\[0,1\\] indicating whether the video has been manipulated or not", "section": "use", "field": "inputs_outputs"},
                {"sentence": "\\- Face detection  \n\\- Enlarge faces by a factor of 1.3  \n\\- Crop faces and resize to 224x224  \n\\- Data augmentation during training (random resized crop, random flipping, color jittering, cutout)", "section": "training", "field": "preprocessing"},
                {"sentence": "\\- Sample the video at 1 FPS\n\n\\- Face detection\n\n\\- Enlarge faces by a factor of 1.3\n\n\\- Crop faces and resize to 224x224", "section": "evaluation", "field": "preprocessing"},
            ],
        },
        {
            "question": "Is this model trustworthy?",
            "ground_truth": [
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Risk of false positives: mislabeling authentic videos as fake could undermine trust in legitimate sources or individuals.", "section": "safety", "field": "ethics"},
                {"sentence": "It is recommended to cross-validate your results with several deepfake detectors.", "section": "safety", "field": "ethics"},
                {"sentence": "The Video FaceSwap detector is not future-proof and it may have low accuracy on new face manipulation methods without fine-tuning.", "section": "safety", "field": "caveats"},
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
                {"sentence": "The model does not take into account any cybersecurity standards", "section": "safety", "field": "security"},
                {"sentence": "The model was not tested for its bias across various demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "What is this model's main contribution?",
            "ground_truth": [
                {"sentence": "This model is designed for Video Deepfake Detection tasks, specialized in detecting\u00a0face-swap and face-reenactment manipulations, not fully AI-generated videos.", "section": "overview", "field": "description"},
                {"sentence": "It focuses on the participants faces and by utilizing only the vision stream of the video (not the audio) determines whether a person\u2019s face has been replaced or manipulated within the video.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "Is this model reliable?",
            "ground_truth": [
                {"sentence": "The Video FaceSwap detector is not future-proof and it may have low accuracy on new face manipulation methods without fine-tuning.", "section": "safety", "field": "caveats"},
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
            ],
        },
        {
            "question": "What makes this model novel?",
            "ground_truth": [
                {"sentence": "This model is designed for Video Deepfake Detection tasks, specialized in detecting\u00a0face-swap and face-reenactment manipulations, not fully AI-generated videos.", "section": "overview", "field": "description"},
                {"sentence": "It focuses on the participants faces and by utilizing only the vision stream of the video (not the audio) determines whether a person\u2019s face has been replaced or manipulated within the video.", "section": "overview", "field": "description"},
            ],
        },
        {
            "question": "Is this model ready for production?",
            "ground_truth": [
                {"sentence": "The Video FaceSwap detector is not future-proof and it may have low accuracy on new face manipulation methods without fine-tuning.", "section": "safety", "field": "caveats"},
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "The model was not tested for its bias across various demographic groups.", "section": "performance", "field": "bias"},
            ],
        },
        {
            "question": "Is this model eco-friendly?",
            "ground_truth": [
                {"sentence": "Energy consumptions depends on input size and hardware.", "section": "performance", "field": "environmental_impact"},
            ],
        },
        {
            "question": "How do I use this model?",
            "ground_truth": [
                {"sentence": "Input: Video\n\nOutput: Score in range \\[0,1\\] indicating whether the video has been manipulated or not", "section": "use", "field": "inputs_outputs"},
            ],
        },
        {
            "question": "What should I know before using this model?",
            "ground_truth": [
                {"sentence": "The Video FaceSwap detector is not future-proof and it may have low accuracy on new face manipulation methods without fine-tuning.", "section": "safety", "field": "caveats"},
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
                {"sentence": "Over-reliance on automated detection without human oversight could lead to unfair consequences in sensitive domains (e.g., journalism, legal evidence).", "section": "safety", "field": "risks"},
                {"sentence": "Risk of false positives: mislabeling authentic videos as fake could undermine trust in legitimate sources or individuals.", "section": "safety", "field": "ethics"},
                {"sentence": "It is recommended to cross-validate your results with several deepfake detectors.", "section": "safety", "field": "ethics"},
                {"sentence": "The model was not tested for its bias across various demographic groups.", "section": "performance", "field": "bias"},
                {"sentence": "Unsupervised decision making, Detection of AI-generated videos", "section": "use", "field": "out_of_scope_use"},
            ],
        },
        {
            "question": "Can I use this model commercially?",
            "ground_truth": [
                {"sentence": "Apache-2.0", "section": "overview", "field": "license"},
            ],
        },
        {
            "question": "What are the main takeaways about this model?",
            "ground_truth": [
                {"sentence": "This model is designed for Video Deepfake Detection tasks, specialized in detecting\u00a0face-swap and face-reenactment manipulations, not fully AI-generated videos.", "section": "overview", "field": "description"},
                {"sentence": "It focuses on the participants faces and by utilizing only the vision stream of the video (not the audio) determines whether a person\u2019s face has been replaced or manipulated within the video.", "section": "overview", "field": "description"},
                {"sentence": "We present video-level AUC scores and Average Precision (AP) for each dataset.", "section": "performance", "field": "analysis"},
                {"sentence": "The Video FaceSwap detector is not future-proof and it may have low accuracy on new face manipulation methods without fine-tuning.", "section": "safety", "field": "caveats"},
                {"sentence": "May present low accuracy on low resolution videos or videos with blurred and very small faces.", "section": "use", "field": "factors"},
            ],
        },
    ],
}