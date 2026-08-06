"""
clone the repository and run the following:
> pip install package
> python -m ui.llama_server
examples in tests/server.py (also contains full structure of a model card)

.venv serves index.html at http://127.0.0.1:5000
refer to the implementation in package/service/server.py
"""
import os, shutil, signal, sys
import requests
import json
from requests.models import Response
from flask import jsonify

# MONKEY PATCH THE COMMUNICATION LAYER WITH OLLAMA
_original_get = requests.get
_original_post = requests.post
def _fake_response(url: str, **kwargs):
    class FakeRaw:
        def close(self):
            pass
    class FakeResponse(Response):
        def __init__(self, url, stream=False):
            super().__init__()
            self.status_code = 200
            self.url = url
            self.encoding = "utf-8"
            self._stream = stream
            self._json = {"message": { "content": "TEST MONKEYPATCH" }, "done": True,}
            self._content = json.dumps(self._json).encode("utf-8")
            self.raw = FakeRaw()
        def json(self, **kwargs):
            return self._json
        def iter_lines(self, *args, decode_unicode=False, **kwargs):
            for line in [self._json]:
                data = json.dumps(line)
                yield data if decode_unicode else data.encode("utf-8")
    return FakeResponse(url, **kwargs)
def patched_get(url, *args, **kwargs):
    if url.startswith("http://localhost:11434"): return _fake_response(url, stream=kwargs.get("stream", False))
    return _original_get(url, *args, **kwargs)
def patched_post(url, *args, **kwargs):
    if url.startswith("http://localhost:11434"): return _fake_response(url, stream=kwargs.get("stream", False))
    return _original_post(url, *args, **kwargs)
requests.get = patched_get
requests.post = patched_post

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
    Ollama("mistral:latest", name="🌬️ Mistral", timeout_secs=45),
    description="Mistral is used as the base model.",
    text_preprocessor=text_compression
)
agent = Combined(refine=prompter, complete=matcher)
app, gc, monitor = serve(
    {"agent": agent},
    env="ui/.env",
    feature_extractor=matcher,
    email_verification=EmailVerification(env="ui/.env"), 
    max_agents_per_user = 99,
    root='db_pytest'
)

def cleanup_folder(signal, frame):
    folder = "db_pytest"
    if os.path.exists(folder):
        shutil.rmtree(folder)
    sys.exit(0)
signal.signal(signal.SIGINT, cleanup_folder)

        
if __name__ == "__main__":
    Thread(target=gc, daemon=True).start()
    Thread(target=monitor, daemon=True).start()
    app.run(threaded=False)  # TODO: temporarily mandatory
