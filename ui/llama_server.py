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
    matching_strictness=0,
    fuzzer_weight=0.25,
    promote_filling_simple_fields=0.1)
prompter = Prompter(
    Ollama("phi3:latest", name="AI", timeout_secs=60),
    description="Phi3 is used to refine the model card.",
    text_preprocessor=text_compression
)
agent1 = Combined(refine=prompter, complete=matcher, description="<h1>Run</h1>")
#
# matcher = SemanticMatcher(
#     "sentence-transformers/all-mpnet-base-v2",
#     external_get_timeout_sec=3,
#     matching_strictness=0,
#     fuzzer_weight=0.25,
#     promote_filling_simple_fields=0.1,
#     title_importance=0.2,
#     intrusive_rearrange=True,
# ).nostart()
# agent2 = Combined(refine=prompter, complete=matcher, description="<h1>Run & reorganize</h1>")


app, gc, monitor = serve(
    {"agent": agent1},
    env="ui/.env",
    feature_extractor=matcher,
    email_verification=EmailVerification(env="ui/.env")
)

if __name__ == "__main__":
    Thread(target=gc, daemon=True).start()
    Thread(target=monitor, daemon=True).start()
    app.run(threaded=False)  # TODO: temporarily mandatory
