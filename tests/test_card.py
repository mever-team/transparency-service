def test_card_create_delete(client, admin_token):
    response = client.post("/transparency/card", json={"title": ""}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201
    card_id = int(response.data.decode())
    response = client.delete(f"/transparency/card/{card_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 204
    
def test_card_clone(client, admin_token):
    response = client.post("/transparency/card", json={"title": ""}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201
    card_id = int(response.data.decode())
    response_clone = client.post(f"/transparency/card/{card_id}/clone", headers={"Authorization": f"Bearer {admin_token}"})
    assert response_clone.status_code == 201
    response = client.delete(f"/transparency/card/{card_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 204
    card_id = int(response_clone.data.decode())
    response = client.delete(f"/transparency/card/{card_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 204
    
def test_get_cards(client):
    response = client.post("/transparency/cards", json={})
    assert response.status_code == 200
    
def test_set_field(client, admin_token):
    response = client.post("/transparency/card", json={"title": ""}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201
    card_id = int(response.data.decode())
    response = client.put(f"/transparency/card/{card_id}/overview/name", json={"value": "pytest"}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    response = client.delete(f"/transparency/card/{card_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 204