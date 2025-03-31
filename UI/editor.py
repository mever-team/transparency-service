import globals
import tkinter as tk
from tkinter import filedialog
import transparency_service
import pandas as pd

def file_dialog():
    # Select a file
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()
    return file_path

def ai_data_summary(file_path):
    # Read and create ai summary
    data_pd = transparency_service.evaluation.read_data(file_path)
    ai_data_summ = globals.aia.dataset_summary(data_pd).replace('\n', '<br>')
    data_extracted_info = transparency_service.utils._extract_data_info(data_pd)
    return ai_data_summ, data_extracted_info

def construct_html_table_for_data(data_info):
    data_set_outline = '<table id="dataTable" border="0"><thead><tr>'
    for column_name in data_info['column_names']:
        data_set_outline += f'<th>{column_name}</th>'
    data_set_outline += '</tr></thead>'
    data_set_outline += '<tbody><tr>'
    for column_name in data_info['column_names']:
        data_set_outline += '<td style="text-align: center;">'
        for key in data_info:
            if (column_name in key) and ('sample' in key):
                data_set_outline += '...'
            elif (column_name in key) and ('number of instances' in key):
                for row in data_info[key]:
                    data_set_outline += f'{row}<br>'
        data_set_outline += '</td>'
    data_set_outline += '</tr></tbody>'
    data_set_outline += '</table>'
    return data_set_outline

def construct_metrics_table_html(metrics):
    # Construct metrics_table for quantitative_analysis.html
    globals.metrics_table = '<div style="overflow-x: auto;"><table id="dataTable" border="0"><thead><tr>'
    for column_name in metrics.column_names:
        globals.metrics_table += f'<th>{column_name}</th>'
    globals.metrics_table += '</tr></thead>'
    globals.metrics_table += '<tbody>'
    for line in metrics:
        globals.metrics_table += '<tr>'
        for column_name in metrics.column_names:
            try:
                globals.metrics_table += f'<td style="text-align: center;">{round(line[column_name], 4)}</td>'
            except (ValueError, TypeError):
                globals.metrics_table += f'<td style="text-align: center;">{line[column_name]}</td>'
        globals.metrics_table += '</tr>'
    globals.metrics_table += '</tbody></table></div>'

def construct_terms_tips_table():
    globals.terms_tips_table = ''
    for term, tip in globals.tips.items():
        globals.terms_tips_table += '<div class="container">'
        globals.terms_tips_table += f'<textarea id="term_{term}">{term}</textarea>'
        globals.terms_tips_table += f'<textarea id="tip_{tip}">{tip}</textarea>'
        globals.terms_tips_table += f'<button class="dynamic-btn" data-button-name="save_{term}">Save</button>'
        globals.terms_tips_table += f'<button class="dynamic-btn" data-button-name="remove_{term}">Remove</button>'
        globals.terms_tips_table += '</div>'

def level_of_details_editor(args):
    if args.button == "Add AI tips":
        globals.tips = globals.tips | globals.aia._create_hints(globals.mc.text['Model Details'])
        globals.tips = globals.tips | globals.aia._create_hints(globals.mc.text['Considerations'])
        globals.tips = globals.tips | globals.aia._create_hints(globals.mc.text['Training Set'])
        globals.tips = globals.tips | globals.aia._create_hints(globals.mc.text['Eval Set'])
        globals.tips = globals.tips | globals.aia._create_hints(globals.mc.text['Quantitative Analysis'])
        construct_terms_tips_table()
    elif "remove" in args.button:
        globals.tips.pop(args.button.split('_',1)[1])
        construct_terms_tips_table()
    elif args.button == "Add Tip":
        print(args.user_input)
        term = args.user_input.split('<term_divider_tip>')[0]
        tip = args.user_input.split('<term_divider_tip>')[1]
        globals.tips = globals.tips | {term: tip}
        construct_terms_tips_table()
    elif args.button == "Create Level of Details":
        if globals.tips:
            globals.mc.text['Model Details'] = globals.aia._inject_text_with_hints(globals.mc.text['Model Details'], globals.tips)
            globals.mc.text['Considerations'] = globals.aia._inject_text_with_hints(globals.mc.text['Considerations'], globals.tips)
            globals.mc.text['Training Set'] = globals.aia._inject_text_with_hints(globals.mc.text['Training Set'], globals.tips)
            globals.mc.text['Eval Set'] = globals.aia._inject_text_with_hints(globals.mc.text['Eval Set'], globals.tips)
            globals.mc.text['Quantitative Analysis'] = globals.aia._inject_text_with_hints(globals.mc.text['Quantitative Analysis'], globals.tips)


def model_details_editor(args):
    if args.button == "Submit from model details":
        globals.mc.text['Model Details'] = args.textarea
    elif args.button == "Upload PDF":
        file_path = file_dialog()
        globals.mc.text['Model Details'] += "<br>******** This is AI generated start<br>" + globals.aia.create_overview(file_path).replace('\n', '<br>') + "<br>******** This is AI generated stop<br>"

