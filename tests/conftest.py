import pytest
import time
from ui.llama_server import app

@pytest.fixture(scope="session")
def client():
    time.sleep(10) # wait for matcher
    return app.test_client()

@pytest.fixture
def admin_token(client):
    username = "admin"
    password = "admin"
    headers = { "Content-Type": "application/json", "Accept": "application/json" }
    data = { "username": username, "password": password }
    response = client.post("transparency/login", headers=headers, json=data)
    assert response.status_code == 200
    return response.json["token"]