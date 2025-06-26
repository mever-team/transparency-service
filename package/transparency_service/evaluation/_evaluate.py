import os
import pandas as pd
import csv
import sys
import yaml
import numpy as np
from typing import List, Tuple
from .metrics import compute
import torch
import warnings
import validators
import requests
from PIL import Image
import datasets
from io import BytesIO


def is_path(s):
    if isinstance(s, str):
        if os.path.exists(os.path.expanduser(s)):
            return True
    return False


def get_supported_types():
    return [
        ".csv",
        ".tsv",
        ".json",
        ".jsonl",
        ".xml",
        ".yml",
        ".yaml",
        ".parquet",
        ".feather",
        ".pickle",
        ".html",
    ]


def get_supported_image_types():
    return [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".tiff",
        ".tif",
    ]


def determine_type(path):
    _, extension = os.path.splitext(path)
    return extension


def xyxy2xywh(xyxy):
    x_min, y_min, x_max, y_max = xyxy
    w = x_max - x_min
    h = y_max - y_min
    return x_min, y_min, w, h


def xywh2xyxy(xywh):
    x_min, y_min, w, h = xywh
    x_max = x_min + w
    y_max = y_min + h
    return x_min, y_min, x_max, y_max


def determin_xyxy_or_xywh(bbox, img_w, img_h):
    x_min, y_min, curious1, curious2 = xyxy2xywh(bbox)
    if curious1 < 0 or curious2 < 0:
        return "xywh"
    x_min, y_min, curious1, curious2 = xywh2xyxy(bbox)
    if curious1 > img_w or curious2 > img_h:
        return "xyxy"
    return None
    # warnings.warn("Warning: Can't determine bbox format. Assuming xyxy. Consider using the box_format option")


def read_data_pd(path, delimiter=None, names=None, split=None):
    supported_types = get_supported_types()
    t = determine_type(path)
    if t == supported_types[0]:  # .csv
        csv.field_size_limit(sys.maxsize)
        data = (
            pd.read_csv(path, names=names, engine="python")
            if delimiter is None
            else pd.read_csv(path, delimiter=delimiter, names=names, engine="python")
        )
    elif t == supported_types[1]:  # .tsb
        csv.field_size_limit(sys.maxsize)
        data = pd.read_csv(path, delimiter=delimiter, names=names, engine="python")
    elif t == supported_types[2]:  # .json
        data = pd.read_json(path)
    elif t == supported_types[3]:  # .jsonl
        data = pd.read_json(path, lines=True)
    elif t == supported_types[4]:  # .xml
        data = pd.read_xml(path)
    elif t == supported_types[5] or t == supported_types[6]:  # .yml .yaml
        with open(path, "r") as file:
            yaml_data = yaml.safe_load(file)
        data = pd.DataFrame(yaml_data)
    elif t == supported_types[7]:  # .parquet
        data = pd.read_parquet(path)
    elif t == supported_types[8]:  # .feather
        data = pd.read_feather(path)
    elif t == supported_types[9]:  # .pickle
        data = pd.read_pickle(path)
    elif t == supported_types[10]:  # .html
        data = pd.read_html(path)[0]
    else:  # not supported file types
        raise ValueError(f"read_data_structure: Type of {t} is not supported")

    return data


def read_data(path, delimiter=None, names=None, split=None):
    data = read_data_pd(path, delimiter=None, names=None, split=None)
    return datasets.Dataset.from_pandas(data)


