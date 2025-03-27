"""
Cases done:
    single file with supported files: ..utils._read_data_structure.get_supported_types()
    folder with multimple supported files
Image.registered_extensions()
"""
import os.path
from PIL import Image
import pandas as pd

try:
    import torch
    from torch.utils.data import Dataset
except ImportError:
    pass
from typing import List, Callable, Union
from ..utils._read_data_structure import get_data
from ..utils._count_data import count_data
from ..utils._read_data_structure import get_supported_images
import sklearn
import numpy as np
from ..model_card_generator import ModelCard

import transformers
from torchmetrics.detection import MeanAveragePrecision


def isImage(path):
    _, extension = os.path.splitext(path)
    return extension.lower() in Image.registered_extensions()

def get_supported_models():
    return [
        'torch'
    ]

def model_agnostics(model):
    supported_models = get_supported_models()
    if supported_models[0] in globals(): # torch
        if isinstance(model, torch.nn.Module):
            return supported_models[0]
    else:
        print(f"Did not find an installation of supported models. Supported models are: {supported_models}")
        return None

def calc_max_image_dim(image_paths):
    max_width = 0
    max_height = 0

    for path in image_paths:
        with Image.open(path) as img:
            width, height = img.size
            max_width = max(max_width, width)
            max_height = max(max_height, height)

    return max_width, max_height

class EvaluationDataset(Dataset):
    def __init__(self, in_dict, is_file, preprocessor, label_name, assign_classes, max_width = None, max_height = None):
        self.preprocessor = preprocessor
        self.is_file = is_file
        if self.is_file:
            self.eval_set = pd.DataFrame(in_dict)
        else:
            self.eval_set = in_dict['Files']
        self.label_name = label_name
        self.assign_classes = assign_classes
        self.max_width = max_width
        self.max_height = max_height
    def __len__(self):
        return len(self.eval_set)


    def __getitem__(self, idx):
        if self.is_file:
            row_data = self.eval_set.iloc[idx].copy()
            processed_data = self.preprocessor(row_data)
            if self.assign_classes is not None:
                for key, label in self.assign_classes.items():
                    if row_data[self.label_name] == key:
                        row_data[self.label_name] = label
            return [processed_data, row_data[self.label_name]]
        else: # Only Image cases for now
            row_data = self.eval_set[idx]
            row_data = Image.open(row_data).convert('RGB')
            padded_img = Image.new("RGB", (self.max_width, self.max_height), (0, 0, 0))
            padded_img.paste(row_data, (0, 0))
            processed_data = self.preprocessor(padded_img)
            return processed_data

def xywh_to_xyxy(xywh):
    return [xywh[0], xywh[1], xywh[0] + xywh[2], xywh[1] + xywh[3]]

