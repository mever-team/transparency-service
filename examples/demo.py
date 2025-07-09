import modelcard as mc
import webbrowser

card = mc.ModelCard()
card.title = "Model Card"
card.model.name = "Llama"
card.model.overview = "This is a model overview. Freely add <b>html</b> or *markdown*."
card.model.version = "0.1.0"
card.considerations.use_case = "text generation"

#card.save_html(filename="temp.html")
#webbrowser.open("temp.html")
print(card)
