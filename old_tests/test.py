from transparency.card import ModelCard, mtplot_to_base64
import matplotlib.pyplot as plt

filename = "val_results"
data = []

with open(filename, "r") as file:
    for line in file.readlines():
        if line.strip() and ":" in line:
            key, values = line.split(":")
            values = values.strip().split("/")
            col1 = float(values[0])
            col2 = float(values[1])
            data.append((key.strip(), col1, col2))

names, col1, col2 = zip(*data)
bar_width = 0.35
x_positions = range(len(names))

plt.figure(figsize=(6, 4))
plt.bar(x_positions, col1, width=bar_width, color="blue")
plt.xlabel("Data Sets")
plt.ylabel("Accuracy (%)")
plt.title("Accuracy on different val data")
plt.xticks([x + bar_width / 2 for x in x_positions], names, rotation=45, ha="right")
plt.subplots_adjust(bottom=0.5)

plt64 = mtplot_to_base64(plt)
mc = ModelCard()
mc.data["Title"] = "Model Card for rine"
mc.get_git_info("mever-team", "rine")
with open("tests/input_for_create_overview.txt", "r") as file:
    input_for_create_openai_overview = file.read()
mc.create_openai_overview(input_for_create_openai_overview)


mc.data["Considerations"]["Use Case"]["0"] = "This is the first use case"
mc.data["Considerations"]["Use Case"]["0"] = "This is the second use case"
mc.data["Considerations"]["Limitations"]["0"] = "This is the first Limitation"
mc.data["Considerations"]["Ethical Considerations"][
    "0"
] = "This is the first Ethical Consideration"

mc.data["Train Set"]["plot"] = plt64

mc.json_to_markdown()
mc.markdown_to_html()
mc.save_json("out.json")
mc.save_markdown("out.md")
mc.save_html("out.html")

mcpdf = ModelCard()
mcpdf.create_openai_json("2402.19091v2.pdf")
mcpdf.json_to_markdown()
mcpdf.markdown_to_html()
mcpdf.save_json("out_from_pdf.json")
mcpdf.save_markdown("out_from_pdf.md")
mcpdf.save_html("out_from_pdf.html")
