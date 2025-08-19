# AI Card

This SDK contains a collection of methods to create, manage, 
and edit AI model cards. Cards can be stored either locally or in
an online service (that can also be self-hosted). We finally provide
methods to automatically populate fields.

*Alpha version - Current apis and functionalities are unstable.*

## ⚡ Quickstart

Clone this repository and install it in your virtual environment per:

```commandline
python -m venv .venv
source .venv/bin/activate
pip install aicard
```

If you are a developer working on this repository, clone it and install it locally
per `pip install -e package` instead. Create your first model card like below.

```python
# demo.py
import aicard as aic

card = aic.ModelCard()
card.title = "Model Card"
card.model.name = "Llama"
card.model.overview = "This is a model overview. Freely add <b>html</b> or *markdown*."
card.model.version = "3.2"
card.considerations.use_case = "text generation"

print(card)
```

```commandline
> python demo.py
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                  Model Card                                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
completion        🧩🧩⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️                                        

                                     model                                      
name               Llama                                                        
overview           This is a model overview. Freely add html or markdown.       
version            3.2                                                       

                                 considerations                                 
use case           text generation   
```


## 🧠 Assistants

Perform manual numerical assessment
across a wide variety of available tasks holding popular
evaluation methodologies and measures. 
If you need customization, you can create your own tasks too. 

```python
aic.evaluation.evaluate(
    data={
        "boxes": [[[300, 100, 315, 150],[300, 100, 315, 150]]],
        "labels": [[0,1]],
        "target": ["labels"]
    },
    pipeline=lambda x:[[x["boxes"][0], x["labels"][0], [0.1,0.9]]], # your model
    task=aic.evaluation.tasks.vision.object_detection,
)
# or you can run ts.evaluation.evaluate(...) to obtain a dictionary of metric values
```

You have the option to collaborate with LLM assistants too!
These let you fill in qualitative aspects of the model card from a software's repository.
In the simplest case, the assistants will be owned by you, but
you can collaborate with the online service too.

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
    model=aic.assistants.olama,
    dotenv=".env" # assistant configuration
)
```

## 🛠️ Hosting a local server

```commandline
python -m venv .venv
source .venv/bin/activate
pip install aicard
```

If you are a developer working on this repository, clone it and install it locally
per `pip install -e package` instead.

Then create a dictionary of assistants and start a flask. This will set up
all required steps. If you want console instead of persistent logging, skip
the `log_file` argument. Below is
an example service whose assistant is primarily used for testing:

```python
from aicard.service import serve, TestAssistant

app = serve("/docs", {"tassist": TestAssistant()}, log_file="log.txt")
app.run()
```

## 📜 License

TBD