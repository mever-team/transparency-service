import aicard as aic

card = aic.ModelCard()
card.title = "Model Card"
card.model.name = "Llama"
card.model.overview = "This is a model overview. Freely add <b>html</b> or *markdown*."
card.model.version = "0.1.0"
card.considerations.use_case = "text generation"

print(card)
