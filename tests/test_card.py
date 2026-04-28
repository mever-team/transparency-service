def test_card_create(client, admin_token):
    response = client.post("/transparency/card", json={"title": ""}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201
    
def test_card_delete(client, admin_token):
    response = client.post("/transparency/card", json={"title": ""}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201
    card_id = int(response.data.decode())
    response = client.delete(f"/transparency/card/{card_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 204
    
def test_card_clone(client, admin_token):
    response = client.post("/transparency/card", json={"title": ""}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201
    card_id = int(response.data.decode())
    response = client.post(f"/transparency/card/{card_id}/clone", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201
    
def test_get_cards(client):
    response = client.post("/transparency/cards", json={})
    assert response.status_code == 200
    