def considerations_editor(args):
    if args.button == "Submit from aichat":
        globals.suggest_ethical_considerations_chat_list.append({"role": "user", "content": args.user_input})
        ethical_suggestions = globals.aia.suggest_ethical_considerations(full_message_list = globals.suggest_ethical_considerations_chat_list)
        globals.suggest_ethical_considerations_chat_list.append({"role": "assistant", "content": ethical_suggestions})
        globals.airesponse = ''
        for message in globals.suggest_ethical_considerations_chat_list:
            globals.airesponse = globals.airesponse + '\n' + message['content'] + '\n******************************************'
    elif args.button == "Submit from considerations":
        globals.mc.content['Considerations'] = args.textarea

def training_set_editor(args):
    if args.button == "Submit from training set":
        globals.mc.text['Training Set'] = args.textarea
    elif args.button == "AI Data Summary Train Set":
        file_path = file_dialog()
        ai_data_summ, globals.data_extracted_info_train = ai_data_summary(file_path)
        globals.data_set_outline_training = construct_html_table_for_data(globals.data_extracted_info_train)
        # write and save mc
        globals.mc.text['Training Set'] += '<br>****** AI Data Summary Start*****<br>' + ai_data_summ + '<br>****** AI Data Summary End*****<br>'
        # Create create_plot_buttons for training_set.html
        globals.create_plot_buttons_train = "<br><br>Create a plot for:<br>"
        for column_name in globals.data_extracted_info_train['column_names']:
            for key in globals.data_extracted_info_train:
                if (column_name in key) and ('number of instances' in key):
                    globals.create_plot_buttons_train += f'<button class="dynamic-btn" data-button-name="{key}">{column_name}</button>'
    elif 'number of instances' in args.button:
        plot_name = ''
        for column_name in globals.data_extracted_info_train['column_names']:
            if column_name in args.button:
                plot_name = column_name
                break

        split_data = [item.split(': ') for item in globals.data_extracted_info_train[args.button]]
        data_to_plot_pd = pd.DataFrame(split_data, columns=[plot_name, 'count'])
        data_to_plot_pd['count'] = pd.to_numeric(data_to_plot_pd['count'])

        globals.mc.plots['Training Set'][plot_name] = globals.mc.bar_plot(pdata=data_to_plot_pd, y='count', x=plot_name, title=plot_name, yaxis_title='Number of instances')

def eval_set_editor(args):
    if args.button == "Submit from eval set":
        globals.mc.text['Eval Set'] = args.textarea
    elif args.button == "AI Data Summary Eval Set":
        file_path = file_dialog()
        ai_data_summ, globals.data_extracted_info_eval = ai_data_summary(file_path)
        globals.data_set_outline_eval = construct_html_table_for_data(globals.data_extracted_info_eval)
        # write and save mc
        globals.mc.text['Eval Set'] += '<br>****** AI Data Summary Start*****<br>' + ai_data_summ + '<br>****** AI Data Summary End*****<br>'
        # Create create_plot_buttons_eval for training_set.html
        globals.create_plot_buttons_eval = "<br><br>Create a plot for:<br>"
        for column_name in globals.data_extracted_info_eval['column_names']:
            for key in globals.data_extracted_info_eval:
                if (column_name in key) and ('number of instances' in key):
                    globals.create_plot_buttons_eval += f'<button class="dynamic-btn" data-button-name="{key}">{column_name}</button>'
    elif 'number of instances' in args.button:
        plot_name = ''
        for column_name in globals.data_extracted_info_eval['column_names']:
            if column_name in args.button:
                plot_name = column_name
                break

        split_data = [item.split(': ') for item in globals.data_extracted_info_eval[args.button]]
        data_to_plot_pd = pd.DataFrame(split_data, columns=[plot_name, 'count'])
        data_to_plot_pd['count'] = pd.to_numeric(data_to_plot_pd['count'])

        globals.mc.plots['Eval Set'][plot_name] = globals.mc.bar_plot(pdata=data_to_plot_pd, y='count', x=plot_name, title=plot_name, yaxis_title='Number of instances')


def quantitative_analysis_editor(args):
    if args.button == "Submit from quantitative analysis":
        globals.mc.text['Quantitative Analysis'] = args.textarea.replace('<figure class="table"', '<figure class="table" style="overflow-x: auto;"')
    elif args.button == "Upload Metrics":
        file_path = file_dialog()
        metrics = transparency_service.evaluation.read_data(file_path)
        construct_metrics_table_html(metrics)
        globals.mc.text['Quantitative Analysis'] = globals.aia.metrics_summary(file_path).replace('\n', '<br>') + '<br>' + globals.metrics_table




def call_editor(args):
    editors = {
        'Model Details': model_details_editor,
        'Considerations': considerations_editor,
        'Training Set': training_set_editor,
        'Eval Set': eval_set_editor,
        'Quantitative Analysis': quantitative_analysis_editor,
        'Level of Details': level_of_details_editor,
    }
    return editors.get(args.field, lambda x : None)(args)

def edit_mc(args):
    print(args)
    call_editor(args)
    globals.mc.save('templates/~model_card')