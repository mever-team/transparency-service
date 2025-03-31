import globals

import transparency_service

def init():
    globals.mc = transparency_service.model_card_generator.ModelCard()
    globals.mc.load_json('model_card.jsonl')
    if globals.mc.format_version == '1.0':
        globals.mc.text = globals.mc._json2content()

    globals.mc.save('templates/~model_card')
    globals.aia = transparency_service.ai_assistant.AI_Assistant(model='gpt-3.5-turbo')
    #globals.aia = transparency_service.ai_assistant.AI_Assistant(model='gpt-4')
    #globals.aia = transparency_service.ai_assistant.AI_Assistant(model='meta-llama/Llama-3.2-3B-Instruct')

    # training_set.html
    globals.data_set_outline_training = ''
    globals.create_plot_buttons_train = ''
    globals.data_extracted_info_train = ''

    # eval_set.html
    globals.data_set_outline_eval = ''
    globals.create_plot_buttons_eval = ''
    globals.data_extracted_info_eval = ''

    # considerations.html
    globals.suggest_ethical_considerations_chat_list = []
    globals.airesponse = ''

    # quantitative_analysis.html
    globals.metrics_table = ''

    # level of details
    globals.tips = {}
