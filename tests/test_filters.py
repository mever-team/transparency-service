def test_filters_query(client):
    response = client.post("/transparency/cards", json={'query': 'ri'})
    assert response.status_code == 200
    response = client.post("/transparency/cards", json={'query': 'rine'})
    assert response.status_code == 200

