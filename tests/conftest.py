import pytest
import time
import os
import shutil
from ui.test_server import create_app

@pytest.fixture(scope="session")
def client():
    app, gc, monitor = create_app(None)
    trai_app = app.test_client()
    time.sleep(5) # wait for matcher
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

# @pytest.fixture(scope="session", autouse=True)
# def cleanup_folder():
#     yield  # let all tests run

#     folder = "db_pytest"
#     if os.path.exists(folder):
#         shutil.rmtree(folder)