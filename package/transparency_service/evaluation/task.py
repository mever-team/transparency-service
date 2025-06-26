import numpy as np
import torch
from typing import List
from transparency_service.evaluation import params
from transparency_service.evaluation import metrics

class Task:
    def __init__(self, name: str, targets:list[str], metrics: list, parameters, toinstance):
        self.name = name
        self.targets = targets
        self.metrics = metrics
        self.parameters = parameters
        self.toinstance = toinstance

class targets:
    text = ["solution","answer","output","response","conversations","inferences","messages","texts","caption",]
    image = ["image","url"]
    video = ["video","url","video_path","video_file",]
    classes = ["label","class_name","ground_truth","emotion",]
    depth = ["depth"]
    mask = ["mask"]
    imgfeatextr = []
    keypoint = []
    featextr = []
    segmentation = {
        "target": ["seg"],
        "label": ["cat", "label"],  # candidate names for target. Must be a set of those
        "obj": ["objects"],
    }
    objdetect = {
        "target": ["box"],
        "label": ["cat", "label"],
        "obj": ["objects"],
    }

######## MULTIMODAL

audio_text_to_text = Task(
    "Audio-Text to Text",
    targets=targets.text,
    metrics=[metrics.wer, metrics.cer], # TODO: blue, rouge
    parameters=params.unknown,          # TODO: WAS NOT CLEAR
    toinstance=([str], lambda x: isinstance(x, str)),
)
image_text_to_text = Task(
    "Audio-Text to Text",
    targets=targets.text,
    metrics=[],                         # TODO: blue, rouge, meteor, cider, spice
    parameters=params.unknown,          # TODO: WAS NOT CLEAR
    toinstance=([str], lambda x: isinstance(x, str)),
)
visual_question_answering = Task(
    "Visual Question Answering",
    targets=targets.text,
    metrics=[metrics.f1_macro, metrics.f1_micro], # TODO: Exact Match (EM), blue, meteor, VQA Accuracy
    parameters=params.classification,             # TODO: WAS NOT CLEAR
    toinstance=([str], lambda x: isinstance(x, str)),
)
document_question_answering = Task(
    "Document Question Answering",
    targets=targets.text,
    metrics=[metrics.f1_macro, metrics.f1_micro], # TODO: Exact Match (EM), blue, meteor
    parameters=params.classification,             # TODO: WAS NOT CLEAR
    toinstance=([str], lambda x: isinstance(x, str)),
)
video_text_to_text = Task(
    "Video-Text to Text",
    targets=targets.text,
    metrics=[],                         # TODO: blue, rouge, meteor, CIDEr, spice
    parameters=params.classification,   # TODO: WAS NOT CLEAR
    toinstance=([str], lambda x: isinstance(x, str)),
)

######## COMPUTER VISION

depth_estimation = Task(
    "Depth Estimation",
    targets=targets.depth,
    metrics=[metrics.mae, metrics.rmse, metrics.ssim, metrics],  # TODO: sirmse (Scale-Invariant rmse)
    parameters=params.classification,                            # TODO: WAS NOT CLEAR
    toinstance=([np.ndarray], lambda x: isinstance(x, np.ndarray)),
)

image_segmentation = Task(
    "Image Segmentation",
    targets=targets.segmentation, # special value
    metrics=[metrics.IoU, metrics.map, metrics.dice_macro, metrics.dice_micro], # TODO: pixel acc
    parameters=params.image_segmentation,
    toinstance=([np.ndarray], lambda x: isinstance(x, np.ndarray)),
)

object_detection = Task(
    "Object Detection",
    targets=targets.objdetect, # special value
    metrics=[metrics.map, metrics.IoU, metrics.precision_macro, metrics.precision_micro, metrics.f1_macro, metrics.f1_micro],
    parameters=params.object_detection,
    toinstance=(
            [dict[str, torch.Tensor], list[list[int]], list[int], list[float]],
            lambda x: (
                isinstance(x, list)
                and len(x) == 3
                and isinstance(x[0], list)
                and all(
                    isinstance(sublist, list)
                    and len(sublist) == 4
                    and all(isinstance(i, int) for i in sublist)
                    for sublist in x[0]
                )
                and isinstance(x[1], list)
                and all(isinstance(i, int) for i in x[1])
                and isinstance(x[2], list)
                and all(isinstance(f, float) for f in x[2])
            )
            or (
                isinstance(x, dict)
                and "scores" in x
                and isinstance(x["scores"], torch.Tensor)
                and "labels" in x
                and isinstance(x["labels"], torch.Tensor)
                and "boxes" in x
                and isinstance(x["boxes"], torch.Tensor)
            ),
        ),  # box, cat_id, score,
)

image_classification = Task(
    "Image Classification",
    targets=targets.classes,
    metrics=[metrics.precision_macro, metrics.precision_micro, metrics.recall_macro, metrics.recall_micro,
             metrics.f1_macro, metrics.f1_micro, metrics.auc_roc_macro, metrics.auc_roc_macro],  # TODO: acc
    parameters=params.classification,
    toinstance=(
            [torch.Tensor, int, float, list[float], str, dict[str, float]],
            lambda x: (
                isinstance(x, (torch.Tensor, int, float, str))
                or (isinstance(x, list) and all(isinstance(i, float) for i in x))
                or (
                    isinstance(x, dict)
                    and all(
                        isinstance(k, str) and isinstance(v, float)
                        for k, v in x.items()
                    )
                )
            ),
        ),
)

