import numpy as np
from transparency_service.evaluation import params
from transparency_service.evaluation import metrics
from transparency_service.evaluation.task import Task, targets

question_answering = Task(
    "Question Answering",
    targets=targets.text,
    metrics=[metrics.f1_macro, metrics.f1_micro],  # TODO: Exact Match (EM)
    parameters=params.unknown,  # TODO: WAS NOT CLEAR
    toinstance=([str], lambda x: isinstance(x, str)),
)

translation = Task(
    "Translation",
    targets=targets.text,
    metrics=[],  # TODO: blue, meteor, rouge, chrF++
    parameters=params.unknown,   # TODO: WAS NOT CLEAR
    toinstance=([str], lambda x: isinstance(x, str)),
)

summarization = Task(
    "Summarization",
    targets=targets.text,
    metrics=[],  # TODO: blue, meteor, rouge, BERTScore
    parameters=params.unknown,   # TODO: WAS NOT CLEAR
    toinstance=([str], lambda x: isinstance(x, str)),
)

feature_extraction = Task(
    "Translation",
    targets=targets.featextr,
    metrics=[],  # TODO: Cosine Similarity,Euclidean Distance,Pearson Correlation
    parameters=params.unknown,   # TODO: WAS NOT CLEAR
    toinstance=([np.ndarray], lambda x: isinstance(x, np.ndarray)),
)

text_generation = Task(
    "Text Generation",
    targets=targets.text,
    metrics=[],  # TODO: blue, meteor, rouge, BERTScore, Perplexity
    parameters=params.unknown,   # TODO: WAS NOT CLEAR
    toinstance=([str], lambda x: isinstance(x, str)),
)

text_to_text_generation = Task(
    "Text to Text Generation",
    targets=targets.text,
    metrics=[],  # TODO: blue, meteor, rouge, BERTScore, chrF++"
    parameters=params.unknown,   # TODO: WAS NOT CLEAR
    toinstance=([str], lambda x: isinstance(x, str)),
)
