import time
def test_ask_reply_card(client, admin_token):
    # 1. create card
    response = client.post("/transparency/card", json={"title": "pytest_ask_card"}, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201
    card_id = int(response.data.decode())
    # 2. ask question
    response = client.post(f'transparency/card/{card_id}/ask', json={"question": "what is the name of the model?"})
    assert response.status_code == 200
    question_id = response.get_json()['id']
    # 3. poll to get reply
    timeout = 30
    start = time.time()
    while True:
        response = client.post(f'transparency/card/{card_id}/ask/{question_id}')
        data = response.get_json()
        if data['isfinal']:
            break
        if time.time() - start > timeout:
            raise AssertionError(f"Assistant did not finish in time of pytest timeout: {timeout} secs")
        time.sleep(0.5)
    assert response.status_code == 200
    # 4. delete card
    response = client.delete(f"/transparency/card/{card_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 204