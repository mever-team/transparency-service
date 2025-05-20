from . import globals

import transparency_service

def init():
    globals.mc = transparency_service.model_card_generator.ModelCard()
    globals.mcwithtips = None
    globals.mcsimplified = None
    globals.mc.load_json('./UI/model_card.jsonl')

    globals.mc.save('./UI/templates/~model_card')
    globals.mc.save('./UI/templates/~model_card_simplified')
    globals.mc.save('./UI/templates/~model_card_with_tip')
    # globals.aia = transparency_service.ai_assistant.AI_Assistant(model='gpt-3.5-turbo')
    # globals.aia = transparency_service.ai_assistant.AI_Assistant(model='gpt-4')
    # globals.aia = transparency_service.ai_assistant.AI_Assistant(model='llama3.2:3b')
    globals.aia = transparency_service.ai_assistant.AI_Assistant(model='llama3.2:latest')


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
    globals.considerations_fields = ''

    # model_details.html
    globals.model_details_textareas = ''

    # quantitative_analysis.html
    globals.metrics_table = ''

