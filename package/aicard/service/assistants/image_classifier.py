
class ImageClassifier:
    def __init__(self, device="cpu"):
        import clip

        self.device = device
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        self.labels = None
        self.values = None
        self.is_ready = False

    def _build_embeddings(self):
        import clip
        import torch

        embeddings = {
            "model":
                {
                    "overview": "An overview of the model. The reader should have a good idea of what the model is, the purpose, novelty, capabilities, and caveats after reading this.",
                },
            "considerations": {
                "instructions": "Provide any other information which helps users use the model. Ideally, add a code snippet illustrating a typical use-case. You can also add a link to a GitHub repository with usage instructions.",
                "inputs_outputs": "Provide a short description of the model's inputs and outputs",
            },
            "training_set": {
                "datasets": "What dataset(s) were used to train the model? If possible, please add a link to details on the respective datasets used, for example a datasheet.",
            },
            "eval_set": {
                "datasets": "What dataset(s) were used to evaluate the model? If possible, please add a link to details on the respective datasets used, for example a datasheet.",
            },
            "performance": {
                "analysis": "Analyse and explain performance results of your model.",
                "metrics": "Include any performance metrics here e.g. accuracy, precision, Recall, ROC-AUC, F1-score.",
                "fairness": "How did the model perform with respect to each factor. Quantitative analyses should be disaggregated, that is, broken down by the chosen factors. Quantitative analyses should provide the results of evaluating the model according to the chosen metrics, providing confidence interval values when possible. Parity on the different metrics across disaggregated population subgroups corresponds to how fairness is often defined.",
            },
        }
        with torch.no_grad():
            for category, value in embeddings.items():
                for field, description in value.items():
                    text_tokens = clip.tokenize([description])
                    text_embeddings = self.model.encode_text(text_tokens.to(self.device))
                    embeddings[category][field] = text_embeddings / text_embeddings.norm(dim=-1, keepdim=True)
        del text_embeddings

        self.labels = []
        text_vectors = []
        for category, fields in embeddings.items():
            for field, tensor in fields.items():
                self.labels.append({category: field})
                text_vectors.append(tensor)
        del embeddings
        self.values = torch.cat(text_vectors, dim=0)
        del text_vectors
        self.is_ready = True

    def classify_images(self, image_paths: list[str]):
        from PIL import Image
        import torch

        images = [self.preprocess(Image.open(path)) for path in image_paths]
        images_tensor = torch.stack(images).to(self.device)
        with torch.no_grad():
            image_embeddings = self.model.encode_image(images_tensor)
            image_embeddings /= image_embeddings.norm(dim=-1, keepdim=True)
            similarity = image_embeddings @ self.values.T
            best_idxs = similarity.argmax(dim=1)
            best_labels = [self.labels[idx] for idx in best_idxs]
            best_scores = similarity[range(len(image_paths)), best_idxs]
        return list(zip(best_labels, best_scores.tolist()))
