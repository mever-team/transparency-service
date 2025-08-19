import os
import shutil
from .globals import Globals, globals

import aicard


def copy_all(source_folder, destination_folder):
    # Copy all files and folders (recursively)
    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)
        destination_path = os.path.join(destination_folder, filename)

        if os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)  # copy2 preserves metadata
        elif os.path.isdir(source_path):
            # If destination folder exists, remove it first to avoid errors
            if os.path.exists(destination_path):
                shutil.rmtree(destination_path)


def init(id: "str path per session"):
    # session specific
    # user_path = os.path.join("sessions", id)
    # os.makedirs(user_path, exist_ok=True)
    default_templates_path = "./UI/templates/default"
    session_templates_path = os.path.join("./UI/templates/sessions", id)
    os.makedirs(session_templates_path, exist_ok=True)
    copy_all(default_templates_path, session_templates_path)
    globals[id] = Globals()

    globals[id].mc = aicard.model_card_generator.ModelCard()
    globals[id].mcwithtips = None
    globals[id].mcsimplified = None
    globals[id].mc.load_json("./UI/model_card.jsonl")

    globals[id].mc.save(f"./UI/templates/sessions/{id}/~model_card")
    globals[id].mc.save(f"./UI/templates/sessions/{id}/~model_card_simplified")
    globals[id].mc.save(f"./UI/templates/sessions/{id}/~model_card_with_tip")
    # globals.aia = transparency_service.ai_assistant.AI_Assistant(model='gpt-3.5-turbo')
    # globals.aia = transparency_service.ai_assistant.AI_Assistant(model='gpt-4')
    # globals.aia = transparency_service.ai_assistant.AI_Assistant(model='llama3.2:3b')
    globals[id].aia = aicard.ai_assistant.AI_Assistant(
        model="llama3.2:latest"
    )

    # training_set.html
    globals[id].data_set_outline_training = ""
    globals[id].create_plot_buttons_train = ""
    globals[id].data_extracted_info_train = ""

    # eval_set.html
    globals[id].data_set_outline_eval = ""
    globals[id].create_plot_buttons_eval = ""
    globals[id].data_extracted_info_eval = ""

    # considerations.html
    globals[id].suggest_ethical_considerations_chat_list = []
    globals[id].airesponse = ""
    globals[id].considerations_fields = ""

    # model_details.html
    globals[id].model_details_textareas = ""

    # quantitative_analysis.html
    globals[id].metrics_table = ""

    print(f"initialization of {id} DONE")
