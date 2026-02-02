# AI Card

![CI](https://github.com/mever-team/transparency-service/actions/workflows/ci.yml/badge.svg?branch=dev)
![Coverage](https://github.com/mever-team/transparency-service/raw/dev/coverage.svg)


This SDK contains a collection of methods to create, manage, 
and edit AI model cards. Cards can be stored either locally or in
an online service (that can also be self-hosted). We finally provide
methods to populate fields by analyzing datasets, automating popular
types of algorithmic assessment, or calling AI assistants.

*Alpha version - Current apis and functionalities are unstable.*

## ⚡ Quickstart

Install *aicard* in a virtual environment like below.
If you are a developer working on this repository, clone it and install it locally
per `pip install -e package` instead. 

```commandline
python -m venv .venv
source .venv/bin/activate
pip install aicard
```

Create your first model card like below. You can also visit our public service
or self-host a copy of your own to maintain a database of cards and modify
fields through a UI. The *aicard* library makes that hosting possible, allows
programmatic management of cards, and **passes data to the service from your 
local environment**. Those data comprise mainly quantitative evaluation.

```python
# demo.py
import aicard as aic

card = aic.ModelCard()
card.title = "Model Card"
card.overview.name = "Llama"
card.overview.description = "This is a model overview. Freely add <b>html</b> or *markdown*."
card.overview.version = "3.2"
card.use.use_cases = "text generation"

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

There are broadly two types of assistants for model evaluation: quantitative ones that 
evaluate your models based on popular measures, and LLM-based ones that fill in
qualitative information. The last type can also run through services too.

For the first type, perform manual numerical assessment across a wide variety of available 
tasks holding popular evaluation methodologies and measures like below. 
If you need customization, you can create your own tasks. Contributions are welcome too!

```python
# experiment.py
from datasets import load_dataset
from huggingface_hub import dataset_info
from transformers import pipeline
import aicard as aic

dataset = load_dataset("google-research-datasets/go_emotions", split = 'test')
info = dataset_info("google-research-datasets/go_emotions")
class_names = info.card_data['dataset_info'][1]['features'][1]['sequence']['class_label']['names']
classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

def pipeline(data):
    sentences = [text for text in data['text']]
    model_outputs = classifier(sentences)
    out = []
    for sample in model_outputs:
        flat = {d['label']: d['score'] for d in sample}
        out.append([flat[name] for name in class_names.values()])
    return out

metrics = aic.evaluation.evaluate(
    data=dataset,
    pipeline=pipeline,
    task=aic.evaluation.tasks.nlp.text_classification,
    batch_size=32,
    as_card=True
)

print(metrics)
```

```commandline
> python experiment.py
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                         Text Classification Results                          ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
completion        🧩🧩🧩⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️                                       

                                 considerations                                 
software           The following hardware suffices for model running and        
evaluation:                                                                     
- CPU: x86_64                                                                   
- RAM: 31.05 GB                                                                 
- CUDA: | NVIDIA-SMI 570.169 Driver Version: 570.169 CUDA Version: 12.8 |       
inputs outputs     Prediction targets are selected among the following columns, 
if found in the dataset: label, class_name, ground_truth, emotion               

                                    analysis                                    
analysis           Evaluation was conducted at 2025-08-19 for text              
classification with 32 batch size. A pipeline function runs the model.          
metrics            The following metrics were computed at 2025-08-19:           
- precision_macro: 0.575                                                        
- precision_micro: 0.685                                                        
- recall_macro: 0.396                                                           
- recall_micro: 0.511                                                           
- f1_macro: 0.450                                                               
- f1_micro: 0.586                                                               
- auc_roc_macro: 0.929                                                          
thresholds         No thresholds have been applied on metric values computed at 
2025-08-19.       
```

The default `as_card=True` creates a model card that is partially filled with analysis data
automatically obtained from the evaluation process. Otherwise, computed metrics are returned 
as a dictionary of `(name, value)` pairs for manual usage. The default evaluation card,
however, can be merged into another. Merge commands accept an argument to 
signify a merge string message. If that is `None`, then merged values overwrite previous ones:

```python
myinfo = aic.ModelCard()
myinfo.title = "These are my experiments"
myinfo.considerations.use_case = "This tests model card creation"
myinfo.considerations.oversight = "MeVer team"

metrics.merge(myinfo, message=None)

print(metrics)
```

You have the option to collaborate with LLM assistants too!
These let you fill in qualitative aspects of the model card from a software's repository.
In the simplest case, the assistants will be owned by you. Buf, if you want
persistent storage of your cards, you can collaborate with the public or self-hosted service too 
(see below). The assistant will create a copy of the model card with changes applied.

```python
card = card.complete(
    repository="myproject/README.md", # a readme file here
    assistant=aic.service.assist(aic.agents.Ollama())
) # modifies and returns the card
```

You can also use the server's assistants by referencing them by name. In either case, 
in addition to completing the model card, you can also create a copy of it with fields 
summarized by the assistant.

```python
card = card.gist(assistant=conn.assist("ollama")) # NOT IMPLEMENTED YET
```

## 📡 Connecting to a server

You can link to a public or self-hosted server for persistent card storage.
Here we will link to the public server, with can be found at *URL* (you need 
to register as a user first). To work with a server you need to log in with
your credentials. Create a card from the server connection like below. You
can pass on a card to `create` to use as a prototype.

```python
# the credentials bellow are the default for self-hosted servers
conn = aic.connect("URL").login(username="admin", password="admin")  
card = conn.create()  # no argument for a brand new card
```

Alternatively, connect with a dotenv file holding those fields:

```python
conn = aic.connect("URL").login(env=".env")  
card = conn.create()
```

```bash
# .env
USER=admin
PASS=admin
```

You can also search for cards in the server. Cards that you do not own do not 
come with any connection attached, and therefore cannot be used as contexts 
below. To simplify usage, the default argument value `owned_only=True` retrieves
only the cards owned by you.

```python
for card in conn.search("Model Card", owned_only=True, top=10):
    print(card.title)  # treat it as a normal card
```

Submit local card modifications to the server by calling `card.commit()`. 
The card keeps track of the connection. If you fail to do this throughout 
your program, you will eventually get an assertion error. Call `card.detach()` 
to safely detach a card from a connection without commiting 
pending changes (this disables further commits). The best practice is to use 
the card as a context when making changes that require a commit, like below:

```python
conn = aic.connect("http://127.0.0.1:5000", username="admin", password="admin")
with conn.create(card) as card:
    card.title = "Updated model card name"
```

Connections can also substitute `aic` as the module of assistants. 
For safety, you will get an error if you try to call a connection gist 
without commiting the card first, as the server operates in its own copy 
that needs to be updated first.

```python
card = card.gist(model=conn.assistants["olama"])
```

Server load may delay the above snippet, as it blocks until notified by the sever. 
Finally, the server may not support the assistant, for example if it is a custom one.

## 🛠️ Self-hosting a server

If you have *aicard* installed, you can immediately self-host a server.
To do so, create a dictionary of assistants and start a flask service. 
This will set up everything the first time, including a database. 
If you do not plan to expose the server externally, you can login with
the default administrator credentials, like above.
If you want console instead of persistent logging, skip any logger setup. 
Do note that, if an `.env` file is provided, then 
there will be an attempt to retrieve missing arguments from there.
Below is an example service whose assistant is primarily used for testing:

```python
from aicard.service import serve, TestAssistant
from threading import Thread

app, gc = serve({"tassist": TestAssistant(delay=5)}, env=".env")
Thread(target=gc, daemon=True).start()  # needed for long uptimes
app.run(threaded=False)  # current version requires single-threaded run
```

```bash
# .env
INDEX=/apidocs # redirect_index
USER=admin  # admin_username 
PASS=admin  # admin_password
LOG=log.txt # log_file
```

**Garbage collection (gc)** is a callback function that periodically cleans
up resources that are *estimated* as to no longer be in use. This includes 
cleanup of the card access cache and expired tokens. Creating a thread for running 
the `gc` function is required for servers with long uptimes to avoid memory bloat.
However, you can skip spawning a thread for this if host a shorter-time server 
for managing only your own experiments.

## 📜 License

TBD