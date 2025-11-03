import clip
import torch
from PIL import Image
from aicard.utils.image_converters import to_bytes
from io import BytesIO

class ImageClassifier:
    def __init__(self, device="cpu"):
        self.device = device
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        self.labels = None
        self.values = None
        self.is_ready = False

        self._build_embeddings()


    def _build_embeddings(self):
        embeddings = {
            "logo":
                {
                    "logo": "The logo of company or model."
                },
            "symbol":
                {
                    "symbol": "A symbol."
                },
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

    def classify_images(self, content):
        images = []
        are_classified = []
        for img in content:
            img_bytes, status_code = to_bytes(img)
            if status_code == 200:
                images.append(self.preprocess(Image.open(BytesIO(img_bytes))))
                are_classified.append(True)
            else:
                are_classified.append(False)
        images_tensor = torch.stack(images).to(self.device)

        with torch.no_grad():
            image_embeddings = self.model.encode_image(images_tensor)
            image_embeddings /= image_embeddings.norm(dim=-1, keepdim=True)

            similarity = image_embeddings @ self.values.T

            best_idxs = similarity.argmax(dim=1)
            best_labels = [self.labels[idx] for idx in best_idxs]
            best_scores = similarity[range(len(images)), best_idxs]
            best_scores.tolist()

            labels_out = []
            scores_out = []
            i = 0
            for is_classified in are_classified:
                if is_classified:
                    labels_out += [best_labels[i]]
                    scores_out += [best_scores[i]]
                    i += 1
                else:
                    labels_out.append(None)
                    scores_out.append(None)

        return list(zip(labels_out, scores_out))

img_classifier=ImageClassifier()
