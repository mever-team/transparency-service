def test_card_create(client, auth_token):
    response = client.post("/transparency/card", json={"title": ""}, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 201
    
def test_card_delete(client, auth_token):
    response = client.post("/transparency/card", json={"title": ""}, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 201
    card_id = int(response.data.decode())
    response = client.delete(f"/transparency/card/{card_id}", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 204
    
def test_card_clone(client, auth_token):
    response = client.post("/transparency/card", json={"title": ""}, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 201
    card_id = int(response.data.decode())
    response = client.post(f"/transparency/card/{card_id}/clone", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 201
    