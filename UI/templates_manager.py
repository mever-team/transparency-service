from .globals import globals
from flask import render_template

def get_templates(args, session_id):
    left_template = None
    right_template = None
    templates = {
        # Considerations
        'Submit from aichat': lambda : (render_template(f'sessions/{session_id}/considerations.html', considerations_fields=globals[session_id].considerations_fields, considerations = globals[session_id].mc.text['Considerations'], airesponse=globals[session_id].airesponse), render_template(f'sessions/{session_id}/menu.html')),
        'Considerations': lambda : (render_template(f'sessions/{session_id}/considerations.html', considerations_fields=globals[session_id].considerations_fields, airesponse=globals[session_id].airesponse, considerations = globals[session_id].mc.text['Considerations']), render_template(f'sessions/{session_id}/menu.html')),
        #'Submit from considerations': lambda : (render_template(f'sessions/{session_id}/~model_card.html'), render_template(f'sessions/{session_id}/menu.html')),
        # Eval Set
        'Eval Set': lambda : (render_template(f'sessions/{session_id}/eval_set.html', eval_set = globals[session_id].mc.text['Eval Set']['Description'], eval_set_plots = ''.join(value for value in globals[session_id].mc.plots['Eval Set'].values()) , data_set_outline_eval = globals[session_id].data_set_outline_eval,create_plot_buttons_eval = globals[session_id].create_plot_buttons_eval), render_template(f'sessions/{session_id}/menu.html')),
        #'Submit from eval set': lambda : (render_template(f'sessions/{session_id}/~model_card.html'), render_template(f'sessions/{session_id}/menu.html')),
        'AI Data Summary Eval Set': lambda: (render_template(f'sessions/{session_id}/eval_set.html',eval_set=globals[session_id].mc.text['Eval Set']['Description'], eval_set_plots = ''.join(value for value in globals[session_id].mc.plots['Eval Set'].values()), data_set_outline_eval=globals[session_id].data_set_outline_eval, create_plot_buttons_eval=globals[session_id].create_plot_buttons_eval), render_template(f'sessions/{session_id}/menu.html')),
        # Training Set
        'Training Set': lambda: (render_template(f'sessions/{session_id}/training_set.html', training_set = globals[session_id].mc.text['Training Set']['Description'], training_set_plots = ''.join(value for value in globals[session_id].mc.plots['Training Set'].values()) , data_set_outline_training = globals[session_id].data_set_outline_training, create_plot_buttons_train = globals[session_id].create_plot_buttons_train), render_template(f'sessions/{session_id}/menu.html')),
        #'Submit from training set': lambda: (render_template(f'sessions/{session_id}/~model_card.html'), render_template(f'sessions/{session_id}/menu.html')),
        'AI Data Summary Train Set': lambda: (render_template(f'sessions/{session_id}/training_set.html', training_set = globals[session_id].mc.text['Training Set']['Description'],data_set_outline_training = globals[session_id].data_set_outline_training,create_plot_buttons_train = globals[session_id].create_plot_buttons_train), render_template(f'sessions/{session_id}/menu.html')),
        # Quantitative Analysis
        'Quantitative Analysis': lambda: (render_template(f'sessions/{session_id}/quantitative_analysis.html', quantitative_analysis = globals[session_id].mc.text['Quantitative Analysis']['Description'],metrics_table = globals[session_id].metrics_table), render_template(f'sessions/{session_id}/menu.html')),
        #'Submit from quantitative analysis': lambda: (render_template(f'sessions/{session_id}/~model_card.html'), render_template(f'sessions/{session_id}/menu.html')),
        'Upload Metrics': lambda: (render_template(f'sessions/{session_id}/quantitative_analysis.html', quantitative_analysis = globals[session_id].mc.text['Quantitative Analysis']['Description'], metrics_table = globals[session_id].metrics_table), render_template(f'sessions/{session_id}/menu.html')),
        # Model Details
        'Model Details': lambda: (render_template(f'sessions/{session_id}/model_details.html', model_details_textareas=globals[session_id].model_details_textareas), render_template(f'sessions/{session_id}/menu.html')),
        #'Submit from model details': lambda: (render_template(f'sessions/{session_id}/~model_card.html'), render_template(f'sessions/{session_id}/menu.html')),
        'Upload PDF': lambda: (render_template(f'sessions/{session_id}/model_details.html', model_details_textareas=globals[session_id].model_details_textareas), render_template(f'sessions/{session_id}/menu.html')),
        # General
        #'Back': lambda: (render_template(f'sessions/{session_id}/~model_card.html'), render_template(f'sessions/{session_id}/menu.html')),
        # Level of Details
        'Level of Details': lambda: (render_template(f'sessions/{session_id}/level_of_details.html',terms_tips_table=globals[session_id].terms_tips_table), render_template(f'sessions/{session_id}/menu.html')),
        'Add Tip': lambda: (render_template(f'sessions/{session_id}/level_of_details.html',terms_tips_table=globals[session_id].terms_tips_table), render_template(f'sessions/{session_id}/menu.html')),
        'Add AI tips': lambda: (render_template(f'sessions/{session_id}/level_of_details.html',terms_tips_table=globals[session_id].terms_tips_table), render_template(f'sessions/{session_id}/menu.html')),
        'remove': lambda: (render_template(f'sessions/{session_id}/level_of_details.html', terms_tips_table=globals[session_id].terms_tips_table),render_template(f'sessions/{session_id}/menu.html')),
        'Model Card with tips': lambda : (render_template(f'sessions/{session_id}/~model_card_with_tip.html'), render_template(f'sessions/{session_id}/menu.html')),
        'Model Card Simplified': lambda: (render_template(f'sessions/{session_id}/~model_card_simplified.html'), render_template(f'sessions/{session_id}/menu.html')),
    }

    b = args.button.split('_',1)[0]
    return templates.get(b, lambda : (render_template(f'sessions/{session_id}/~model_card.html'), render_template(f'sessions/{session_id}/menu.html')))()