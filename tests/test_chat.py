import time
def test_ask_reply_card(client, admin_token, user_card_id):
    # 1. create card
    card_id = user_card_id
    # 2. ask question
    response = client.post(f'/transparency/card/{card_id}/ask', json={"question": "what is the name of the model?"})
    assert response.status_code == 200
    question_id = response.get_json()['id']
    # 3. poll to get reply
    timeout = 300
    start = time.time()
    while True:
        response = client.post(f'/transparency/card/{card_id}/ask/{question_id}')
        data = response.get_json()
        if data['isfinal']:
            break
        if time.time() - start > timeout:
            raise AssertionError(f"Assistant did not finish in time of pytest timeout: {timeout} secs")
        time.sleep(0.5)
    assert response.status_code == 200