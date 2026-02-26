# clone and run
# > pip install package
# > python -m ui.test_server
# examples in tests/server.py (also contains full structure of a model card)
#
# .venv serves index.html at http://127.0.0.1:5000
# server specs in http://127.0.0.1:5000/apidocs
# refer to the implementation in package/service/server.py

from aicard.service import serve
from aicard.service.assistants import SemanticMatcher, Prompter, Combined
from aicard.agents import Ollama
from threading import Thread
from aicard.agents.extensions.embeddings import ImageClassifier
from aicard.service.email import EmailVerification

image_classifier = ImageClassifier()
matcher = SemanticMatcher(
    "sentence-transformers/all-mpnet-base-v2",
    external_get_timeout_sec=10,
    matching_strictness=0.5
)
prompter = Prompter(
    Ollama("mistral:latest", name="🌬️ Mistral", timeout_secs=45),
    description="Mistral is used as the base model.",
    image_classifier=image_classifier
)
app, gc = serve(
    {"agent": Combined(complete=matcher, refine=prompter)},
    env="ui/.env",
    feature_extractor=matcher,
    email_verification=EmailVerification(env="ui/.env")
)

if __name__ == "__main__":
    Thread(target=gc, daemon=True).start()
    app.run(threaded=False)  # TODO: temporary measure
