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
from aicard.agents import Ollama
from aicard.service.assistants import WordNet, Prompter
from aicard.agents.extensions.embeddings import ImageClassifier
from threading import Thread

image_classifier = ImageClassifier()
app, gc = serve({"wordnet": WordNet(),
        "qwen": Prompter(
            Ollama("qwen2.5:1.5b", name="🦋 Fast thinker", timeout_secs=10),
            description="Qwen2.5:1.5b is used as the base model.",
            image_classifier=image_classifier),
        "llama": Prompter(
            Ollama("llama3.2:latest", name="🦙 Deep thinker", timeout_secs=30),
            description="Llama 3.2 is used as the base model.",
            image_classifier=image_classifier),
        # "ollama": Prompter(Ollama("mistral:latest", name="🌬️ Mistral"))
    },
    env="ui/.env"
)

if __name__ == "__main__":
    Thread(target=gc, daemon=True).start()
    app.run(threaded=False)  # TODO: temporary measure