def calc_metrics(
    data, preds, target_column, task, num_classes_model, anns, device=None
):
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    if "class" in task.lower():  # all classification cases
        target = []
        for batch in data:  # flatten the batch data[target_column]
            target.extend(batch[target_column])
        if isinstance(target[0], int):
            num_classes = (
                num_classes_model if num_classes_model is not None else len(set(target))
            )
            if num_classes < 2:
                raise ValueError(
                    f"found only {num_classes} classes in the dataset. Can't calculate metrics"
                )
            elif num_classes == 2:
                class_task = "binary"
            else:
                class_task = "multiclass"
        elif isinstance(target[0], list):
            class_task = "multilabel"
            if num_classes_model is not None:
                num_classes = num_classes_model
            else:
                classes = set()
                for sample in target:
                    classes = classes | set(sample)
                num_classes = len(classes)
            for t in target:  # correct the format
                if len(t) != num_classes:
                    for i in range(len(target)):
                        reconstruct = [0] * num_classes
                        for cl in target[i]:
                            reconstruct[cl] = 1
                        target[i] = reconstruct
                    break
        args = torch.tensor(preds).to(device), torch.tensor(target).to(device)
        args = *args, class_task, num_classes

    elif task == "Object Detection":
        anns_source = data if len(anns.features) == 0 else anns
        if len(target_column) == 2:
            bbox_column, label_column = target_column
        else:
            obj_column, bbox_column, label_column = target_column
        iou_type = "bbox"
        img_column = None
        src_type = None

        for key in data.column_names:  # search for the images as path or web
            if is_path(data[key][0][0]):
                if determine_type(data[key][0][0]) in get_supported_image_types():
                    img_column = key
                    src_type = "path"
            elif validators.url(data[key][0][0]):
                image_formats = [
                    "image/" + t.replace(".", "") for t in get_supported_image_types()
                ]
                r = requests.head(data[key][0][0])
                if r.headers["content-type"] in image_formats:
                    img_column = key
                    src_type = "url"

        box_format = None
        if src_type == "path":  # we can found the images
            for batch in data:
                for img, bboxes in zip(batch[img_column], batch[bbox_column]):
                    image = Image.open(img)
                    width, height = image.size
                    for bbox in bboxes:
                        box_format = determin_xyxy_or_xywh(bbox, width, height)
                        if box_format is not None:
                            break
                    if box_format is not None:
                        break
                if box_format is not None:
                    break
        elif src_type == "url":
            for batch in zip(data, anns_source):
                for img, bboxes in zip(batch[0][img_column], batch[1][bbox_column]):
                    image = Image.open(BytesIO(requests.get(img).content))
                    width, height = image.size
                    for bbox in bboxes:
                        box_format = determin_xyxy_or_xywh(bbox, width, height)
                        if box_format is not None:
                            break
                    if box_format is not None:
                        break
                if box_format is not None:
                    break
        if box_format is None:
            warnings.warn(
                "Warning: can't determine box_format. Setting box_format = 'xyxy'. Consider using the box_format option"
            )
            box_format = "xyxy"

        preds_ready = []
        if not isinstance(preds[0], dict):
            for pred in preds:
                boxes, cat_ids, scores = pred
                preds_ready.append(
                    {
                        "boxes": torch.tensor(boxes).to(device),
                        "labels": torch.tensor(cat_ids).to(device),
                        "scores": torch.tensor(scores).to(device),
                    }
                )
        else:
            preds_ready = preds
            for pred_ready in preds_ready:
                for key in pred_ready:
                    pred_ready[key] = pred_ready[key].to(device)
        target_ready = []
        if len(target_column) == 2:
            # bbox, label = target
            # assuming batch[bbox_column] and batch[label_column] are list or tuple
            for batch in anns_source:
                for boxes_target, cat_ids_target in zip(
                    batch[bbox_column], batch[label_column]
                ):
                    if (boxes_target is not None) and (
                        cat_ids_target is not None
                    ):  # prevent reading None values that the convertion to datasets creates
                        target_ready.append(
                            {
                                "boxes": torch.tensor(boxes_target).to(device),
                                "labels": torch.tensor(cat_ids_target).to(device),
                            }
                        )
        else:
            # obj, bbox, label = target
            if isinstance(anns_source[0][obj_column], dict):
                for batch in anns_source:
                    for boxes_target, cat_ids_target in zip(
                        batch[obj_column][bbox_column], batch[obj_column][label_column]
                    ):
                        if (boxes_target is not None) and (
                            cat_ids_target is not None
                        ):  # prevent reading None values that the convertion to datasets creates
                            target_ready.append(
                                {
                                    "boxes": torch.tensor(boxes_target).to(device),
                                    "labels": torch.tensor(cat_ids_target).to(device),
                                }
                            )
            else:  # elif isinstance(data[obj], list)
                for batch in anns_source:
                    for object in batch[obj_column]:
                        if (object[bbox_column] is not None) and (
                            object[label_column] is not None
                        ):  # prevent reading None values that the convertion to datasets creates
                            target_ready.append(
                                {
                                    "boxes": torch.tensor(object[bbox_column]).to(
                                        device
                                    ),
                                    "labels": torch.tensor(object[label_column]).to(
                                        device
                                    ),
                                }
                            )

        args = preds_ready, target_ready, iou_type, box_format
    elif task == "Image Segmentation":
        iou_type = "segm"

    metrics_to_calc = tasks2metrics()[task]
    out = {}
    for m in metrics_to_calc:
        metr = compute()[m](*args, device)
        out = out | metr
    return out


