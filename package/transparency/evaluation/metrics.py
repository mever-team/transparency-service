import torchmetrics

# (binary/multiclass) preds: Tensor[int/float], (multiclass) preds: Tensor[List[float]],, targets: Tensor[int]
# or (multilabel) preds: Tensor[List[int/float]], targets: Tensor[List[int]]

def f1(preds, targets, task, num_classes, device): return f1_micro(preds, targets, task, num_classes, device)
def f1_micro(preds, targets, task, num_classes, device): return torchmetrics.F1Score(task=task, num_classes=num_classes, average="micro", num_labels=num_classes).to(device)(preds, targets)
def f1_macro(preds, targets, task, num_classes, device): return torchmetrics.F1Score(task=task, num_classes=num_classes, average="macro", num_labels=num_classes).to(device)(preds, targets)
def f1_weighted(preds, targets, task, num_classes, device): return torchmetrics.F1Score(task=task, num_classes=num_classes, average="weighted", num_labels=num_classes).to(device)(preds, targets)
def top1_acc_micro(preds, targets, task, num_classes, device): return torchmetrics.Accuracy(task=task, num_classes=num_classes, top_k=1, average="micro", num_labels=num_classes).to(device)(preds, targets)
def top1_acc_macro(preds, targets, task, num_classes, device): return torchmetrics.Accuracy(task=task, num_classes=num_classes, top_k=1, average="macro", num_labels=num_classes).to(device)(preds, targets)
def top1_acc_weighted(preds, targets, task, num_classes, device): return torchmetrics.Accuracy(task=task, num_classes=num_classes, top_k=1, average="weighted", num_labels=num_classes).to(device)(preds, targets)
def top5_acc_micro(preds, targets, task, num_classes, device): return torchmetrics.Accuracy(task=task, num_classes=num_classes, top_k=5, average="micro", num_labels=num_classes).to(device)(preds, targets)
def top5_acc_macro(preds, targets, task, num_classes, device): return torchmetrics.Accuracy(task=task, num_classes=num_classes, top_k=5, average="macro", num_labels=num_classes).to(device)(preds, targets)
def top5_acc_weighted(preds, targets, task, num_classes, device): return torchmetrics.Accuracy(task=task, num_classes=num_classes, top_k=5, average="weighted", num_labels=num_classes).to(device)(preds, targets)
def precision_micro(preds, targets, task, num_classes, device): return torchmetrics.Precision(task=task, num_classes=num_classes, average="micro", num_labels=num_classes).to(device)(preds, targets)
def precision_macro(preds, targets, task, num_classes, device): return torchmetrics.Precision(task=task,num_classes=num_classes,average="macro",num_labels=num_classes).to(device)(preds, targets)
def precision_weighted(preds, targets, task, num_classes, device): return torchmetrics.Precision(task=task,  num_classes=num_classes, average="weighted", num_labels=num_classes).to(device)(preds, targets)
def recall_micro(preds, targets, task, num_classes, device): return torchmetrics.Recall(task=task, num_classes=num_classes, average="micro",num_labels=num_classes).to(device)(preds, targets)
def recall_macro(preds, targets, task, num_classes, device): return torchmetrics.Recall(task=task, num_classes=num_classes, average="macro", num_labels=num_classes).to(device)(preds, targets)
def recall_weighted(preds, targets, task, num_classes, device): return torchmetrics.Recall(task=task, num_classes=num_classes, average="weighted", num_labels=num_classes,).to(device)(preds, targets)
def auc_roc_macro(preds, targets, task, num_classes, device): return torchmetrics.AUROC(task=task, num_classes=num_classes, average="macro", num_labels=num_classes).to(device)(preds, targets)
def auc_roc_weighted(preds, targets, task, num_classes, device): return torchmetrics.AUROC(task=task, num_classes=num_classes, average="weighted", num_labels=num_classes).to(device)(preds, targets)
def dice_micro(preds, targets, num_classes, device): return torchmetrics.classification.Dice(num_classes=num_classes, average="micro").to(device)(preds, targets)
def dice_macro(preds, targets, num_classes, device): return torchmetrics.classification.Dice(num_classes=num_classes, average="macro").to(device)(preds, targets)
def wer(preds, targets, device):
    """Word Error Rate"""
    return torchmetrics.text.WordErrorRate().to(device)(preds, targets)
def cer(preds, targets, device):
    """Character Error Rate"""
    return torchmetrics.text.CharErrorRate().to(device)(preds, targets)
def mae(preds, targets, device):
    """Mean Absolute Error"""
    return torchmetrics.regression.MeanAbsoluteError().to(device)(preds, targets)
def rmse(preds, targets, device):
    """Root Mean Square Error"""
    return torchmetrics.image.RootMeanSquaredErrorUsingSlidingWindow().to(device)(preds, targets)
def ssim(preds, targets, device):
    """Structural Similarity Index"""
    return torchmetrics.image.StructuralSimilarityIndexMeasure().to(device)(preds, targets)
def psnr(preds, targets, device):
    """Peak Signal-to-Noise Ratio"""
    return torchmetrics.image.PeakSignalNoiseRatio().to(device)(preds, targets)
def map(preds, targets, iou_type, box_format, device):
    """Mean Average precision"""
    # TODO: module 'torchmetrics.detection' has no attribute 'MeanAveragePrecision'
    return torchmetrics.detection.MeanAveragePrecision(iou_type=iou_type, box_format=box_format).to(device)(preds, targets)
def IoU(preds, targets, iou_type, box_format, device):
    """Intersection over Union"""
    # TODO: torch offers only iou for bboxes. what about segmenation
    # TODO: module 'torchmetrics.detection' has no attribute 'IntersectionOverUnion'
    return torchmetrics.detection.IntersectionOverUnion(box_format=box_format).to(device)(preds, targets)
