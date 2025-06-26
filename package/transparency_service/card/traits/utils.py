import json
import copy
from transparency_service.card.traits.html import HTMLRenderer


class Utils:
    ###################################
    ####	saves and loads			###
    ###################################
    def save(self, filename: str = "out", editable_html=False):
        self.save_json(f"{filename}.jsonl")
        self.json_to_html()
        self.save_html(f"{filename}.html")

    def save_json(self, filename: str):
        with open(filename, "w") as f:
            f.write(json.dumps({"format_version": self.format_version}) + "\n")
            f.write(json.dumps({"text": self.text}) + "\n")
            f.write(json.dumps({"plots": self.plots}) + "\n")
            f.write(json.dumps({"hash_history": self.hash_history}) + "\n")
            f.write(json.dumps({"tips": self.tips}) + "\n")
            f.write(json.dumps({"metrics": self.metrics}) + "\n")
            f.write(json.dumps({"emission": self.emission}) + "\n")

    def save_html(self, filename: str):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.html_string)

    def json_to_html(self, editable_html=False):
        self.compile()
        htmlout = HTMLRenderer(self.compiled, editable_html=editable_html)
        self.html_string = htmlout.json_to_html()

    def load_json(self, filename: str):
        with open(filename, "r") as f:
            self.format_version = json.loads(f.readline())["format_version"]
            self.text = json.loads(f.readline())["text"]
            self.plots = json.loads(f.readline())["plots"]
            self.hash_history = json.loads(f.readline())["hash_history"]
            self.tips = json.loads(f.readline())["tips"]
            self.metrics = json.loads(f.readline())["metrics"]
            self.emission = json.loads(f.readline())["emission"]

    ###################################
    ####		other utils			###
    ###################################
    def _json2content(self):
        for tab_name in self.text:
            if (
                tab_name == "Training Set"
                or tab_name == "Eval Set"
                or tab_name == "Quantitative Analysis"
            ):
                self.content[tab_name] = ""
                for bullet, content in self.text[tab_name].items():
                    self.content[tab_name] += f"<p>{content}</p>"
            elif isinstance(self.text[tab_name], str):
                self.content[tab_name] = self.text[tab_name]
            else:
                self.content[tab_name] = ""
                for bullet, content in self.text[tab_name].items():
                    self.content[
                        tab_name
                    ] += f"<p><strong>{bullet}:</strong> {content}</p>"
        return self.content

    def compile(self):
        self.compiled = copy.deepcopy(self.text)
        for field in self.compiled:
            if field in self.plots:
                for plot in self.plots[field]:
                    self.compiled[field]["Description"] += self.plots[field][plot]
