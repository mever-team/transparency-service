from modelcard.service.server import serve
from modelcard.service.assistant import TestAssistant
import json
import time

app, gc = serve(
    redirect_index="/docs",
    assistants={"tassist": TestAssistant(delay=0.1)}, # delay is the number of seconds in which no more updates are available
    root=None # non-persistent in-memory database
)

client = app.test_client()
admin = client.post('/login', json={"username": "admin","password": "admin"})
admin = json.loads(admin.data)["token"]

def test_cards():
    response = client.post('/cards', json={})
    assert response.status_code==200
    data = json.loads(response.data)
    assert "results" in data
    assert "pages" in data
    assert len(data)==2
    assert len(data["results"]) == 0

def test_assistants():
    response = client.get('/assistants', headers={"Authorization": f"Bearer {admin}"})
    assert response.status_code==200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data)==1
    assert "name" in data[0]
    assert "desc" in data[0]

def test_creation():
    prev_count = len(json.loads(client.post('/cards', json={}).data)["results"])
    card_id1 = client.post('/card', headers={"Authorization": f"Bearer {admin}"}, json={"title": "My Special Model Card", "model": {"overview": "My cool overview."}})
    card_id2 = client.post('/card', headers={"Authorization": f"Bearer {admin}"}, json={})
    assert card_id1.status_code==201
    assert card_id2.status_code==201
    assert isinstance(json.loads(card_id1.data), int)
    assert isinstance(json.loads(card_id2.data), int)
    assert card_id1.data!=card_id2.data
    assert len(json.loads(client.post(f'/cards', json={}).data)["results"])==prev_count+2

    card_id1 = json.loads(card_id1.data)
    retrieve = json.loads(client.get(f'/card/{card_id1}').data)

    assert retrieve["title"] == "My Special Model Card"
    model = next(item["value"] for item in retrieve["data"] if item["name"]=="model")
    value = next(item["value"] for item in model if item["name"]=="overview")
    assert value=="My cool overview."


def test_creation_dynamic_format():
    prev_count = len(json.loads(client.post('/cards', json={}).data)["results"])
    card_id1 = client.post('/card', headers={"Authorization": f"Bearer {admin}"}, json={
        "title": "My Special Model Card",
        "data": [{"name": "model", "value": [{"name": "overview", "value": "My cool overview."}]}]
    })
    card_id2 = client.post('/card', headers={"Authorization": f"Bearer {admin}"}, json={})
    assert card_id1.status_code==201
    assert card_id2.status_code==201
    assert isinstance(json.loads(card_id1.data), int)
    assert isinstance(json.loads(card_id2.data), int)
    assert card_id1.data!=card_id2.data
    assert len(json.loads(client.post('/cards', json={}).data)["results"])==prev_count+2

    card_id1 = json.loads(card_id1.data)
    retrieve = json.loads(client.get(f'/card/{card_id1}').data)

    assert retrieve["title"] == "My Special Model Card"
    model = next(item["value"] for item in retrieve["data"] if item["name"]=="model")
    value = next(item["value"] for item in model if item["name"]=="overview")
    assert value=="My cool overview."


def test_modify_title():
    card_id = json.loads(client.post('/card', headers={"Authorization": f"Bearer {admin}"}, json={"title": "My Special Model Card"}).data)
    assert json.loads(client.get(f'/card/{card_id}/title').data) == "My Special Model Card"
    assert json.loads(client.put(f'/card/{card_id}/title', headers={"Authorization": f"Bearer {admin}"}, json="My updated title").data) == "My updated title"
    assert json.loads(client.get(f'/card/{card_id}/title').data) == "My updated title"


def test_modify_field():
    card_id = json.loads(client.post('/card', headers={"Authorization": f"Bearer {admin}"}, json={}).data)
    assert json.loads(client.get(f'/card/{card_id}/model/license').data) == ""
    assert json.loads(client.put(f'/card/{card_id}/model/license', headers={"Authorization": f"Bearer {admin}"}, json="Apache 2.0").data) == "Apache 2.0"
    assert json.loads(client.get(f'/card/{card_id}/model/license').data) == "Apache 2.0"


def test_request():
    card_id = json.loads(client.post('/card', headers={"Authorization": f"Bearer {admin}"}, json={}).data)
    # tassist is the assistant's name
    time.sleep(1)
    assert client.post(f'/assistant/tassist/complete/{card_id}', headers={"Authorization": f"Bearer {admin}"}, json="my_url").status_code == 200
    assert client.post(f'/assistant/tassist/complete/{card_id}', headers={"Authorization": f"Bearer {admin}"}, json="my_url").status_code != 200
    assert client.post(f'/assistant/tassist/refine/{card_id}', headers={"Authorization": f"Bearer {admin}"}, json={}).status_code != 200
    assert client.put(f'/card/{card_id}/model/license', headers={"Authorization": f"Bearer {admin}"}, json="Apache 2.0").status_code != 200
    time.sleep(2)
    assert client.post(f'/assistant/tassist/refine/{card_id}', headers={"Authorization": f"Bearer {admin}"}, json={}).status_code == 200
    assert client.post(f'/assistant/tassist/complete/{card_id}', headers={"Authorization": f"Bearer {admin}"}, json="my_url").status_code != 200
    assert client.post(f'/assistant/tassist/refine/{card_id}', headers={"Authorization": f"Bearer {admin}"}, json={}).status_code != 200
    assert client.put(f'/card/{card_id}/model/license', headers={"Authorization": f"Bearer {admin}"}, json="Apache 2.0").status_code != 200
    time.sleep(2)