def run_eval(model, model_type, preprocessor, in_dic, is_file, device, label_name,
             batch_size, num_workers, assign_classes, basename, annotations, postprocessor,
             target_box_format, predict_box_format, target_iou, predict_iou,predict_labels,target_labels,scores) -> dict:
    supported_models = get_supported_models()
    out_dic = {}
    if model_type == supported_models[0]: # torch
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        if is_file: # files
            current_assign_classes = assign_classes  # changed from None to work with folder classification
            if assign_classes is not None:  # get assign classes
                for key, value in assign_classes.items():
                    if os.path.basename(basename) == key:
                        current_assign_classes = assign_classes[os.path.basename(basename)]
            # change the is_file to False in case of folder -> Images
            if 'Files' in in_dic:
                is_file = False
                max_w, max_h = calc_max_image_dim(in_dic['Files'])
                eval_data = EvaluationDataset(in_dic, is_file, preprocessor, label_name, current_assign_classes,
                                              max_width=max_w, max_height=max_h)
            else:
                eval_data = EvaluationDataset(in_dic, is_file, preprocessor, label_name, current_assign_classes)

            # TODO: do the same for label_name
            loader = torch.utils.data.DataLoader(
                eval_data,
                batch_size=batch_size,
                shuffle=False,
                num_workers=num_workers,
                pin_memory=True,
                drop_last=False,
            )
            model.to(device)
            y_true = []
            y_score = []
            with torch.no_grad():
                if is_file: # no images
                    for data in loader:
                        model_input, labels = data
                        model_input, labels = model_input.to(device), labels.to(device)
                        outputs = model(model_input)
                        y_true.extend(labels.cpu().numpy().tolist())
                        y_score.extend(torch.sigmoid(outputs).cpu().numpy().tolist())
                    test_acc = sklearn.metrics.accuracy_score(np.array(y_true), np.array(y_score) > 0.5)
                    test_ap = sklearn.metrics.average_precision_score(y_true, y_score)
                    out_dic[basename] = {'acc': test_acc * 100, 'ap': test_ap * 100}
                    return out_dic
                else: # Images
                    preds = []
                    target = []
                    for data in loader:
                        if len(data.keys()) != 0: # if it is a dictionary
                            # Result dictionary to store individual values
                            for values in zip(*data.values()):
                                model_input = {key: value for key, value in zip(data.keys(), values)}
                                model_input = transformers.BatchFeature(model_input).to(device)
                                outputs = model(model_input)
                                image_size = [max_w, max_h]
                                if postprocessor is not None:
                                    outputs = postprocessor(outputs, image_size)
                                preds.append(dict(boxes=outputs[predict_iou], scores=outputs[scores], labels=outputs[predict_labels]))
                        else: # TODO:
                            pass
                    # Construct Targe
                    target_boxes = []
                    for anns in annotations:
                        target_boxes.append([[ann[target_iou][0], ann[target_iou][1], ann[target_iou][2],ann[target_iou][3]] for ann in anns])
                    if target_box_format == 'xywh':
                        for boxes in target_boxes:
                            for i, box in enumerate(boxes):
                                boxes[i] = xywh_to_xyxy(box)
                    for i, boxes in enumerate(target_boxes):
                        target_boxes[i] = torch.tensor(boxes).to(device)
                    # Construct Predicted
                    # preds = preds
                    target_labels_list = []
                    for anns in annotations:
                        target_labels_list.append(torch.tensor([ann[target_labels] for ann in anns]).to(device))
                    for tb, tl in zip(target_boxes, target_labels_list):
                        target.append(dict(boxes=tb, labels=tl))
                    # print(target)

                    metric = MeanAveragePrecision(iou_type="bbox")
                    metric.update(preds, target)
                    print(f"metric: {metric.compute()}")

        elif "Files" in in_dic: # folder -> files
            isimage = os.path.splitext(in_dic['Files'][0])[1] in get_supported_images()
            accumulated_metrics = {}
            if not isimage: # Not an image
                for i, path in enumerate(in_dic["Files"]):
                    dic_current, is_file_current, total_len  = get_data(path)
                    metrics = run_eval(model, model_type, preprocessor, dic_current, is_file_current, device,
                             label_name, batch_size, num_workers, assign_classes, os.path.basename(path), annotations,
                                       postprocessor, target_box_format, predict_box_format, target_iou, predict_iou,
                                       predict_labels,target_labels,scores)
                    accumulated_metrics[i] = next(iter(metrics.values()))
            else: # is image
                dic_current, is_file_current, total_len = in_dic, True, len(in_dic['Files'])
                metrics = run_eval(model, model_type, preprocessor, dic_current, is_file_current, device,
                            label_name, batch_size, num_workers, assign_classes, 'eoeoeoeoe', annotations,
                                   postprocessor, target_box_format, predict_box_format, target_iou, predict_iou,
                                   predict_labels,target_labels,scores)
                accumulated_metrics[i] = next(iter(metrics.values()))
            acc = []
            ap = []
            for key, value in accumulated_metrics.items():
                acc.append(value['acc'])
                ap.append(value['ap'])
            acc = sum(acc)/len(accumulated_metrics)
            ap = sum(ap)/len(accumulated_metrics)
            out_dic[basename] = {'acc': acc, 'ap': ap}
            return  out_dic
        else: # folder -> folders ... this is the last case else ..utis._read_data_structure.get_list_of_items( will raise an error
            for path in in_dic:
                # create [path, label] and run evaluation. this will output ONE accuracy value
                # convert the full path to class name
                in_dic[os.path.basename(path)] = in_dic.pop(path)
            pass


