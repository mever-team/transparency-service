from utils import ModelCard, mtplot_to_base64

mcpdf = ModelCard()
mcpdf.load_json("out_from_pdf.json")
mcpdf.improve_json_with_openai("text_for_improve_json_with_openai.txt")