def tasks2instance():
    return {
        # Multimodal
        "Audio - Text - to - Text": ([str], lambda x: isinstance(x, str)),
        "Image - Text - to - Text": ([str], lambda x: isinstance(x, str)),
        "Visual Question Answering": ([str], lambda x: isinstance(x, str)),
        "Document Question Answering": ([str], lambda x: isinstance(x, str)),
        "Video - Text - to - Text": ([str], lambda x: isinstance(x, str)),
        # Computer Vision
        "Depth Estimation": ([np.ndarray], lambda x: isinstance(x, np.ndarray)),
        "Image Classification": (
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
        "Object Detection": (
            [dict[str, torch.Tensor], List[List[int]], List[int], List[float]],
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
        ),  # box, cat_id, score
        "Image Segmentation": ([np.ndarray], lambda x: isinstance(x, np.ndarray)),
        "Text - to - Image": ([np.ndarray], lambda x: isinstance(x, np.ndarray)),
        "Image - to - Text": ([str], lambda x: isinstance(x, str)),
        "Image - to - Image": ([np.ndarray], lambda x: isinstance(x, np.ndarray)),
        "Image - to - Video": (
            List[np.ndarray],
            lambda x: isinstance(x, list) and all(isinstance(t, np.ndarray) for t in x),
        ),
        "Video Classification": (
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
        "Text - to - Video": (
            List[np.ndarray],
            lambda x: isinstance(x, list) and all(isinstance(t, np.ndarray) for t in x),
        ),
        "Mask Generation": ([np.ndarray], lambda x: isinstance(x, np.ndarray)),
        "Image Feature Extraction": ([np.ndarray], lambda x: isinstance(x, np.ndarray)),
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
    }


def tasks2targets():
    text_targets = [
        "solution",
        "answer",
        "output",
        "response",
        "conversations",
        "inferences",
        "messages",
        "texts",
        "caption",
    ]
    image_targets = [
        "image",
        "url",
    ]
    video_targets = [
        "video",
        "url",
        "video_path",
        "video_file",
    ]
    class_targets = [
        "label",
        "class_name",
        "ground_truth",
        "emotion",
    ]
    depth_targets = ["depth"]
    mask_targets = ["mask"]
    imgfeatextr_targets = []
    keypoint_targets = []
    featextr_targets = []

    return {
        # Multimodal
        "Audio - Text - to - Text": text_targets,
        "Image - Text - to - Text": text_targets,
        "Visual Question Answering": text_targets,
        "Document Question Answering": text_targets,
        "Video - Text - to - Text": text_targets,
        # Computer Vision
        "Depth Estimation": depth_targets,
        "Image Classification": class_targets,
        "Text - to - Image": image_targets,
        "Image - to - Text": text_targets,
        "Image - to - Image": image_targets,
        "Image - to - Video": video_targets,
        "Video Classification": class_targets,
        "Text - to - Video": video_targets,
        "Mask Generation": mask_targets,
        "Image Feature Extraction": imgfeatextr_targets,
        "Keypoint Detection": keypoint_targets,
        # Natural Language Processing
        "Text Classification": class_targets,
        "Question Answering": text_targets,
        "Translation": text_targets,
        "Summarization": text_targets,
        "Feature Extraction": featextr_targets,
        "Text Generation": text_targets,
        "Text2Text Generation": text_targets,
    }


def tasks2targets_object_special_case():
    seg_targets = {
        "target": ["seg"],
        "label": ["cat", "label"],  # candidate names for target. Must be a set of those
        "obj": ["objects"],
    }  # candidate names for object
    objdetect_targets = {
        "target": ["box"],
        "label": ["cat", "label"],
        "obj": ["objects"],
    }
    return {
        "Image Segmentation": seg_targets,
        "Object Detection": objdetect_targets,
    }


def tasks2metrics():
    return {
        # Multimodal
        "Audio - Text - to - Text": [
            "wer",
            "cer",
            "blue",
            "rouge",
        ],  # Word Error Rate (WER), Character Error Rate (CER), blue, rouge
        "Image - Text - to - Text": ["blue", "rouge", "meteor", "cider", "spice"],
        "Visual Question Answering": [
            "EM",
            "blue",
            "meteor",
            "VQA Accuracy",
        ],  # Exact Match (EM), f1, blue, meteor, VQA Accuracy # 'f1',
        "Document Question Answering": ["EM", "blue", "rouge", "meteor"],  # 'f1',
        "Video - Text - to - Text": ["blue", "rouge", "meteor", "CIDEr", "spice"],
        # Computer Vision
        "Depth Estimation": [
            "mae",
            "rmse",
            "ssim",
            "sirmse",
        ],  # Mean Absolute Error (mae), Root Mean Square Error (rmse), Structural Similarity Index (ssim), Scale-Invariant rmse
        "Image Segmentation": ["IoU", "Pixel acc", "map", "dice"],
        "Object Detection": [
            "map",
            "IoU",
        ],  # Mean Average precision (map), Intersection over Union (IoU), recall, precision, f1 # , 'f1'
        "Image Classification": ["precision", "recall", "f1", "acc", "roc-auc"],
        "Text - to - Image": [
            "IS",
            "fid",
            "CLIPScore",
            "ssim",
        ],  # Inception Score (IS), Fréchet Inception Distance (fid), CLIPScore, Structural Similarity Index (ssim)
        "Image - to - Text": ["blue", "rouge", "meteor", "CIDEr", "spice"],
        "Image - to - Image": [
            "ssim",
            "psnr",
            "lpips",
        ],  # Structural Similarity Index (ssim), Peak Signal-to-Noise Ratio (psnr), lpips (Perceptual Loss)
        "Image - to - Video": [
            "FVD",
            "ssim",
            "psnr",
        ],  # FVD (Fréchet Video Distance), ssim, psnr
        "Video Classification": ["precision", "recall", "f1", "acc", "roc-auc"],
        "Text - to - Video": ["FVD", "IS", "fid", "ssim"],
        "Mask Generation": ["IoU", "Pixel Accuracy", "dice"],
        "Image Feature Extraction": [
            "Cosine Similarity",
            "Euclidean Distance",
            "lpips",
        ],
        "Keypoint Detection": [
            "PCK",
            "NME",
            "MSE",
        ],  # Percentage of Correct Keypoints (PCK), Normalized Mean Error (NME), Mean Squared Error (MSE)
        # Natural Language Processing
        "Text Classification": ["precision", "recall", "f1", "acc", "roc-auc"],
        "Question Answering": [
            "EM",
        ],  # Exact Match (EM), f1 # 'f1'
        "Translation": ["blue", "meteor", "rouge", "chrF++"],
        "Summarization": ["rouge", "blue", "meteor", "BERTScore"],
        "Feature Extraction": [
            "Cosine Similarity",
            "Euclidean Distance",
            "Pearson Correlation",
        ],
        "Text Generation": ["blue", "rouge", "meteor", "BERTScore", "Perplexity"],
        "Text2Text Generation": ["blue", "rouge", "meteor", "BERTScore", "chrF++"],
    }


def handle_object_special_case(data, task, target):
    t2t = tasks2targets_object_special_case()[task]
    targets_found = []
    for candidate_object in t2t["obj"]:
        for key in data:
            if candidate_object.lower() in key.lower():  # we have an object
                if isinstance(data[key], dict):
                    for candidate_target in t2t["target"]:
                        t = []
                        t_found = 0
                        l_found = 0
                        for k in data[key]:
                            if candidate_target.lower() in k.lower():
                                t.append(k)
                                t_found += 1
                            for candidate_label in t2t["label"]:
                                if candidate_label.lower() in k.lower():
                                    t.append(k)
                                    l_found += 1
                        if t_found == 1 and l_found == 1:
                            return [key, t[0], t[1]]  # object, target, label
                elif isinstance(data[key], list):
                    for candidate_target in t2t["target"]:
                        t = []
                        t_found = 0
                        l_found = 0
                        for k in data[key][0]:
                            if candidate_target.lower() in k.lower():
                                t.append(k)
                                t_found += 1
                            for candidate_label in t2t["label"]:
                                if candidate_label.lower() in k.lower():
                                    t.append(k)
                                    l_found += 1
                        if t_found == 1 and l_found == 1:
                            return [key, t[0], t[1]]  # object, target, label
    # if we don't have an object
    for candidate_target in t2t["target"]:
        t = []
        t_found = 0
        l_found = 0
        for k in data:
            if candidate_target.lower() in k.lower():
                t.append(k)
                t_found += 1
            for candidate_label in t2t["label"]:
                if candidate_label.lower() in k.lower():
                    t.append(k)
                    l_found += 1
        if t_found == 1 and l_found == 1:
            return [t[0], t[1]]  # target, category


def check_validity_of_output(out_sample, task):
    t2i = tasks2instance()
    if task in t2i:
        isok = t2i[task][1](out_sample)
        if isok:
            return True
        else:
            raise ValueError(
                f'Expected one of {", ".join(str(i) for i in t2i[task][0])}, but got {repr(out_sample)}'
            )
    else:
        raise ValueError(
            f"""Task of type "{task}", is not supported. Choose one of {', '.join('"'+i+'"' for i in t2i)}"""
        )


def check_validity_of_target(data, task, target_column):
    if task == "Image Segmentation" or task == "Object Detection":
        target_column = handle_object_special_case(data, task, target_column)
        return target_column

    if target_column is not None:
        for key in data:
            if target_column in key:
                return target_column

    # task exists in tasks2targets() because we already checked with check_validity_of_output()
    t2t = tasks2targets()[task]
    targets_found = []
    for candidate in t2t:
        for key in data:
            if candidate.lower() in key.lower():  # cases insensitive match
                targets_found.append(key)
    if len(targets_found) == 0:
        raise ValueError(
            f"""Expected one of {', '.join('"'+i+'"' for i in t2t)}, but got {', '.join('"'+key+'"' for key in data)}"""
        )
    elif len(targets_found) > 1:
        raise ValueError(
            f"""Found more that one match to target: {', '.join('"'+i+'"' for i in targets_found)}. Use the option "target" to choose which one you want"""
        )
    else:
        return targets_found[0]


def convert_to_datasets(data):
    if isinstance(data, datasets.Dataset):
        return data
    elif isinstance(data, dict):
        return datasets.Dataset.from_dict(data)
    elif isinstance(data, list):
        return datasets.Dataset.from_list(data)
    else:
        raise ValueError(f"Dataset of type {type(data)} is not supported")


def anns_to_datasets(anns):
    # assuming anns is a list
    if isinstance(anns[0], dict):
        return datasets.Dataset.from_list(anns)
    else:  # isinstance(anns[0], list)
        anns = [datasets.Dataset.from_list(ann) for ann in anns]
        anns = [datasets.Dataset.to_dict(ann) for ann in anns]
        return datasets.Dataset.from_list(anns)


def run(
    data: "path or data",
    pipeline: "callable",
    task: "str",
    target_column=None,
    metrics: "List[str]" = None,
    num_classes: int = None,  # in case the preds have more classes than target
    box_format: str = None,
    batch_size=1,
    anns: "List[List[dict]] | List[dict]" = [None],
):

    # Prepare data and anns
    if is_path(data):
        data = read_data(data)
    data = convert_to_datasets(data)
    data = data.batch(batch_size)
    anns = anns_to_datasets(anns)
    anns = anns.batch(batch_size)

    # Check validity of output and target
    out_sample = pipeline(data[0])
    check_validity_of_output(out_sample[0], task)
    target_column = check_validity_of_target(
        data[0] if len(anns.features) == 0 else anns[0], task, target_column
    )

    # Process data with pipeline
    pred = []
    for batch in data:
        pred.extend(pipeline(batch))

    # Calculate Metrics
    m = calc_metrics(data, pred, target_column, task, num_classes, anns)
    return m


# calc_metrics({'label': [1, 0, 1,0,1,0,1]}, [0.2,0.8,0.8,0.1,0.8,0.3,0.6], 'label', 'Image Classification')
# calc_metrics(data={"boxes": [[[300.00, 100.00, 315.00, 150.00],[300.00, 100.00, 315.00, 150.00]]], "labels": [[4,5]]}, preds=[([
#              [296.55, 93.96, 314.97, 152.79],
#              [298.55, 98.96, 314.97, 151.79]], [4, 5], [0.9, 0.8])], task='Object Detection',
#              target=['boxes', "labels"], num_classes_model=None)
