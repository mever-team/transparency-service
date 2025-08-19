import aicard as aic


conn = aic.connect("http://127.0.0.1:5000", username="admin", password="admin")
with conn.create() as card:
    card.title = "Updated model card name"

print(len(conn.search("updated model card", top=100)))
