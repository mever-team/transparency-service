from datasets import load_dataset
from huggingface_hub import dataset_info
from transformers import pipeline
import aicard as aic

dataset = load_dataset("google-research-datasets/go_emotions", split = 'test')
info = dataset_info("google-research-datasets/go_emotions")
class_names = info.card_data['dataset_info'][1]['features'][1]['sequence']['class_label']['names']
classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

def pipeline(data):
    sentences = [text for text in data['text']]
    model_outputs = classifier(sentences)
    out = []
    for sample in model_outputs:
        flat = {d['label']: d['score'] for d in sample}
        out.append([flat[name] for name in class_names.values()])
    return out

metrics = aic.evaluation.evaluate(
    data=dataset,
    pipeline=pipeline,
    task=aic.evaluation.tasks.nlp.text_classification,
    batch_size=32)

print(metrics)



