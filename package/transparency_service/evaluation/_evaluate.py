import torch
import datasets
from typing import List
from transparency_service.evaluation.task import Task
from transparency_service.evaluation import loaders

def calc_metrics(task: Task, device=None, **kwargs):
    if device is None: device = "cuda" if torch.cuda.is_available() else "cpu"
    kwargs = task.parameters[task](**kwargs, device=device)
    return {metric.__name__: metric(**kwargs, device=device) for metric in task.metrics}




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
    if loaders.is_path(data):
        data = loaders.read_data(data)
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

    preds = []
    for batch in data:
        preds.extend(pipeline(batch))
    m = calc_metrics(task, data=data, preds=preds, target_column=target_column, num_classes=num_classes, anns=anns)
    return m


# calc_metrics({'label': [1, 0, 1,0,1,0,1]}, [0.2,0.8,0.8,0.1,0.8,0.3,0.6], 'label', 'Image Classification')
# calc_metrics(data={"boxes": [[[300.00, 100.00, 315.00, 150.00],[300.00, 100.00, 315.00, 150.00]]], "labels": [[4,5]]}, preds=[([
#              [296.55, 93.96, 314.97, 152.79],
#              [298.55, 98.96, 314.97, 151.79]], [4, 5], [0.9, 0.8])], task='Object Detection',
#              target=['boxes', "labels"], num_classes_model=None)
