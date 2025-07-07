import pandas as pd
import json
from transparency.card.traits.plots import Plots
from transparency.card.traits.repo import Repo
from transparency.card.traits.metrics import Metrics
from transparency.card.traits.version_control import VersionControl
from transparency.card.traits.html import HTMLRenderer
from transparency.card.dot_dict import DotDict


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