text_to_image = Task(
    "Text to Image",
    targets=targets.image,
    metrics=[metrics.ssim], # TODO: Inception Score (IS), Fréchet Inception Distance (fid), CLIPScore
    parameters=params.image_segmentation,  # TODO: WAS NOT CLEAR - I PUT ONE AT RANDOM (Manios)
    toinstance= ([np.ndarray], lambda x: isinstance(x, np.ndarray)),
)

image_to_text = Task(
    "Image to Text",
    targets=targets.text,
    metrics=[],  # TODO: blue, rouge, meteor, CIDEr, spice
    parameters=params.classification,  # TODO: WAS NOT CLEAR
    toinstance=([str], lambda x: isinstance(x, str)),
)

image_to_image = Task(
    "Image to Image",
    targets=targets.image,
    metrics=[metrics.ssim, metrics.psnr],  # TODO: lpips (Perceptual Loss)
    parameters=params.image_segmentation,  # TODO: WAS NOT CLEAR - I PUT ONE AT RANDOM (Manios)
    toinstance=([np.ndarray], lambda x: isinstance(x, np.ndarray))
)

image_to_video = Task(
    "Image to Video",
    targets=targets.video,
    metrics=[metrics.ssim, metrics.psnr],  # TODO: FVD (Fréchet Video Distance)
    parameters=params.unknown,             # TODO: WAS NOT CLEAR AT ALL
    toinstance=(List[np.ndarray],lambda x: isinstance(x, list) and all(isinstance(t, np.ndarray) for t in x),),
)

video_classification = Task(
    "Video Classification",
    targets=targets.classes,
    metrics=[metrics.precision_macro, metrics.precision_micro, metrics.recall_macro, metrics.recall_micro,
             metrics.f1_macro, metrics.f1_micro, metrics.auc_roc_macro, metrics.auc_roc_macro],  # TODO: acc
    parameters=params.classification,
    toinstance=(
        [torch.Tensor, int, float, List[float], str, dict[str, float]],
        lambda x: (
            isinstance(x, (torch.Tensor, int, float, str))
            or (isinstance(x, list) and all(isinstance(i, float) for i in x))
            or (
                isinstance(x, dict)
                and all(
                    isinstance(k, str) and isinstance(v, float)
                    for k, v in x.items()
                )
            )
        ),
    ),
)

text_to_video = Task(
    "Text to Video",
    targets=targets.video,
    metrics=[metrics.ssim],     # TODO: FVD, IS, Fid
    parameters=params.unknown,  # TODO: WAS NOT CLEAR
    toinstance=(List[np.ndarray],lambda x: isinstance(x, list) and all(isinstance(t, np.ndarray) for t in x),),
)

mask_generation = Task(
    "Text to Video",
    targets=targets.mask,
    metrics=[metrics.IoU, metrics.dice_macro, metrics.dice_micro], # TODO: Pixel Accuracy
    parameters=params.unknown,  # TODO: WAS NOT CLEAR
    toinstance=([np.ndarray], lambda x: isinstance(x, np.ndarray)),
)

image_feature_extraction = Task(
    "Image Feature Extraction",
    targets=targets.imgfeatextr,
    metrics=[], # TODO: Cosine Similarity,Euclidean Distance,lpips
    parameters=params.unknown,  # TODO: WAS NOT CLEAR
    toinstance=([np.ndarray], lambda x: isinstance(x, np.ndarray)),
)



tasks2metrics = {
    "Keypoint Detection": ["PCK","NME","MSE"],  # Percentage of Correct Keypoints (PCK), Normalized Mean Error (NME), Mean Squared Error (MSE)
    # Natural Language Processing
    "Text Classification": ["precision", "recall", "f1", "acc", "roc-auc"],
    "Question Answering": ["EM",],  # Exact Match (EM), f1 # 'f1'
    "Translation": ["blue", "meteor", "rouge", "chrF++"],
    "Summarization": ["rouge", "blue", "meteor", "BERTScore"],
    "Feature Extraction": ["Cosine Similarity","Euclidean Distance","Pearson Correlation"],
    "Text Generation": ["blue", "rouge", "meteor", "BERTScore", "Perplexity"],
    "Text2Text Generation": ["blue", "rouge", "meteor", "BERTScore", "chrF++"],
}

def tasks2instance():
    "Keypoint Detection": (
        List[Tuple[int, int]],
        lambda x: isinstance(x, list)
        and all(
            isinstance(t, tuple)
            and len(t) == 2
            and isinstance(t[0], int)
            and isinstance(t[1], int)
            for t in x
        ),
    ),
    # Natural Language Processing
    "Text Classification": (
        [torch.Tensor, int, float, List[float], str, dict[str, float]],
        lambda x: (
            isinstance(x, (torch.Tensor, int, float, str))
            or (isinstance(x, list) and all(isinstance(i, float) for i in x))
            or (
                isinstance(x, dict)
                and all(
                    isinstance(k, str) and isinstance(v, float)
                    for k, v in x.items()
                )
            )
        ),
    ),
    "Question Answering": ([str], lambda x: isinstance(x, str)),
    "Translation": ([str], lambda x: isinstance(x, str)),
    "Summarization": ([str], lambda x: isinstance(x, str)),
    "Feature Extraction": ([np.ndarray], lambda x: isinstance(x, np.ndarray)),
    "Text Generation": ([str], lambda x: isinstance(x, str)),
    "Text2Text Generation": ([str], lambda x: isinstance(x, str)),


def tasks2targets():
    "Keypoint Detection": keypoint_targets,
    # Natural Language Processing
    "Text Classification": class_targets,
    "Question Answering": text_targets,
    "Translation": text_targets,
    "Summarization": text_targets,
    "Feature Extraction": featextr_targets,
    "Text Generation": text_targets,
    "Text2Text Generation": text_targets,
