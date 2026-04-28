def test_card_create(client, auth_token):
    response = client.post("/transparency/card", json={"title": ""}, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 201
    