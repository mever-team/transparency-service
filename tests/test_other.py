def test_admin_dashboard(client, admin_token):
    request = client.get('transparency/users', headers={"Authorization": f"Bearer {admin_token}"})
    assert request.status_code == 200