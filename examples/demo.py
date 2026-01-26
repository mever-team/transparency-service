import aicard as aic

card = aic.ModelCard()
card.title = "Model Card"
card.overview.name = "Llama"
card.overview.description = "This is a model overview. Freely add <b>html</b> or *markdown*."
card.overview.version = "3.2"
card.use.use_cases = "text generation"

print(card)
