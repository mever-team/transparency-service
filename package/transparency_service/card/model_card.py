import pandas as pd
import json
from transparency_service.card.traits.plots import Plots
from transparency_service.card.traits.repo import Repo
from transparency_service.card.traits.metrics import Metrics
from transparency_service.card.traits.version_control import VersionControl
from transparency_service.card.traits.html import HTMLRenderer
from transparency_service.card.dot_dict import DotDict


class ModelCard(
    Plots,
    Repo,
    Metrics,
    VersionControl,
):
    def __init__(self):
        object.__setattr__(self, "data", DotDict(
            title="Model Card",
            model=DotDict(name="", overview="", version="", license="", github="", paper=""),
            considerations=DotDict(use_case="", limitations="", ethical_risks=""),
            training_set=DotDict(description="", plot=""),
            eval_set=DotDict(description="", plot=""),
            analysis=DotDict(description="", plot=""),
        ))
        VersionControl.__init__(self)
        """
        self.content = {}
        self._compiled = None
        self.html_string = ""
        self.bar_plot_data = {}
        self.data = pd.DataFrame(columns=["label", "acc", "ap", "f1"])
        self.hash_history = []
        self.format_version = None
        self.tips = {}
        self.metrics = None
        self.emission = None"""

    def __getattr__(self, key):
        if key=="data": return object.__getattribute__(self, key)
        if key in self.data: return self.data[key]
        raise AttributeError

    def __setattr__(self, key, value):
        if key=="data": return object.__setattr__(self, key, value)
        if key in self.data: self.data[key] = value
        return object.__setattr__(self, key, value)

    def to_html(self, editable=False):
        return HTMLRenderer(self.data, editable=editable).render()

    def save_json(self, filename: str):
        with open(filename, "w") as f:
            f.write(json.dumps(self.data))

    def load_json(self, filename: str):
        with open(filename, "r") as f:
            self.data.assign(json.loads(f.readline()))

    def save_html(self, filename: str, editable=False):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.to_html(editable))