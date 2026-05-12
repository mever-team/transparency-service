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

with conn.attach(1) as card:
    assert card.title == "my new card"
    card.title = "edited title"

with conn.attach(1) as card:
    assert card.title == "edited title"
