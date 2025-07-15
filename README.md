# Transparency-service

This SDK contains a collection of methods to create, manage, 
and edit AI model cards. It can handle text, lists of data, and plots 
which can be used to populate parts of the cards. We also provide methods 
to automatically populate fields.

## :zap: Quickstart

Clone this repository and install it in your virtual environment per:

```commandline
python -m venv .venv
source .venv/bin/activate
pip install -e package
```

Run manually any evaluation pipeline like so:

```commandline
python -m old_tests.demo
```

## :brain: About

We offer an standardized structure for model cards to be filled
either manually or (semi-)automatically. Here is a manually generated card
that is saved as HTML and previewed in the browser.

```python
import modelcard as mc
import webbrowser

card = mc.ModelCard()
card.title = "Model Card"
card.model.name = "Llama"
card.model.version = "0.1.0"
card.considerations.use_case = "text generation"

card.save_html(filename="temp.html", editable=False)
webbrowser.open("temp.html")
```

You can perform manual numerical assessment
across a wide variety of available tasks holding popular
evaluation methodologies and measures. 
If you need customization, you can create your own tasks too. 
**This functionality is under construction.**

```python
mc.evaluation.evaluate(
    data={
        "boxes": [[[300, 100, 315, 150],[300, 100, 315, 150]]],
        "labels": [[0,1]],
        "target": ["labels"]
    },
    pipeline=lambda x:[[x["boxes"][0], x["labels"][0], [0.1,0.9]]], # your model
    task=mc.evaluation.tasks.vision.object_detection,
)
# or you can run ts.evaluation.evaluate(...) to obtain a dictionary of metric values
```

Finally, you have the option to collaborate with LLM assistants
to fill in qualitative aspects of the model card from a software's repository. 
**This functionality is under construction.**

```python
card.assistant(
    repository="myproject/", # your model's git repository or working directory here
    model=mc.assistants.olama,
    dotenv=".env", # assistant configuration
)
```

The AI assistant can even go a step further and help create a simplified version 
of your model card that is friendlier to laypeople to read and parse through.
**This functionality is under construction.**

```python
card.gist(
    model=mc.assistants.olama,
    dotenv=".env" # assistant configuration
)
```

## :hammer_and_wrench: Hosting a local server

Clone this repository and install it in your virtual environment per:

```commandline
python -m venv .venv
source .venv/bin/activate
pip install -e package
```

Then create a dictionary of assistants and start a flask. Below is
an example service whose assistant is primarily used for testing:

```python
from modelcard.service import serve, TestAssistant

app = serve("/docs", {"tassist": TestAssistant()})
app.run()
```

## :scroll: License

TBD