from transparency_service.card import ModelCard
import webbrowser


card = ModelCard()
card.text.title = "Model Card"
card.text.model.name = "Llama"
card.text.model.version = "0.1.0"
card.text.considerations.use_case = "text generation"

card.save_html("temp.html", editable=False)
webbrowser.open("temp.html")

