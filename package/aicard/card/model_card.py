import json
from typing import Union

import html2text
import markdown2
import rich
import io
from aicard.card.traits.html import HTMLRenderer
from aicard.card.dot_dict import DotDict
from rich.markdown import Markdown

from pydantic import BaseModel, create_model

def truncate(text, size):
    if size<3:
        return ""
    text = str(text)
    size = int(size)
    if len(text)<=size:
        return text
    return text[:(size-3)]+"..."


class ModelCard:
    def __init__(self, connector=None):
        object.__setattr__(self, "data", DotDict(
            title="Model Card",
            model=DotDict(name="", overview="", author="", date="", version="", type="", license="", github="", paper="", contact="", more=""),
            considerations=DotDict(use_case="", oversight="", out_of_scope_use="", limitations="", ethical_risks="", software="", hardware="",
                                   instructions="", inputs_outputs="", factors="", more=""),
            training_set=DotDict(datasets="", motivation="", pre_processing="", standards="", update="", more=""),
            eval_set=DotDict(datasets="", motivation="", pre_processing="", standards="", update="", more=""),
            analysis=DotDict(analysis="", metrics="", thresholds="", uncertainty="", more=""),
        ))
        self.connector = connector # used by the client - the server does something else and model cards stored there should never set this field
        #VersionControl.__init__(self)

    def __enter__(self):
        assert self.connector, "You need a model card connector to use it as a context"
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.commit()
        return False

    def __del__(self):
        if self.connector:
            assert json.dumps(self.connector.prototype.data) == json.dumps(self.data), \
                "There are uncommitted changes to a model card with a connector. Do one of these:\n * Commit the changes\n * Detach the connector\n * Use the card as a context to auto-commit"

    def detach(self):
        self.connector = None
        return self

    def __getattr__(self, key):
        if key in ["data", "connector"]: return object.__getattribute__(self, key)
        if key in self.data: return self.data[key]
        raise AttributeError

    def __setattr__(self, key, value):
        if key in ["data", "connector"]: return object.__setattr__(self, key, value)
        if key in self.data: self.data[key] = value
        return object.__setattr__(self, key, value)

    def is_stable(self):
        return (not self.connector) or json.dumps(self.connector.prototype.data) == json.dumps(self.data)

    def gist(self, assistant):
        assert self.is_stable(), "Cannot obtain a gist while there are uncommited changes"
        if not self.connector:
            card = ModelCard()
            card.data.assign(self.data)
            assistant.refine(card)
        else:
            card = self.connector.create(self)
            assistant.refine(card)
        return card

    def complete(self, assistant, url: str):
        assert self.is_stable(), "Cannot obtain a gist while there are uncommited changes"
        assistant.complete(self, url)
        return self

    def merge(self, data: Union["ModelCard",dict], message: str|None=None):
        if isinstance(data, ModelCard): data = data.data
        assert isinstance(data, dict), "Can only merge with another model card or dct"
        self.data.append(data, message=message)

    def commit(self):
        from aicard.service import converters
        assert self.connector, "The current model card does not have any connector to commit to (either it was not obtained from a connection or it was detached)."
        if json.dumps(self.connector.prototype.data) == json.dumps(self.data):
            self.connector.client.logger.info(f"Nothing to commit")
            return
        result = self.connector.client.put(f"/card/{self.connector.id}", json=converters.dict2dynamic(self.data))
        assert result.status_code == 200, "Failed to commit"
        self.connector.prototype.data.assign(self.data)
        self.connector.client.logger.info(f"Committed card")

    def assign(self, other: "ModelCard"):
        self.data.assign(other.data)

    def summary(self):
        summary = ""
        #if self.data.model.name:
        #    summary += " "+truncate(self.data.model.name.split(" ")[0].split("\n")[0], 50)
        if self.data.model.version:
            summary += " version "+truncate(self.data.model.version.split(" ")[0].split("\n")[0], 50)
        return summary[1:] if summary else ""

    def quality(self) -> float:
        nom = 0
        denom = 0
        for key, dotdict in self.data.items():
            if isinstance(dotdict, DotDict):
                for field, value in dotdict.items():
                    denom += 1
                    if value.strip(): nom += 1
            else:
                denom += 1
                if dotdict: nom += 1
        return nom/denom

    def to_markdown_card(self):
        card = ModelCard()
        card.title = self.title
        for key, dotdict in self.data.items():
            if isinstance(dotdict, DotDict):
                for field, value in dotdict.items():
                    assert isinstance(value, str)
                    card.data[key][field] = html2text.html2text(value)
        return card

    def to_html_card(self):
        card = ModelCard()
        card.title = self.title
        for key, dotdict in self.data.items():
            if isinstance(dotdict, DotDict):
                for field, value in dotdict.items():
                    assert isinstance(value, str)
                    # the following line is a trick so that simple strings remain simple strings without <p>
                    value = markdown2.markdown(value, extras=["markdown-in-html", "code-friendly"])
                    if value.startswith("<p>") and value.count("</p>")==1: value = value.strip()[3:-4]
                    card.data[key][field] = value
        return card

    def to_markdown(self):
        ret = ""
        card = self.to_markdown_card()
        for key, dotdict in card.data.items():
            if not isinstance(dotdict, DotDict): ret += f"# {dotdict}\n"
        quality = self.quality()
        ret += "*completion*".ljust(20)+ "🧩"*int(quality*20)+"⚠️"*(20-int(quality*20))
        ret += "\n"
        for key, dotdict in card.data.items():
            if isinstance(dotdict, DotDict):
                segment = ""
                for field, value in dotdict.items():
                    if value.strip(): segment += f"{("*"+field.replace("_", " ")+"*").ljust(20)} {value.strip()}\n\n"
                if segment: ret += f"\n## {key.replace("_", " ")}\n"+segment
        return ret

    def to_pydantic(self) -> type[BaseModel]:
        fields = {}
        sub_models = {}

        for key, value in self.data.items():
            if isinstance(value, dict):
                sub_model = create_model(f"card_{key}", **{k: (str, v) for k, v in value.items()})
                sub_models[key] = sub_model
                fields[key] = (sub_model, ...)
            else:
                fields[key] = (str, value)

        pydantic_model = create_model('card', **fields)
        return pydantic_model

    def __str__(self):
        buffer = io.StringIO()
        console = rich.console.Console(file=buffer, force_terminal=True, color_system="truecolor")
        console.print(Markdown(self.to_markdown()))
        return buffer.getvalue().replace("\n\n", "\n")

    def to_html(self):
        return HTMLRenderer(self.to_html_card().data, editable=False).render()

    def json_dumps(self):
        return json.dumps(self.data)

    def save_json(self, filename: str):
        with open(filename, "w") as f:
            f.write(json.dumps(self.data))

    def load_json(self, filename: str):
        with open(filename, "r") as f:
            self.data.assign(json.loads(f.readline()))

    def save_html(self, filename: str):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.to_html())