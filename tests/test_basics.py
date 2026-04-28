def test_index(client):
    response = client.get("transparency/index.html")
    assert response.status_code == 200
    
def test_handbook(client):
    response = client.get("transparency/handbook.html")
    assert response.status_code == 200
    
def test_ping(client):
    response = client.get("transparency/ping")
    assert response.status_code == 200
    
def test_ping_admin(client, admin_token):
    response = client.get("transparency/ping", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200