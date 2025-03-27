import copy
import pandas as pd

from ._plots import _Plots
from ._github import _Github
from ._utils import _Utils
from ._metrics import _Metrics
from ._version_control import _Version_Control

class ModelCard(
	_Plots,
	_Github,
	_Utils,
	_Metrics,
	_Version_Control,
	):
	def __init__(self):
		_Version_Control.__init__(self)
		self.text = { # for legacy. have to change a bunch of code if I remove this
			"Title": "Model Card",
			"Model Details": {
				"Name": "",
				"Overview": "",
				"Version": "",
				"License": "",
				"GitHub": "",
				"Paper": ""
			},
			"Considerations": {
				"Use Case": "",
				"Limitations": "",
				"Ethical Risks": ""
			},
			"Training Set": {
				"Text": ""
			},
			"Eval Set": {
				"Text": ""
			},
			"Quantitative Analysis": {
				"Text": ""
			}
		}
		self.plots = {
			"Considerations": {},
			"Training Set": {},
			"Eval Set": {},
			"Quantitative Analysis": {}
		}
		self.content = {}
		self.compiled = None
		self.jsonsimple = copy.deepcopy(self.text)
		self.markdown_string = ""
		self.html_string = ""
		self.bar_plot_data = {}
		self.data = pd.DataFrame(columns=["label", "acc", "ap", "f1"])
		self.hash_history = []
		self.format_version = None
