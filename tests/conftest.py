import pytest
from ui.llama_server import app

@pytest.fixture(scope="session")
def client():
    return app.test_client()

@pytest.fixture
def auth_token(client):
    username = "admin"
    password = "admin"
    headers = { "Content-Type": "application/json", "Accept": "application/json" }
    data = { "username": username, "password": password }
    response = client.post("transparency/login", headers=headers, json=data)
    assert response.status_code == 200
    return response.json["token"]