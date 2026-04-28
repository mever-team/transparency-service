import time
def test_import_url(client, admin_token):
    # 1. create card
    url = 'https://arxiv.org/html/2402.19091v2'
    response = client.post("/transparency/card", json={"title": "pytest_import_url"}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201
    card_id = int(response.data.decode())
    # 2. start assistant process
    response = client.post(
        f"/transparency/assistant/agent/complete/{card_id}", 
        headers={"Authorization": f"Bearer {admin_token}"},
        json=url,
    )
    assert response.status_code == 200
    # 3. poll until finish
    time.sleep(1) # Give time to start 
    timeout = 30
    start = time.time()
    while True:
        response = client.get(f"/transparency/card/{card_id}/locked", headers={"Authorization": f"Bearer {admin_token}"})
        data = response.get_json()
        if data == "" or data is None:
            break
        if time.time() - start > timeout:
            raise AssertionError(f"Assistant did not finish in time of pytest timeout: {timeout} secs")
        time.sleep(0.5)
    assert response.status_code == 200
    
    
def test_refine(client, admin_token):
    # 1. create card
    response = client.post("/transparency/card", json={"title": "pytest_refine"}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201
    card_id = int(response.data.decode())
    # 2. start refine
    response = client.post(
        f"/transparency/assistant/agent/refine/{card_id}", 
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    # 3. poll until finish
    time.sleep(2) # Give time for Ollama 
    timeout = 60
    start = time.time()
    while True:
        response = client.get(f"/transparency/job/{card_id}", headers={"Authorization": f"Bearer {admin_token}"})
        data = response.get_json()
        if not data:
            break
        if time.time() - start > timeout:
            raise AssertionError(f"Assistant did not finish in time of pytest timeout: {timeout} secs")
        time.sleep(0.5)
    assert response.status_code == 200
    