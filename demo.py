import transparency_service as ts
import webbrowser

results = ts.evaluation.run(
    data={
        "boxes": [[[300, 100, 315, 150],[300, 100, 315, 150]]],
        "labels": [[0,1]],
        "target": ["labels"]
    },
    pipeline=lambda x:[[x["boxes"][0], x["labels"][0], [0.1,0.9]]],
    task=ts.evaluation.tasks.vision.object_detection,
)

print(results)


"""
card = ts.card.ModelCard()
card.title = "Model Card"
card.model.name = "Llama"
card.model.version = "0.1.0"
card.considerations.use_case = "text generation"

card.save_html(filename="temp.html", editable=False)
webbrowser.open("temp.html")"""
