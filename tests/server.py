from modelcard.service.server import serve
from modelcard.service.assistant import TestAssistant
import json
import time

app = serve("/docs", {"tassist": TestAssistant(delay=0.1)})  # delay is the number of seconds in which no more updates are available

client = app.test_client()
def test_cards():
    response = client.post('/cards', json={})
    assert response.status_code==200
    data = json.loads(response.data)
    assert "results" in data
    assert "pages" in data
    assert len(data)==2
    assert len(data["results"]) == 0

def test_assistants():
    response = client.get('/assistants')
    assert response.status_code==200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data)==1
    assert "name" in data[0]
    assert "desc" in data[0]

def test_creation():
    prev_count = len(json.loads(client.post('/cards', json={}).data)["results"])

    card_id1 = client.post('/card', json={"title": "My Special Model Card", "model": {"overview": "My cool overview."}})
    card_id2 = client.post('/card', json={})
    assert card_id1.status_code==200
    assert card_id2.status_code==200
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

    card_id1 = client.post('/card', json={
        "title": "My Special Model Card",
        "data": [{"name": "model", "value": [{"name": "overview", "value": "My cool overview."}]}]
    })
    card_id2 = client.post('/card', json={})
    assert card_id1.status_code==200
    assert card_id2.status_code==200
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
    card_id = json.loads(client.post('/card', json={"title": "My Special Model Card"}).data)
    assert json.loads(client.get(f'/card/{card_id}/title').data) == "My Special Model Card"
    assert json.loads(client.put(f'/card/{card_id}/title', json="My updated title").data) == "My updated title"
    assert json.loads(client.get(f'/card/{card_id}/title').data) == "My updated title"


def test_modify_field():
    card_id = json.loads(client.post('/card', json={}).data)
    assert json.loads(client.get(f'/card/{card_id}/model/license').data) == ""
    assert json.loads(client.put(f'/card/{card_id}/model/license', json="Apache 2.0").data) == "Apache 2.0"
    assert json.loads(client.get(f'/card/{card_id}/model/license').data) == "Apache 2.0"


def test_request():
    card_id = json.loads(client.post('/card', json={}).data)
    # tassist is the assistant' name
    time.sleep(1)
    assert client.post(f'/assistant/tassist/complete/{card_id}', json="my_url").status_code == 200
    assert client.post(f'/assistant/tassist/complete/{card_id}', json="my_url").status_code != 200
    assert client.post(f'/assistant/tassist/refine/{card_id}', json={}).status_code != 200
    assert client.post(f'/card/{card_id}/model/license', json="Apache 2.0").status_code != 200
    time.sleep(2)
    assert client.post(f'/assistant/tassist/refine/{card_id}', json={}).status_code == 200
    assert client.post(f'/assistant/tassist/complete/{card_id}', json="my_url").status_code != 200
    assert client.post(f'/assistant/tassist/refine/{card_id}', json={}).status_code != 200
    assert client.post(f'/card/{card_id}/model/license', json="Apache 2.0").status_code != 200
    time.sleep(2)



