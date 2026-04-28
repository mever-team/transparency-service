def test_index(client):
    response = client.get("transparency/index.html")
    assert response.status_code == 200
    
def test_handbook(client):
    response = client.get("transparency/handbook.html")
    assert response.status_code == 200
    
def test_login(client):
    username = "admin"
    password = "admin"
    headers = { "Content-Type": "application/json", "Accept": "application/json" }
    data = { "username": username, "password": password }
    response = client.post('transparency/login', headers=headers, json=data)
    assert response.status_code == 200