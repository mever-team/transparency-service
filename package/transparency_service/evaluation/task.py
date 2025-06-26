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
