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
from aicard.service.assistants import WordNet, Prompter
from aicard.agents import Ollama
from threading import Thread

app, gc = serve({"wordnet": WordNet(),
                 # "qwen_fast": Prompter(Ollama("qwen:0.5b", name="🦋 Qwen-small", description="Less accurate but fast LLM.")),
                 #"qwen": Prompter(Ollama("qwen2.5:1.5b", name="🦋 Qwen")),
                 "llama": Prompter(Ollama("llama3.2:latest", name="🦙 Llama")),
                 # "ollama": Prompter(Ollama("mistral:latest", name="🌬️ Mistral"))
                 },
                env="ui/.env")

if __name__ == "__main__":
    Thread(target=gc, daemon=True).start()
    app.run(threaded=False)  # TODO: temporary measure for development