# TODO: THE FOLLOWING NEEDS TO BE UPDATED BECAUSE WE HAVE MODIFIED MODEL CARD FIELDS
# def test_submit():
#     card_id = json.loads(client.post('/card', json={}).data)
#     full_card = {
#       "title": "MyCard1",
#       "model": {
#         "name": "MyModel1",
#         "overview": "This is a multiline overview. It may be in various formats internally, but the backend will convert it to html to bring it to the frontend. Always do a round trip of fronend input -> backend -> read value from post request",
#         "version": "v0.0.1",
#         "license": "Apache 2.0",
#         "github": "https://www.google.com",
#         "paper": "Somebody et al., Title (2025)"
#       },
#       "considerations": {
#         "use_case": "This may be formatted as html. Example: This <b>model</b> is used to recognize conditions based on x-ray images.",
#         "limitations": "This may be formatted as html. Example: This model can only be used with x-ray image inputs.",
#         "ethical_risks": "This may be formatted as html. Example: This model can only be used with x-ray image inputs."
#       },
#       "training_set": {
#         "datasets": "This may be formatted as html. Example: <h1>Data gathering</h1>Data were gathered somehow, swometime, somewhere.<h1>Concerns</h1>There was no quality check.",
#         "motivation": "This may be formatted as html. For now, this may have some embedded style tags - we can discuss common tags so that all plots look the same. \n                                  <style>\n                                  .barchart {\n                                    display: flex;\n                                    align-items: flex-end;\n                                    gap: 10px;\n                                    height: 150px;\n                                    width: 300px;\n                                    border-left: 2px solid #333;\n                                    border-bottom: 2px solid #333;\n                                    padding: 10px;\n                                    font-family: sans-serif;\n                                  }\n                                  .bar {\n                                    width: 30px;\n                                    background-color: steelblue;\n                                    text-align: center;\n                                    color: white;\n                                    display: flex;\n                                    justify-content: center;\n                                    align-items: flex-end;\n                                  }\n                                  .bar span {\n                                    writing-mode: vertical-rl;\n                                    transform: rotate(180deg);\n                                    margin-bottom: 5px;\n                                  }\n                                </style>\n                                <h3>Bar Chart (Embedded CSS)</h3>\n                                <div class=\"barchart\">\n                                  <div class=\"bar\" style=\"height: 60px;\"><span>3</span></div>\n                                  <div class=\"bar\" style=\"height: 90px;\"><span>5</span></div>\n                                  <div class=\"bar\" style=\"height: 120px;\"><span>7</span></div>\n                                  <div class=\"bar\" style=\"height: 30px;\"><span>1.5</span></div>\n                                </div>\n                               "
#       },
#       "eval_set": {
#         "datasets": "This may be formatted as html. Example: <h1>Data gathering</h1>Data were gathered somehow, swometime, somewhere.<h1>Concerns</h1>There was no quality check.",
#         "motivation": "This may be formatted as html. For now, this may have some embedded style tags - we can discuss common tags so that all plots look the same. \n                                  <style>\n                                  .barchart {\n                                    display: flex;\n                                    align-items: flex-end;\n                                    gap: 10px;\n                                    height: 150px;\n                                    width: 300px;\n                                    border-left: 2px solid #333;\n                                    border-bottom: 2px solid #333;\n                                    padding: 10px;\n                                    font-family: sans-serif;\n                                  }\n                                  .bar {\n                                    width: 30px;\n                                    background-color: steelblue;\n                                    text-align: center;\n                                    color: white;\n                                    display: flex;\n                                    justify-content: center;\n                                    align-items: flex-end;\n                                  }\n                                  .bar span {\n                                    writing-mode: vertical-rl;\n                                    transform: rotate(180deg);\n                                    margin-bottom: 5px;\n                                  }\n                                </style>\n                                <h3>Bar Chart (Embedded CSS)</h3>\n                                <div class=\"barchart\">\n                                  <div class=\"bar\" style=\"height: 60px;\"><span>3</span></div>\n                                  <div class=\"bar\" style=\"height: 90px;\"><span>5</span></div>\n                                  <div class=\"bar\" style=\"height: 120px;\"><span>7</span></div>\n                                  <div class=\"bar\" style=\"height: 30px;\"><span>1.5</span></div>\n                                </div>\n                               "
#       },
#       "analysis": {
#         "analysis": "This may be formatted as html. Example: This is a short analysis that takes into account the following measures:<ul><li><b>tpr</b> - true positive rates of predicted labels</li><li><b>tnr</b> - true negative rates of predicted labels</li></ul>",
#         "metrics": "This may be formatted as html. For now, this may have some embedded style tags - we can discuss common tags so that all plots look the same. \n                                  <style>\n                                  .barchart {\n                                    display: flex;\n                                    align-items: flex-end;\n                                    gap: 10px;\n                                    height: 150px;\n                                    width: 300px;\n                                    border-left: 2px solid #333;\n                                    border-bottom: 2px solid #333;\n                                    padding: 10px;\n                                    font-family: sans-serif;\n                                  }\n                                  .bar {\n                                    width: 30px;\n                                    background-color: steelblue;\n                                    text-align: center;\n                                    color: white;\n                                    display: flex;\n                                    justify-content: center;\n                                    align-items: flex-end;\n                                  }\n                                  .bar span {\n                                    writing-mode: vertical-rl;\n                                    transform: rotate(180deg);\n                                    margin-bottom: 5px;\n                                  }\n                                </style>\n                                <h3>Bar Chart (Embedded CSS)</h3>\n                                <div class=\"barchart\">\n                                  <div class=\"bar\" style=\"height: 60px;\"><span>3</span></div>\n                                  <div class=\"bar\" style=\"height: 90px;\"><span>5</span></div>\n                                  <div class=\"bar\" style=\"height: 120px;\"><span>7</span></div>\n                                  <div class=\"bar\" style=\"height: 30px;\"><span>1.5</span></div>\n                                </div>\n                               "
#       }
#     }
#     client.post(f'/card/{card_id}',json=full_card)
#     analysis_description = json.loads(client.get(f'/card/{card_id}/analysis/description').data)
#     assert analysis_description.startswith('This may be formatted as html. Example: This is a short analysis')
