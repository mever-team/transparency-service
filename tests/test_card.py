def test_card_create_delete(client, admin_token):
    response = client.post("/transparency/card", json={"title": ""}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201
    card_id = int(response.data.decode())
    response = client.delete(f"/transparency/card/{card_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 204
    
def test_card_clone(client, admin_token, admin_card_id):
    card_id = admin_card_id
    response_clone = client.post(f"/transparency/card/{card_id}/clone", headers={"Authorization": f"Bearer {admin_token}"})
    assert response_clone.status_code == 201
    
def test_get_cards(client):
    response = client.post("/transparency/cards", json={})
    assert response.status_code == 200
    
def test_set_card_field(client, admin_token, admin_card_id):
    card_id = admin_card_id
    response = client.put(f"/transparency/card/{card_id}/overview/name", json={"value": "pytest"}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200

def test_get_card(client, admin_card_id):
    card_id = admin_card_id
    response = client.get(f"/transparency/card/{card_id}")
    assert response.status_code == 200
    
def test_get_card_simple(client, admin_card_id):
    card_id = admin_card_id
    response = client.get(f"/transparency/card/simple/{card_id}")
    assert response.status_code == 200
    
def test_get_card_locked_status(client, admin_card_id):
    card_id = admin_card_id
    response = client.get(f"/transparency/card/{card_id}/locked")
    assert response.status_code == 200
    
def test_get_card_title(client, admin_card_id):
    card_id = admin_card_id
    response = client.get(f"/transparency/card/{card_id}/title")
    assert response.status_code == 200
    
def test_set_card_title(client, admin_token, admin_card_id):
    card_id = admin_card_id
    response = client.put(f"/transparency/card/{card_id}/title", json="pytest_set_card_title", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    
def test_report(client, admin_token, user_card_id):
    card_id = user_card_id
    # report_card
    response = client.post(f"/transparency/card/{card_id}/report", json="pytest_report", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    # get_card_reports
    response = client.get(f"/transparency/reports/{card_id}", json="pytest_report", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.get_json()
    # resolve_card_reports
    response = client.delete(f"/transparency/reports/{card_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 204
    assert not response.get_json()
    
def test_get_card_fields(client):
    response = client.get('/transparency/card/fields')
    assert response.status_code == 200
    
def test_get_card_field_names(client):
    response = client.get('/transparency/card/fields/overview')
    assert response.status_code == 200
    
def test_get_card_field(client, admin_card_id):
    card_id = admin_card_id
    response = client.get(f'/transparency/card/{card_id}/overview/name')
    assert response.status_code == 200
    
def test_update_card(client, admin_token, admin_card_id):
    card_id = admin_card_id
    response = client.get(f"/transparency/card/{card_id}")
    assert response.status_code == 200
    card_json = response.get_json()
    response = client.put(f"/transparency/card/{card_id}", json=card_json, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    
# TODO: unclear what json data should send
def test_update_card_simple(client, admin_token, admin_card_id):
    card_id = admin_card_id
    response = client.get(f"/transparency/card/simple/{card_id}")
    assert response.status_code == 200
    card_json = response.get_json()
    response = client.put(f"/transparency/card/simple/{card_id}", json=card_json, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    
def test_card_job(client, admin_token, admin_card_id):
    card_id = admin_card_id
    response = client.get(f"/transparency/job/{card_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    
def test_download_card(client, admin_card_id):
    card_id = admin_card_id
    response = client.get(f"/transparency/card/{card_id}/download/json")
    assert response.status_code == 200
    # TODO: aborts with 500
    response = client.get(f"/transparency/card/{card_id}/download/markdown")
    assert response.status_code == 200
    response = client.get(f"/transparency/card/{card_id}/download/pdf")
    assert response.status_code == 200
    
    
def test_get_options(client):
    response = client.get(f"/transparency/options/overview/task")
    assert response.status_code == 200
    response = client.get(f"/transparency/options/overview/type")
    assert response.status_code == 200
    response = client.get(f"/transparency/options/overview/name")
    assert response.status_code == 400
    