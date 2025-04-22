import globals
from flask import render_template

def get_templates(args):
    left_template = None
    right_template = None
    templates = {
        # Considerations
        'Submit from aichat': lambda : (render_template('considerations.html', considerations_fields=globals.considerations_fields, considerations = globals.mc.text['Considerations'], airesponse=globals.airesponse), render_template('menu.html')),
        'Considerations': lambda : (render_template('considerations.html', considerations_fields=globals.considerations_fields, airesponse=globals.airesponse, considerations = globals.mc.text['Considerations']), render_template('menu.html')),
        #'Submit from considerations': lambda : (render_template('~model_card.html'), render_template('menu.html')),
        # Eval Set
        'Eval Set': lambda : (render_template('eval_set.html', eval_set = globals.mc.text['Eval Set']['Description'], eval_set_plots = ''.join(value for value in globals.mc.plots['Eval Set'].values()) , data_set_outline_eval = globals.data_set_outline_eval,create_plot_buttons_eval = globals.create_plot_buttons_eval), render_template('menu.html')),
        #'Submit from eval set': lambda : (render_template('~model_card.html'), render_template('menu.html')),
        'AI Data Summary Eval Set': lambda: (render_template('eval_set.html',eval_set=globals.mc.text['Eval Set']['Description'], eval_set_plots = ''.join(value for value in globals.mc.plots['Eval Set'].values()), data_set_outline_eval=globals.data_set_outline_eval, create_plot_buttons_eval=globals.create_plot_buttons_eval), render_template('menu.html')),
        # Training Set
        'Training Set': lambda: (render_template('training_set.html', training_set = globals.mc.text['Training Set']['Description'], training_set_plots = ''.join(value for value in globals.mc.plots['Training Set'].values()) , data_set_outline_training = globals.data_set_outline_training, create_plot_buttons_train = globals.create_plot_buttons_train), render_template('menu.html')),
        #'Submit from training set': lambda: (render_template('~model_card.html'), render_template('menu.html')),
        'AI Data Summary Train Set': lambda: (render_template('training_set.html', training_set = globals.mc.text['Training Set']['Description'],data_set_outline_training = globals.data_set_outline_training,create_plot_buttons_train = globals.create_plot_buttons_train), render_template('menu.html')),
        # Quantitative Analysis
        'Quantitative Analysis': lambda: (render_template('quantitative_analysis.html', quantitative_analysis = globals.mc.text['Quantitative Analysis']['Description'],metrics_table = globals.metrics_table), render_template('menu.html')),
        #'Submit from quantitative analysis': lambda: (render_template('~model_card.html'), render_template('menu.html')),
        'Upload Metrics': lambda: (render_template('quantitative_analysis.html', quantitative_analysis = globals.mc.text['Quantitative Analysis']['Description'], metrics_table = globals.metrics_table), render_template('menu.html')),
        # Model Details
        'Model Details': lambda: (render_template('model_details.html', model_details_textareas=globals.model_details_textareas), render_template('menu.html')),
        #'Submit from model details': lambda: (render_template('~model_card.html'), render_template('menu.html')),
        'Upload PDF': lambda: (render_template('model_details.html', model_details_textareas=globals.model_details_textareas), render_template('menu.html')),
        # General
        #'Back': lambda: (render_template('~model_card.html'), render_template('menu.html')),
        # Level of Details
        'Level of Details': lambda: (render_template('level_of_details.html',terms_tips_table=globals.terms_tips_table), render_template('menu.html')),
        'Add Tip': lambda: (render_template('level_of_details.html',terms_tips_table=globals.terms_tips_table), render_template('menu.html')),
        'Add AI tips': lambda: (render_template('level_of_details.html',terms_tips_table=globals.terms_tips_table), render_template('menu.html')),
        'remove': lambda: (render_template('level_of_details.html', terms_tips_table=globals.terms_tips_table),render_template('menu.html')),
        'Model Card with tips': lambda : (render_template('~model_card_with_tip.html'), render_template('menu.html')),
        'Model Card Simplified': lambda: (render_template('~model_card_simplified.html'), render_template('menu.html')),
    }

    b = args.button.split('_',1)[0]
    return templates.get(b, lambda : (render_template('~model_card.html'), render_template('menu.html')))()