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
        VersionControl.__init__(self)
        self.text = DotDict(
            title="Model Card",
            model=DotDict(name="", overview="", version="", license="", github="", paper=""),
            considerations=DotDict(use_case="", limitations="", ethical_risks=""),
            training_set=DotDict(description="", plot=""),
            eval_set=DotDict(description="", plot=""),
            analysis=DotDict(description="", plot=""),
        )
        self.content = {}
        self._compiled = None
        self.html_string = ""
        self.bar_plot_data = {}
        self.data = pd.DataFrame(columns=["label", "acc", "ap", "f1"])
        self.hash_history = []
        self.format_version = None
        self.tips = {}
        self.metrics = None
        self.emission = None

    def to_html(self, editable=False):
        return HTMLRenderer(self.text, editable=editable).render()

    def save_json(self, filename: str):
        with open(filename, "w") as f:
            f.write(json.dumps({"format_version": self.format_version}) + "\n")
            f.write(json.dumps({"text": self.text}) + "\n")
            f.write(json.dumps({"plots": self.plots}) + "\n")
            f.write(json.dumps({"hash_history": self.hash_history}) + "\n")
            f.write(json.dumps({"tips": self.tips}) + "\n")
            f.write(json.dumps({"metrics": self.metrics}) + "\n")
            f.write(json.dumps({"emission": self.emission}) + "\n")

    def load_json(self, filename: str):
        with open(filename, "r") as f:
            self.format_version = json.loads(f.readline())["format_version"]
            self.text = json.loads(f.readline())["text"]
            self.plots = json.loads(f.readline())["plots"]
            self.hash_history = json.loads(f.readline())["hash_history"]
            self.tips = json.loads(f.readline())["tips"]
            self.metrics = json.loads(f.readline())["metrics"]
            self.emission = json.loads(f.readline())["emission"]

    def save_html(self, filename: str, editable=False):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.to_html(editable))