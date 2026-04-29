def test_login(client):
    username = "admin"
    password = "admin"
    headers = { "Content-Type": "application/json", "Accept": "application/json" }
    data = { "username": username, "password": password }
    response = client.post('transparency/login', headers=headers, json=data)
    assert response.status_code == 200
    
def test_user_register_delete(client, admin_token):
    username = 'pytest_user_register_delete'
    email = 'pytest@example.com'
    response = client.post('/transparency/register', json={"username": username, "password": "", 'email': email})
    assert response.status_code == 201
    response = client.delete(f'/transparency/users/{username}', headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    