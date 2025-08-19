import aicard as aic

card = aic.ModelCard()
card.title = "Model Card"
card.model.name = "Llama"
card.model.overview = "This is a model overview. Freely add <b>html</b> or *markdown*."
card.model.version = "3.2"
card.considerations.use_case = "text generation"

print(card)
print("-------------------------------------------------------------------------------")

conn = aic.connect("http://127.0.0.1:5000", username="admin", password="admin")
with conn.create(card) as card:
    card.title = "Updated model card name"
