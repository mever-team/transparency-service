"""
clone the repository and run the following:
> pip install package
> python -m ui.llama_server
examples in tests/server.py (also contains full structure of a model card)

.venv serves index.html at http://127.0.0.1:5000
refer to the implementation in package/service/server.py
"""

from aicard.service import serve
from aicard.service.assistants import SemanticMatcher, Prompter, Combined
from aicard.service.email import EmailVerification
from aicard.agents import Ollama
from aicard.agents.extensions.speedups import text_compression
from threading import Thread

matcher = SemanticMatcher(
    "sentence-transformers/all-mpnet-base-v2",
    external_get_timeout_sec=3,
    matching_strictness=0.5)
prompter = Prompter(
    Ollama("mistral:latest", name="mistral:latest", timeout_secs=45),
    description="Mistral is used as the base model.",
    text_preprocessor=text_compression
)
agent = Combined(refine=prompter, complete=matcher)
app, gc, monitor = serve(
    {"agent": agent},
    env="ui/.env",
    feature_extractor=matcher,
    email_verification=EmailVerification(env="ui/.env")
)

if __name__ == "__main__":
    Thread(target=gc, daemon=True).start()
    Thread(target=monitor, daemon=True).start()
    app.run(threaded=False)  # TODO: temporarily mandatory
