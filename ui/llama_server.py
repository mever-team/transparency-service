# clone and run
# > pip install package
# > python -m ui.test_server
# examples in tests/server.py (also contains full structure of a model card)
#
# .venv serves index.html at http://127.0.0.1:5000
# server specs in http://127.0.0.1:5000/apidocs
# refer to the implementation in package/service/server.py
# The delay below is for how many seconds the test agent will
# pretend to be thinking, so that invalid requests can be tested.

from aicard.service import serve
from aicard.service.assistants import WordNet, Prompter, Combined
from aicard.agents import Ollama
from threading import Thread
from aicard.agents.extensions.embeddings import ImageClassifier

image_classifier = ImageClassifier()
app, gc = serve({
        "run": Combined(
            complete=WordNet(),
            refine=Prompter(
                Ollama("llama3.2:latest", name="🦙 Llama 3.2", timeout_secs=60),
                description="Llama 3.2 is used as the base model.",
                image_classifier=image_classifier),
        )
    },
    env="ui/.env"
)

if __name__ == "__main__":
    Thread(target=gc, daemon=True).start()
    app.run(threaded=False)  # TODO: temporary measure
