import transparency_service

mc = transparency_service.model_card_generator.ModelCard()
ai = transparency_service.ai_assistant.AI_Assistant(model_card=mc)  # llama default
# ai = transparency_service.ai_assistant.AI_Assistant(model = 'gpt', model_card=mc)


ai.create_openai_json("2402.19091v2.pdf")
with open("../input_for_create_overview.txt", "r") as file:
    input_txt = file.read()
ai.create_overview(input_txt)
mc.git_get_license("mever-team", "rine")


# create test plot
# mcpdf.create_bar_plot("Sales Data", "Products", "Sales")
# mcpdf.append_bar_to_plot("Sales Data", "Product A", 50)
# mcpdf.append_bar_to_plot("Sales Data", "Product B", 75)
# mcpdf.append_bar_to_plot("Sales Data", "Product C", 100)
# mcpdf.add_plot_to("Sales Data", 'Testing')


# mc.save(editable_html=True)