def write_md(model_card, metrics_pd):
    # TODO: for multiple splits
    model_card.text['Quantitative Analysis']['ACC plot'] = model_card.bar_plot(
        pdata=metrics_pd,
        y='acc',
        x='set',
        title='ACC',
        yaxis_title='Accuracy (%)').replace('<div>', '<div class="plot-inline-div">')
    model_card.text['Quantitative Analysis']['AP plot'] = model_card.bar_plot(
        pdata=metrics_pd,
        y='ap',
        x='set',
        title='AP',
        yaxis_title='Average Precision (%)').replace('<div>', '<div class="plot-inline-div">')

def evaluate(
        model: "torch.nn.Module",
        preprocessor: Union[Callable, object],
        path: "str | List[str] path to file/folder",
        postprocessor: Union[Callable, object] = None,
        annotations: "iterable" = None,
        target_box_format: "'xyxy' 'xywh'" = 'xywh',
        predict_box_format: "'xyxy' 'xywh'" = 'xywh',
        target_iou='bbox',
        predict_iou='bbox',
        predict_labels = 'labels',
        target_labels = 'labels',
        scores = 'scores',
        device: str = None,
        label_name: str = 'label', # TODO: support for folder e.g. multiple files with different label_name
        batch_size = 32,
        num_workers = 1,
        assign_classes: dict = None,
        model_card: ModelCard = None,
        split: 'str | List[str]' = None):
    metrics_pd = pd.DataFrame()
    if not isinstance(path, list): # if not a list make it
        path = [path]
    path = [os.path.expanduser(p) for p in path]
    if not isinstance(split, list) and split is not None: # if not a list make it
        split = [split]
    model_type = model_agnostics(model)
    if model_type is None:
        return
    else:
        for p in path: # each path will yield a dict of metric values
            data, is_file, total_len = get_data(p, split = split)
            if data is None:
                raise ValueError("Improper data")
            if split is not None:
                basename = os.path.basename(p)
                accumulated = []
                for i, chunk in enumerate(data):
                    for isplit in chunk:
                        metrics = run_eval(model, model_type, preprocessor, chunk[isplit], is_file,
                                           device, label_name, batch_size, num_workers, assign_classes, basename,
                                           annotations, postprocessor, target_box_format, predict_box_format,
                                           target_iou, predict_iou,predict_labels,target_labels,scores)
                        new_row = metrics[basename] | {'set': os.path.splitext(basename)[0]} | {'split': isplit}
                        metrics_pd = pd.concat([metrics_pd, pd.DataFrame(new_row, index=[0])], ignore_index=True)
                        accumulated.append(metrics_pd)
                    accumulated_df = pd.concat(accumulated, ignore_index=True)
                    metrics_pd = accumulated_df.groupby(['set', 'split'], as_index=False).mean()
            else:
                basename  = os.path.basename(p)
                accumulated = []
                for i, chunk in enumerate(data):
                    metrics = run_eval(model, model_type, preprocessor, chunk, is_file,
                                       device, label_name, batch_size, num_workers, assign_classes, basename,
                                       annotations, postprocessor, target_box_format, predict_box_format,
                                       target_iou, predict_iou,predict_labels,target_labels,scores)
                    new_row = metrics[basename] | {'set': os.path.splitext(basename)[0]}
                    metrics_pd = pd.concat([metrics_pd, pd.DataFrame(new_row, index=[0])], ignore_index=True)
                    accumulated.append(metrics_pd)
                accumulated_df = pd.concat(accumulated, ignore_index=True)
                mean_values = accumulated_df.select_dtypes(include=['number']).mean()
                mean_row = mean_values.to_dict()
                mean_row['set'] = accumulated_df['set'].iloc[0]
                metrics_pd = pd.DataFrame([mean_row])

    if model_card is not None:
        write_md(model_card, metrics_pd)
        # write the 'Eval Set' of the model_card
        count_data(path, split = split, model_card = model_card, is_train_set = False)