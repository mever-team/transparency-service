import json
import html2text
import markdown2
import rich
import io

from typing import Union
from rich.markdown import Markdown
from pydantic import BaseModel, create_model
from pydantic import Field as pydantic_Field
from aicard.card.dot_dict import DotDict
from aicard.card.fields import ShortText, LongText, Options, Field, Pattern, Date

def truncate(text, size):
    text = text.strip().split(" ")[0].split("\n")[0].split("/")[-1].strip()
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
            title=ShortText(),
            overview=DotDict(
                name=ShortText("Name of the model."),
                description=LongText("Model purpose, capabilities, novelty and caveats"),
                creator=ShortText("Person or organization developed the model."),
                date=Date("Model development completion date."),
                version=ShortText("Version of the model."),
                type=Options([
                    "#Neural Networks",
                    "Convolutional Neural Network",
                    "Recurrent Neural Network",
                    "Multilayer Perceptron",
                    "Transformer",
                    "Graph Neural Network",
                    "Autoencoder",
                    "Generative Adversarial Network",


                    "#Classical Machine Learning",
                    "Linear Regression",
                    "Logistic Regression",
                    "K-Nearest Neighbors",
                    "Naive Bayes",
                    "Support Vector Machine",
                    "Decision Tree",


                    "#Ensemble Methods",
                    "Random Forest",
                    "Gradient Boosting",
                    "Ensemble Model",


                    "#Unsupervised / Representation Learning",
                    "Clustering Model",
                    "Dimensionality Reduction Model",


                    "#Reinforcement Learning",
                    "Reinforcement Learning Agent",


                    "#Other",
                    "Other",
                    "unknown"
                    ],"Model architecture or algorithm type."),
                task=Options([
                    "#Multimodal",
                    "Audio-Text-to-Text",
                    "Image-Text-to-Text",
                    "Image-Text-to-Image",
                    "Image-Text-to-Video",
                    "Visual Question Answering",
                    "Document Question Answering",
                    "Video-Text-to-Text",
                    "Visual Document Retrieval",
                    "Any-to-Any",
                    
                    "#Computer Vision",
                    "Depth Estimation",
                    "Image Classification",
                    "Object Detection",
                    "Image Segmentation",
                    "Text-to-Image",
                    "Image-to-Text",
                    "Image-to-Image",
                    "Image-to-Video",
                    "Unconditional Image Generation",
                    "Video Classification",
                    "Text-to-Video",
                    "Zero-Shot Image Classification",
                    "Mask Generation",
                    "Zero-Shot Object Detection",
                    "Text-to-3D",
                    "Image-to-3D",
                    "Image Feature Extraction",
                    "Keypoint Detection",
                    "Video-to-Video",
                    
                    "#Natural Language Processing",
                    "Text Classification",
                    "Token Classification",
                    "Table Question Answering",
                    "Question Answering",
                    "Zero-Shot Classification",
                    "Translation",
                    "Summarization",
                    "Feature Extraction",
                    "Text Generation",
                    "Fill-Mask",
                    "Sentence Similarity",
                    "Text Ranking",
                    
                    "#Audio",
                    "Text-to-Speech",
                    "Text-to-Audio",
                    "Automatic Speech Recognition",
                    "Audio-to-Audio",
                    "Audio Classification",
                    "Voice Activity Detection",
                    
                    "#Tabular",
                    "Tabular Classification",
                    "Tabular Regression",
                    "Time Series Forecasting",
                    
                    "#Reinforcement Learning",
                    "Reinforcement Learning",
                    "Robotics",
                    
                    "#Other",
                    "Other",
                    "unknown"
                    ], "Model task."),
                license=LongText("Licence and intellectual property (IP) information."),
                home=ShortText("URL hosting the model."),
                contact=ShortText("Author contact information."),
                citation=LongText("How should the model be cited? Typically includes title, author, year, and publisher. May be a formatted citation or bibtex entries like @article.", technical_nature=True),
                more=LongText("Additional model information not found above.")),
            use=DotDict(
                use_cases=LongText("Intended uses of the model."),
                oversight=Options(["self-learning/autonomous", "human-in-the-loop", "human-on-the-loop", "human-in-command", "unknown"], "Defines the level of human control over the system."),
                user_groups=LongText("Intended users."),
                out_of_scope_use=LongText("Unintended and improper use of model."),
                software=LongText("Software requirements and dependencies?"),
                instructions=LongText("Use instructions.", technical_nature=True),
                inputs_outputs=LongText("Description of the model's inputs and outputs", technical_nature=True),
                factors=LongText("Foreseeable salient factors for which model performance may vary."),
                hardware=LongText("Hardware requirements for training and inference."),
                more=LongText("Additional information about intended uses not found above.", technical_nature=True)),
            training=DotDict(
                datasets=LongText("Dataset(s) used during training."),
                motivation=LongText("Why were training datasets chosen?"),
                preprocessing=LongText("Data pre-processing for training (tokenizer, data augmentation etc.).", technical_nature=True),
                standards=Options(["none", "ISO","IEEE", "unknown"], "Technical or ethical frameworks used that define best practices for safety, quality, transparency, or risk management."),
                update=Options(["no", "yes", "unknown"], "Is tge training set up-to-date, of high quality, complete and representative of the environment the system will be deployed in?"),
                more=LongText("Additional training set information not found above.", technical_nature=True)),
            evaluation=DotDict(
                datasets=LongText("Dataset(s) used during evaluation."),
                motivation=LongText("Why were evaluation datasets chosen?"),
                preprocessing=LongText("Data pre-processing for evaluation (tokenizer, data augmentation etc.).", technical_nature=True),
                standards=Options(["none", "ISO","IEEE", "unknown"], "Technical or ethical frameworks used that define best practices for safety, quality, transparency, or risk management."),
                update=Options(["no", "yes", "unknown"], "Is the evalution set up-to-date, of high quality, complete and representative of the environment the system will be deployed in?"),
                more=LongText("Additional evaluation set information not found above.", technical_nature=True)
            ),
            performance=DotDict(
                analysis=LongText("Analysis and explanation of performance results."),
                metrics=LongText("Benchmark results for any performance metrics.", technical_nature=True),
                thresholds=LongText("If decision thresholds are used, what are they, and why were those parameters chosen?"),
                methodology=LongText("Explanation of how metrics are calculated and averaged, with uncertainty measures and evaluation method."),
                bias=LongText("Performance and bias across different groups (e.g. ethnicity, gender)"),
            ),
            safety=DotDict(
                ethics=LongText("Ethical considerations regarding datasets and usage of model. Recommended mitigation measures."),
                fairness=LongText("Definition of fairness applied in setting up the AI system."),
                risks=LongText("Possible threats to the AI system (design faults, technical faults, environmental threats) and the possible consequences."),
                security=LongText("Is the AI system certified for cybersecurity or is it compliant with specific security standards?"),
                caveats=LongText("Additional concerns that were not covered in the previous sections.")
            ),
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
        if key in self.data:
            ret = self.data[key]
            return ret.get() if isinstance(ret, Field) else ret
        raise AttributeError

    def __setattr__(self, key, value):
        if key in ["data", "connector"]: return object.__setattr__(self, key, value)
        if key in self.data: self.data[key].set(value)
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
        #if self.data.overview.name:
        #    summary += " "+truncate(self.data.overview.name.split(" ")[0].split("\n")[0], 50)
        if self.data.overview.version:
            summary += " "+truncate(self.data.overview.version, 50)
        return summary[1:] if summary else ""

    def quality(self) -> float:
        nom = 0
        denom = 0
        for key, dotdict in self.data.items():
            if isinstance(dotdict, DotDict):
                for field, value in dotdict.items():
                    denom += 1
                    if value: nom += 1
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
                    if isinstance(value, Field): value = value.get()
                    assert isinstance(value, str)
                    card.data[key][field].set(html2text.html2text(value))
        return card

    def to_html_card(self):
        card = ModelCard()
        card.title = self.title
        for key, dotdict in self.data.items():
            if isinstance(dotdict, DotDict):
                for field, value in dotdict.items():
                    if isinstance(value, Field): value = value.get()
                    if not value: value = ""
                    assert isinstance(value, str), f"Field {key} {field} stores type {type(value)} and not a string"
                    # the following line is a trick so that simple strings remain simple strings without <p>
                    value = markdown2.markdown(value, extras=["markdown-in-html", "code-friendly"])
                    if value.startswith("<p>") and value.count("</p>")==1: value = value.strip()[3:-4]
                    card.data[key][field].set(value)
        return card

    def to_markdown(self):
        ret = ""
        card = self.to_markdown_card()
        for key, dotdict in card.data.items():
            if not isinstance(dotdict, DotDict):
                ret += f"# {dotdict.get()}\n"

        # Compute 5-star rating
        quality = self.quality()
        stars = int(round(quality * 5))
        ret += "*completion*".ljust(20) + "⭐" * stars + "☆" * (5 - stars)
        ret += "\n"

        # Add fields
        for key, dotdict in card.data.items():
            if isinstance(dotdict, DotDict):
                segment = ""
                for field, value in dotdict.items():
                    val = value.get().strip()
                    if val and val != "unknown":
                        segment += f"{('*' + field.replace('_', ' ') + '*').ljust(20)} {val}\n\n"

                if segment:
                    ret += f"\n## {key.replace('_', ' ')}\n" + segment
        return ret

    def to_html(self):
        ret = ""
        card = self.to_html_card()
        for key, dotdict in card.data.items():
            if not isinstance(dotdict, DotDict):
                ret += f"<h1>{dotdict.get()}</h1>\n"

        # Compute 5-star rating
        quality = self.quality()
        stars = int(round(quality * 5))
        filled_star = "⭐"
        empty_star = "☆"
        star_html = filled_star * stars + empty_star * (5 - stars)

        ret += (
                f"<div>"
                f"<b>completion</b>".ljust(20)
                + star_html +
                "</div>\n"
        )

        for key, dotdict in card.data.items():
            if isinstance(dotdict, DotDict):
                segment = ""
                for field, value in dotdict.items():
                    v = value.get()
                    val = v.strip() if v else ""
                    if val and str(val) != "unknown":
                        field_label = field.replace("_", " ")
                        segment += f"<p><b>{field_label}</b>: {val}</p>\n"

                if segment:
                    section_title = key.replace("_", " ")
                    ret += f"<h2>{section_title}</h2>\n<div>{segment}</div>\n"

        return f"<div class='card'>{ret}</div>"

    def to_pydantic(self) -> type[BaseModel]:
        fields = {}
        sub_models = {}
        for category, values in self.data.items():
            if not isinstance(values, dict): continue
            sub_model_fields = {}
            for field, value in values.items():
                field_args = {'default': value.get(),'description': value.description}
                if isinstance(value, Options): field_args['enum'] = value.options()
                if isinstance(value, Pattern): field_args['pattern'] = value.pattern()
                sub_model_fields[field] = (str, pydantic_Field(**field_args))
            sub_model = create_model(category, **sub_model_fields)
            sub_models[category] = sub_model
            fields[category] = (sub_model, ...)
        pydantic_model = create_model('card', **fields)
        return pydantic_model

    def json_schema(self):
        schema = self.to_pydantic().model_json_schema()
        return schema

    def to_pydantic_per_category(self) -> dict[str, BaseModel]:
        models = {}
        for category, values in self.data.items():
            if not isinstance(values, dict): continue
            model_fields = {}
            for field, value in values.items():
                field_args = {'default': value.get(),'description': value.description}
                if isinstance(value, Options): field_args['enum'] = value.options()
                if isinstance(value, Pattern): field_args['pattern'] = value.pattern()
                model_fields[field] = (str, pydantic_Field(**field_args))
            model = create_model(category, **model_fields)()
            models[category] = model
        return models

    def json_schema_per_category(self):
        schemas = {category: model.model_json_schema() for category, model in self.to_pydantic_per_category().items()}
        return schemas

    def __str__(self):
        buffer = io.StringIO()
        console = rich.console.Console(file=buffer, force_terminal=True, color_system="truecolor")
        console.print(Markdown(self.to_markdown()))
        return buffer.getvalue().replace("\n\n", "\n")

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
