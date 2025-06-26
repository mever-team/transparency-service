import pandas as pd
from transparency_service.card.traits.plots import Plots
from transparency_service.card.traits.repo import Repo
from transparency_service.card.traits.utils import Utils
from transparency_service.card.traits.metrics import Metrics
from transparency_service.card.traits.version_control import VersionControl


class DotDict(dict):
    def __init__(self, **kwargs):
        super().__init__({k.replace("_", " "): v for k,v in kwargs.items()})
    def __getattr__(self, attr):
        try: return self[attr.replace("_", " ")]
        except KeyError: raise AttributeError
    def __setattr__(self, attr, value):
        self[attr.replace("_", " ")] = value
    def __delattr__(self, attr):
        try: del self[attr.replace("_", " ")]
        except KeyError: raise AttributeError


class ModelCard(
    Plots,
    Repo,
    Utils,
    Metrics,
    VersionControl,
):
    def __init__(self):
        VersionControl.__init__(self)
        self.text = DotDict(
            Title="Model Card",
            Model_Details=DotDict(Name="", Overview="",Version="",License="",GitHub="",Paper=""),
            Considerations=DotDict(Use_Case="", Limitations="", Ethical_Risks=""),
            Training_Set=DotDict(Description=""),
            Eval_Set=DotDict(Description=""),
            Quantitative_Analysis=DotDict(Description=""),
        )
        self.plots = DotDict(
            Considerations=DotDict(Use_Case="", Limitations="", Ethical_Risks=""),
            Training_Set=DotDict(Description=""),
            Eval_Set=DotDict(Description=""),
            Quantitative_Analysis=DotDict(Description=""),
        )
        self.content = {}
        self.compiled = None
        self.html_string = ""
        self.bar_plot_data = {}
        self.data = pd.DataFrame(columns=["label", "acc", "ap", "f1"])
        self.hash_history = []
        self.format_version = None
        self.tips = {}
        self.metrics = None
        self.emission = None
