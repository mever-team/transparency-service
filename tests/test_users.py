def test_login(client):
    username = "admin"
    password = "admin"
    headers = { "Content-Type": "application/json", "Accept": "application/json" }
    data = { "username": username, "password": password }
    response = client.post('transparency/login', headers=headers, json=data)
    assert response.status_code == 200
    
def test_user_register_delete(client, admin_token):
    username = 'pytest_user_register_delete'
    email = 'pytest_user_register_delete@example.com'
    response = client.post('/transparency/register', json={"username": username, "password": "", 'email': email})
    assert response.status_code == 201
    response = client.delete(f'/transparency/users/{username}', headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    
def test_update_password(client, user_token):
    response = client.post('/transparency/update_password', headers={"Authorization": f"Bearer {user_token}"}, json={"password": "newpass"})
    assert response.status_code == 200
    
def test_promote_user(client, admin_token):
    username = 'pytest_promote_user'
    email = 'pytest_promote_user@example.com'
    response = client.post('/transparency/register', json={"username": username, "password": "", 'email': email})
    assert response.status_code == 201
    response = client.post(f'/transparency/users/{username}/accept', headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    response = client.delete(f'/transparency/users/{username}', headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200