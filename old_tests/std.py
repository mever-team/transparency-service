# https://www.analyticsvidhya.com/blog/2020/01/first-text-classification-in-pytorch/
# deal with tensors
# https://peerj.com/articles/cs-518/
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import transparency


def custom_tokenizer(data):
    input_str = "<title>" + data["title"] + "<content>" + data["content"] + "<end>"
    tokenizer = AutoTokenizer.from_pretrained("hamzab/roberta-fake-news-classification")
    return tokenizer.encode_plus(
        input_str,
        max_length=512,
        padding="max_length",
        truncation=True,
        return_tensors="pt",
    )


class customodel(torch.nn.Module):
    def __init__(self, model_name="hamzab/roberta-fake-news-classification"):
        super(customodel, self).__init__()
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

    def forward(self, input_ids):
        # create a forward method to handle batch input for this model
        # input_ids is the output of custom_tokenizer() handled internally in the sdk
        logits = []
        for encoding, mask in zip(input_ids["input_ids"], input_ids["attention_mask"]):
            output = self.model(encoding, attention_mask=mask)
            logits.append(output.logits)
        return torch.stack(
            [logit[:, 0] for logit in logits]
        )  # logit[:, 1] 'Fake' logit[:,0] 'Real'


device = "cuda"
model = customodel()
mc = transparency.model_card_generator.ModelCard()
transparency.evaluation.std.evaluate(
    model, custom_tokenizer, device=device, model_card=mc
)

# mc.save()
