def test_local_card_creation(client):
    import aicard as aic
    card = aic.ModelCard()
    card.title = "Model Card"
    card.overview.name = "Llama"
    card.overview.description = "This is a model overview. Freely add <b>html</b> or *markdown*."
    card.overview.version = "3.2"
    card.use.use_cases = "text generation"
    # check that some information is actually there now
    new_card = aic.ModelCard()
    new_card.assign(card) # check that assignment works correctly too
    assert new_card.title == "Model Card"
    assert new_card.use.use_cases == "text generation"
    assert new_card.overview.version == "3.2"
    assert "text generation" in str(new_card) # check that string conversion works correctly too

def test_remote_card_creation():
    # try local card attached to an actually spawned server
    import aicard as aic
    import multiprocessing
    import time
    def start_server():
        app, gc, monitor = aic.service.serve(root="", admin_username="admin", admin_password="admin", silent=True)
        app.run(threaded=False)
    multiprocessing.Process(target=start_server, daemon=True).start()
    time.sleep(2)
    conn = aic.connect("http://127.0.0.1:5000", username="admin", password="admin", silent=True)
    with conn.create() as card:
        card.title = "my new card"
        card_id = card.connector.id
    with conn.attach(card_id) as card:
        assert card.title == "my new card"
        card.title = "edited title"
    with conn.attach(card_id) as card:
        assert card.title == "edited title"
