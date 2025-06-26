import torchmetrics


# TODO: IoU for segmenation
def compute():
    return {
        "f1": lambda preds, target, task, num_classes, device: compute()["f1 micro"](
            preds, target, task, num_classes, device
        )
        | compute()["f1 macro"](preds, target, task, num_classes, device)
        | compute()["f1 weighted"](preds, target, task, num_classes, device),
        "acc": lambda preds, target, task, num_classes, device: compute()[
            "top-1 acc micro"
        ](preds, target, task, num_classes, device)
        | compute()["top-1 acc macro"](preds, target, task, num_classes, device)
        | compute()["top-1 acc weighted"](
            preds, target, task, num_classes, device
        ),  # , 'top-5 acc micro', compute()['top-5 acc micro'](preds, target, task, num_classes), 'top-5 acc macro', compute()['top-5 acc macro'](preds, target, task, num_classes), 'top-5 acc weighted', compute()['top-5 acc weighted'](preds, target, task, num_classes)},
        "precision": lambda preds, target, task, num_classes, device: compute()[
            "precision micro"
        ](preds, target, task, num_classes, device)
        | compute()["precision macro"](preds, target, task, num_classes, device)
        | compute()["precision weighted"](preds, target, task, num_classes, device),
        "recall": lambda preds, target, task, num_classes, device: compute()[
            "recall micro"
        ](preds, target, task, num_classes, device)
        | compute()["recall macro"](preds, target, task, num_classes, device)
        | compute()["recall weighted"](preds, target, task, num_classes, device),
        "roc-auc": lambda preds, target, task, num_classes, device: compute()[
            "roc-auc macro"
        ](preds, target, task, num_classes, device)
        | compute()["roc-auc weighted"](preds, target, task, num_classes, device),
        "dice": lambda preds, target, device: compute()["dice micro"](
            preds, target, num_classes, device
        )
        | compute()["dice macro"](preds, target, num_classes, device),
        "wer": lambda preds, target, device: {
            "wer": torchmetrics.text.WordErrorRate().to(device)(preds, target)
        },  # preds: List[str], target: List[str]
        "cer": lambda preds, target, device: {
            "cer": torchmetrics.text.CharErrorRate().to(device)(preds, target)
        },  # preds: List[str], target: List[str]
        "mae": lambda preds, target, device: {
            "mae": torchmetrics.regression.MeanAbsoluteError().to(device)(preds, target)
        },  # preds: Tensor[float], target: Tensor[float] or preds: Tensor[List[float]], target: Tensor[List[float]]
        "rmse": lambda preds, target, device: {
            "rmse": torchmetrics.image.RootMeanSquaredErrorUsingSlidingWindow().to(
                device
            )(preds, target)
        },  # tensors (N,C,H,W)
        "ssim": lambda preds, target, device: {
            "ssim": torchmetrics.image.StructuralSimilarityIndexMeasure().to(device)(
                preds, target
            )
        },  # Tensor[B, C, H, W] but not sure
        "f1 micro": lambda preds, target, task, num_classes, device: {
            "f1 micro": torchmetrics.F1Score(
                task=task,
                num_classes=num_classes,
                average="micro",
                num_labels=num_classes,
            ).to(device)(preds, target)
        },  # (binary/multiclass) preds: Tensor[int/float], target: Tensor[int] or (multilabel) preds: Tensor[List[int/float]], target: Tensor[List[int]]
        "f1 macro": lambda preds, target, task, num_classes, device: {
            "f1 macro": torchmetrics.F1Score(
                task=task,
                num_classes=num_classes,
                average="macro",
                num_labels=num_classes,
            ).to(device)(preds, target)
        },  # (binary/multiclass) preds: Tensor[int/float], target: Tensor[int] or (multilabel) preds: Tensor[List[int/float]], target: Tensor[List[int]]
        "f1 weighted": lambda preds, target, task, num_classes, device: {
            "f1 weighted": torchmetrics.F1Score(
                task=task,
                num_classes=num_classes,
                average="weighted",
                num_labels=num_classes,
            ).to(device)(preds, target)
        },  # (binary/multiclass) preds: Tensor[int/float], target: Tensor[int] or (multilabel) preds: Tensor[List[int/float]], target: Tensor[List[int]]
        "top-1 acc micro": lambda preds, target, task, num_classes, device: {
            "top-1 acc micro": torchmetrics.Accuracy(
                task=task,
                num_classes=num_classes,
                top_k=1,
                average="micro",
                num_labels=num_classes,
            ).to(device)(preds, target)
        },  # (binary/multiclass) preds: Tensor[int/float], target: Tensor[int] or (multilabel) preds: Tensor[List[int/float]], target: Tensor[List[int]]
        "top-1 acc macro": lambda preds, target, task, num_classes, device: {
            "top-1 acc macro": torchmetrics.Accuracy(
                task=task,
                num_classes=num_classes,
                top_k=1,
                average="macro",
                num_labels=num_classes,
            ).to(device)(preds, target)
        },  # (binary/multiclass) preds: Tensor[int/float], target: Tensor[int] or (multilabel) preds: Tensor[List[int/float]], target: Tensor[List[int]]
        "top-1 acc weighted": lambda preds, target, task, num_classes, device: {
            "top-1 acc weighted": torchmetrics.Accuracy(
                task=task,
                num_classes=num_classes,
                top_k=1,
                average="weighted",
                num_labels=num_classes,
            ).to(device)(preds, target)
        },  # (binary/multiclass) preds: Tensor[int/float], target: Tensor[int] or (multilabel) preds: Tensor[List[int/float]], target: Tensor[List[int]]
        "top-5 acc micro": lambda preds, target, task, num_classes, device: {
            "top-5 acc micro": torchmetrics.Accuracy(
                task=task,
                num_classes=num_classes,
                top_k=5,
                average="micro",
                num_labels=num_classes,
            ).to(device)(preds, target)
        },  # (binary/multiclass) preds: Tensor[int/float], target: Tensor[int] or (multilabel) preds: Tensor[List[int/float]], target: Tensor[List[int]]
        "top-5 acc macro": lambda preds, target, task, num_classes, device: {
            "top-5 acc macro": torchmetrics.Accuracy(
                task=task,
                num_classes=num_classes,
                top_k=5,
                average="macro",
                num_labels=num_classes,
            ).to(device)(preds, target)
        },  # (binary/multiclass) preds: Tensor[int/float], target: Tensor[int] or (multilabel) preds: Tensor[List[int/float]], target: Tensor[List[int]]
        "top-5 acc weighted": lambda preds, target, task, num_classes, device: {
            "top-5 acc weighted": torchmetrics.Accuracy(
                task=task,
                num_classes=num_classes,
                top_k=5,
                average="weighted",
                num_labels=num_classes,
            ).to(device)(preds, target)
        },  # (binary/multiclass) preds: Tensor[int/float], target: Tensor[int] or (multilabel) preds: Tensor[List[int/float]], target: Tensor[List[int]]
        "precision micro": lambda preds, target, task, num_classes, device: {
            "precision micro": torchmetrics.Precision(
                task=task,
                num_classes=num_classes,
                average="micro",
                num_labels=num_classes,
            ).to(device)(preds, target)
        },  # (binary/multiclass) preds: Tensor[int/float], target: Tensor[int] or (multilabel) preds: Tensor[List[int/float]], target: Tensor[List[int]]
        "precision macro": lambda preds, target, task, num_classes, device: {
            "precision macro": torchmetrics.Precision(
                task=task,
                num_classes=num_classes,
                average="macro",
                num_labels=num_classes,
            ).to(device)(preds, target)
        },  # (binary/multiclass) preds: Tensor[int/float], target: Tensor[int] or (multilabel) preds: Tensor[List[int/float]], target: Tensor[List[int]]
        "precision weighted": lambda preds, target, task, num_classes, device: {
            "precision weighted": torchmetrics.Precision(
                task=task,
                num_classes=num_classes,
                average="weighted",
                num_labels=num_classes,
            ).to(device)(preds, target)
        },  # (binary/multiclass) preds: Tensor[int/float], target: Tensor[int] or (multilabel) preds: Tensor[List[int/float]], target: Tensor[List[int]]
        "recall micro": lambda preds, target, task, num_classes, device: {
            "recall micro": torchmetrics.Recall(
                task=task,
                num_classes=num_classes,
                average="micro",
                num_labels=num_classes,
            ).to(device)(preds, target)
        },  # (binary/multiclass) preds: Tensor[int/float], target: Tensor[int] or (multilabel) preds: Tensor[List[int/float]], target: Tensor[List[int]]
        "recall macro": lambda preds, target, task, num_classes, device: {
            "recall macro": torchmetrics.Recall(
                task=task,
                num_classes=num_classes,
                average="macro",
                num_labels=num_classes,
            ).to(device)(preds, target)
        },  # (binary/multiclass) preds: Tensor[int/float], target: Tensor[int] or (multilabel) preds: Tensor[List[int/float]], target: Tensor[List[int]]
        "recall weighted": lambda preds, target, task, num_classes, device: {
            "recall weighted": torchmetrics.Recall(
                task=task,
                num_classes=num_classes,
                average="weighted",
                num_labels=num_classes,
            ).to(device)(preds, target)
        },  # (binary/multiclass) preds: Tensor[int/float], target: Tensor[int] or (multilabel) preds: Tensor[List[int/float]], target: Tensor[List[int]]
        "roc-auc macro": lambda preds, target, task, num_classes, device: {
            "roc-auc macro": torchmetrics.AUROC(
                task=task,
                num_classes=num_classes,
                average="macro",
                num_labels=num_classes,
            ).to(device)(preds, target)
        },  # (binary/multiclass) preds: Tensor[int/float], (multiclass) preds: Tensor[List[float]],, target: Tensor[int] or (multilabel) preds: Tensor[List[int/float]], target: Tensor[List[int]]
        "roc-auc weighted": lambda preds, target, task, num_classes, device: {
            "roc-auc weighted": torchmetrics.AUROC(
                task=task,
                num_classes=num_classes,
                average="weighted",
                num_labels=num_classes,
            ).to(device)(preds, target)
        },  # (binary/multiclass) preds: Tensor[int/float], (multiclass) preds: Tensor[List[float]],, target: Tensor[int] or (multilabel) preds: Tensor[List[int/float]], target: Tensor[List[int]]
        "map": lambda preds, target, iou_type, box_format, device: {
            "map": torchmetrics.detection.MeanAveragePrecision(
                iou_type=iou_type, box_format=box_format
            ).to(device)(preds, target)
        },
        "IoU": lambda preds, target, iou_type, box_format, device: {
            "IoU": torchmetrics.detection.IntersectionOverUnion(
                box_format=box_format
            ).to(device)(preds, target)
        },  # torch offers only iou for bboxes. what about segmenation
        "dice micro": lambda preds, target, num_classes, device: {
            "dice": torchmetrics.classification.Dice(
                num_classes=num_classes, average="micro"
            ).to(device)(preds, target)
        },
        "dice macro": lambda preds, target, num_classes, device: {
            "dice": torchmetrics.classification.Dice(
                num_classes=num_classes, average="macro"
            ).to(device)(preds, target)
        },
        "psnr": lambda preds, target, device: {
            "psnr": torchmetrics.image.PeakSignalNoiseRatio().to(device)(preds, target)
        },
        #'lpips': lambda preds, target: {'lpips': torchmetrics.image.lpip.LearnedPerceptualImagePatchSimilarity()(preds, target)},
        #'fid': lambda preds, target: {'fid': torchmetrics.image.fid.FrechetInceptionDistance()(preds, target)},
        #'Cosine Similarity'
        #'Pearson Correlation'
    }
