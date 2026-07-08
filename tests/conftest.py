import pytest
import os
import shutil
import requests
import json
from requests.models import Response

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

from ui.test_server import create_app # ONLY IMPORT AFTER MONKEY PATCHING

@pytest.fixture(scope="session")
def client():
    app, gc, monitor = create_app('db_pytest')
    trai_app = app.test_client()
    return trai_app

@pytest.fixture(scope="session")
def admin_token(client):
    username = "admin"
    password = "admin"
    headers = { "Content-Type": "application/json", "Accept": "application/json" }
    data = { "username": username, "password": password }
    response = client.post("transparency/login", headers=headers, json=data)
    assert response.status_code == 200
    return response.json["token"]

@pytest.fixture(scope="session")
def admin_card_id(client, admin_token):
    response = client.post("/transparency/card", json={"title": ""}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201
    return int(response.data.decode())

@pytest.fixture(scope="session")
def user_token(client):
    username = "pytest"
    password = "pytest"
    headers = { "Content-Type": "application/json", "Accept": "application/json" }
    data = { "username": username, "password": password }
    response = client.post("transparency/login", headers=headers, json=data)
    assert response.status_code == 200
    return response.json["token"]

@pytest.fixture(scope="session")
def user_card_id(client, user_token):
    response = client.post("/transparency/card", json={"title": ""}, headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 201
    return int(response.data.decode())

@pytest.fixture(scope="session", autouse=True)
def cleanup_folder():
    yield  # let all tests run

    folder = "db_pytest"
    if os.path.exists(folder):
        shutil.rmtree(folder)