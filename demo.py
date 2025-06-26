from transparency_service.card import ModelCard
import webbrowser


card = ModelCard()
card.title = "Model Card"
card.model.name = "Llama"
card.model.version = "0.1.0"
card.considerations.use_case = "text generation"

card.save_html(filename="temp.html", editable=False)
webbrowser.open("temp.html")

