from .globals import globals

import aicard
import pandas as pd
import copy
import os


def ai_data_summary(file_path, session_id):
    # Read and create ai summary
    data_pd = aicard.evaluation.read_data(file_path)
    ai_data_summ = (
        globals[session_id].aia.dataset_summary(data_pd).replace("\n", "<br>")
    )
    data_extracted_info = aicard.utils._extract_data_info(data_pd)
    return ai_data_summ, data_extracted_info


def construct_html_table_for_data(data_info):
    data_set_outline = '<table id="dataTable" border="0"><thead><tr>'
    for column_name in data_info["column_names"]:
        data_set_outline += f"<th>{column_name}</th>"
    data_set_outline += "</tr></thead>"
    data_set_outline += "<tbody><tr>"
    for column_name in data_info["column_names"]:
        data_set_outline += '<td style="text-align: center;">'
        for key in data_info:
            if (column_name in key) and ("sample" in key):
                data_set_outline += "..."
            elif (column_name in key) and ("number of instances" in key):
                for row in data_info[key]:
                    data_set_outline += f"{row}<br>"
        data_set_outline += "</td>"
    data_set_outline += "</tr></tbody>"
    data_set_outline += "</table>"
    return data_set_outline


def construct_metrics_table_html(metrics, session_id):
    # Construct metrics_table for quantitative_analysis.html
    globals[session_id].metrics_table = (
        '<div style="overflow-x: auto;"><table id="dataTable" border="0"><thead><tr>'
    )
    for column_name in metrics.column_names:
        globals[session_id].metrics_table += f"<th>{column_name}</th>"
    globals[session_id].metrics_table += "</tr></thead>"
    globals[session_id].metrics_table += "<tbody>"
    for line in metrics:
        globals[session_id].metrics_table += "<tr>"
        for column_name in metrics.column_names:
            try:
                globals[
                    session_id
                ].metrics_table += f'<td style="text-align: center;">{round(line[column_name], 4)}</td>'
            except (ValueError, TypeError):
                globals[
                    session_id
                ].metrics_table += (
                    f'<td style="text-align: center;">{line[column_name]}</td>'
                )
        globals[session_id].metrics_table += "</tr>"
    globals[session_id].metrics_table += "</tbody></table></div>"


def construct_terms_tips_table(session_id):
    globals[session_id].terms_tips_table = ""
    for term, tip in globals[session_id].mc.tips.items():
        globals[session_id].terms_tips_table += '<div class="container">'
        globals[
            session_id
        ].terms_tips_table += f'<textarea id="term_{term}">{term}</textarea>'
        globals[
            session_id
        ].terms_tips_table += f'<textarea id="tip_{tip}">{tip}</textarea>'
        globals[
            session_id
        ].terms_tips_table += (
            f'<button class="dynamic-btn" data-button-name="save_{term}">Save</button>'
        )
        globals[
            session_id
        ].terms_tips_table += f'<button class="dynamic-btn" data-button-name="remove_{term}">Remove</button>'
        globals[session_id].terms_tips_table += "</div>"


def construct_model_details_textareas(session_id):
    globals[session_id].model_details_textareas = ""
    for key, text in globals[session_id].mc.text["Model Details"].items():
        globals[session_id].model_details_textareas += '<div class="container">'
        globals[session_id].model_details_textareas += f"<b>{key}</b>"
        globals[
            session_id
        ].model_details_textareas += f'<textarea id="{key}">{text}</textarea>'
        globals[session_id].model_details_textareas += "</div>"


def construct_considerations_fields(session_id):
    globals[session_id].considerations_fields = ""
    for key, text in globals[session_id].mc.text["Considerations"].items():
        globals[session_id].considerations_fields += '<div class="container">'
        globals[session_id].considerations_fields += f"<b>{key}</b>"
        globals[
            session_id
        ].considerations_fields += f'<textarea id="{key}">{text}</textarea>'
        globals[session_id].considerations_fields += "</div>"


def level_of_details_editor(args, session_id):
    if args.button == "Add AI tips":
        for field in globals[session_id].mc.text:
            if field != "Title":
                for text in globals[session_id].mc.text[field].values():
                    globals[session_id].mc.tips = globals[session_id].mc.tips | globals[
                        session_id
                    ].aia._create_hints(text)
        construct_terms_tips_table(session_id)
    elif "remove" in args.button:
        globals[session_id].mc.tips.pop(args.button.split("_", 1)[1])
        construct_terms_tips_table(session_id)
    elif args.button == "Add Tip":
        term = args.user_input.split("<term_divider_tip>")[0]
        tip = args.user_input.split("<term_divider_tip>")[1]
        globals[session_id].mc.tips = globals[session_id].mc.tips | {term: tip}
        construct_terms_tips_table(session_id)
    elif args.button == "Create Level of Details":
        globals[session_id].mcsimplified = copy.deepcopy(globals[session_id].mc)
        globals[session_id].mcwithtips = copy.deepcopy(globals[session_id].mc)
        print("Deepcopy OK")

        if globals[session_id].mc.tips:
            for field in globals[session_id].mc.text:
                if field != "Title":
                    for key in globals[session_id].mc.text[field]:
                        print(
                            f"old globals[session_id].mcwithtips.text[{field}][{key}]"
                            + globals[session_id].mcwithtips.text[field][key]
                        )
                        globals[session_id].mcwithtips.text[field][key] = globals[
                            session_id
                        ].aia._inject_text_with_hints(
                            globals[session_id].mc.text[field][key],
                            globals[session_id].mc.tips,
                        )
                        print(
                            f"new globals[session_id].mcwithtips.text[{field}][{key}]"
                            + globals[session_id].mcwithtips.text[field][key]
                        )

        for field in globals[session_id].mc.text:
            if field != "Title":
                for key in globals[session_id].mc.text[field]:
                    print(
                        f"old globals[session_id].mcsimplified.text[{field}][{key}]"
                        + globals[session_id].mcwithtips.text[field][key]
                    )
                    globals[session_id].mcsimplified.text[field][key] = globals[
                        session_id
                    ].aia.simplify(globals[session_id].mc.text[field][key])
                    print(
                        f"old globals[session_id].mcsimplified.text[{field}][{key}]"
                        + globals[session_id].mcwithtips.text[field][key]
                    )

        session_templates_path = os.path.join("./UI/templates/sessions", session_id)
        globals[session_id].mcsimplified.save(
            f"{session_templates_path}/~model_card_simplified"
        )
        globals[session_id].mcwithtips.save(
            f".{session_templates_path}/~model_card_with_tip"
        )


def model_details_editor(args, session_id):
    if args.button == "Submit from model details":
        for key, text in args.textarea.items():
            globals[session_id].mc.text["Model Details"][key] = text
    elif args.button == "Upload PDF":
        file_path = args.file_path
        globals[session_id].mc.text["Model Details"]["Overview"] += (
            "<br>******** This is AI generated start<br>"
            + globals[session_id].aia.create_overview(file_path).replace("\n", "<br>")
            + "<br>******** This is AI generated stop<br>"
        )
    construct_model_details_textareas(session_id)


def considerations_editor(args, session_id):
    if args.button == "Submit from aichat":
        globals[session_id].suggest_ethical_considerations_chat_list.append(
            {"role": "user", "content": args.user_input}
        )
        ethical_suggestions = globals[session_id].aia.suggest_ethical_considerations(
            full_message_list=globals[
                session_id
            ].suggest_ethical_considerations_chat_list
        )
        globals[session_id].suggest_ethical_considerations_chat_list.append(
            {"role": "assistant", "content": ethical_suggestions}
        )
        globals[session_id].airesponse = ""
        for message in globals[session_id].suggest_ethical_considerations_chat_list:
            globals[session_id].airesponse = (
                globals[session_id].airesponse
                + "\n"
                + message["content"]
                + "\n******************************************"
            )
    elif args.button == "Submit from considerations":
        for key, text in args.textarea.items():
            globals[session_id].mc.text["Considerations"][key] = text
    construct_considerations_fields(session_id)


def training_set_editor(args, session_id):
    if args.button == "Submit from training set":
        globals[session_id].mc.text["Training Set"]["Description"] = args.textarea[
            "training_set"
        ]
    elif args.button == "AI Data Summary Train Set":
        file_path = args.file_path
        aicard.utils._extract_dataset_info.ydata_report(
            path=file_path,
            destination=f"./UI/templates/sessions/{session_id}/ydata_train.html",
        )
        globals[session_id].mc.text["Training Set"][
            "Data Report"
        ] = """<iframe src = "{{ url_for('ydata_train') }}" style = "width:100%; height:90vh; border: 2px solid black; border-radius: 8px;"> </iframe>"""
        # ai_data_summ, globals[session_id].data_extracted_info_train = ai_data_summary(file_path, session_id)
        # globals[session_id].data_set_outline_training = construct_html_table_for_data(globals[session_id].data_extracted_info_train)
        # write and save mc
        # globals[session_id].mc.text['Training Set']["Description"] += '<br>****** AI Data Summary Start*****<br>' + ai_data_summ + '<br>****** AI Data Summary End*****<br>'
        # Create create_plot_buttons for training_set.html
        # globals[session_id].create_plot_buttons_train = "<br><br>Create a plot for:<br>"
        # for column_name in globals[session_id].data_extracted_info_train['column_names']:
        #     for key in globals[session_id].data_extracted_info_train:
        #         if (column_name in key) and ('number of instances' in key):
        #             globals[session_id].create_plot_buttons_train += f'<button class="dynamic-btn" data-button-name="{key}">{column_name}</button>'
    elif "number of instances" in args.button:
        plot_name = ""
        for column_name in globals[session_id].data_extracted_info_train[
            "column_names"
        ]:
            if column_name in args.button:
                plot_name = column_name
                break

        split_data = [
            item.split(": ")
            for item in globals[session_id].data_extracted_info_train[args.button]
        ]
        data_to_plot_pd = pd.DataFrame(split_data, columns=[plot_name, "count"])
        data_to_plot_pd["count"] = pd.to_numeric(data_to_plot_pd["count"])

        globals[session_id].mc.plots["Training Set"][plot_name] = globals[
            session_id
        ].mc.bar_plot(
            pdata=data_to_plot_pd,
            y="count",
            x=plot_name,
            title=plot_name,
            yaxis_title="Number of instances",
        )


def eval_set_editor(args, session_id):
    if args.button == "Submit from eval set":
        globals[session_id].mc.text["Eval Set"]["Description"] = args.textarea[
            "eval_set"
        ]
    elif args.button == "AI Data Summary Eval Set":
        file_path = args.file_path
        aicard.utils._extract_dataset_info.ydata_report(
            path=file_path,
            destination=f"./UI/templates/sessions/{session_id}/ydata_eval.html",
        )
        globals[session_id].mc.text["Eval Set"][
            "Data Report"
        ] = """<iframe src = "{{ url_for('ydata_eval') }}" style = "width:100%; height:90vh; border: 2px solid black; border-radius: 8px;"> </iframe>"""
        # ai_data_summ, globals[session_id].data_extracted_info_eval = ai_data_summary(file_path, session_id)
        # globals[session_id].data_set_outline_eval = construct_html_table_for_data(globals[session_id].data_extracted_info_eval)
        # write and save mc
        # globals[session_id].mc.text['Eval Set']["Description"] += '<br>****** AI Data Summary Start*****<br>' + ai_data_summ + '<br>****** AI Data Summary End*****<br>'
        # Create create_plot_buttons_eval for training_set.html
        # globals[session_id].create_plot_buttons_eval = "<br><br>Create a plot for:<br>"
        # for column_name in globals[session_id].data_extracted_info_eval['column_names']:
        #     for key in globals[session_id].data_extracted_info_eval:
        #         if (column_name in key) and ('number of instances' in key):
        #             globals[session_id].create_plot_buttons_eval += f'<button class="dynamic-btn" data-button-name="{key}">{column_name}</button>'
    elif "number of instances" in args.button:
        plot_name = ""
        for column_name in globals[session_id].data_extracted_info_eval["column_names"]:
            if column_name in args.button:
                plot_name = column_name
                break

        split_data = [
            item.split(": ")
            for item in globals[session_id].data_extracted_info_eval[args.button]
        ]
        data_to_plot_pd = pd.DataFrame(split_data, columns=[plot_name, "count"])
        data_to_plot_pd["count"] = pd.to_numeric(data_to_plot_pd["count"])

        globals[session_id].mc.plots["Eval Set"][plot_name] = globals[
            session_id
        ].mc.bar_plot(
            pdata=data_to_plot_pd,
            y="count",
            x=plot_name,
            title=plot_name,
            yaxis_title="Number of instances",
        )


def quantitative_analysis_editor(args, session_id):
    if args.button == "Submit from quantitative analysis":
        globals[session_id].mc.text["Quantitative Analysis"][
            "Description"
        ] = args.textarea["quantitative_analysis"].replace(
            '<figure class="table"', '<figure class="table" style="overflow-x: auto;"'
        )
    elif args.button == "Upload Metrics":
        file_path = args.file_path
        metrics = aicard.evaluation.read_data(file_path)
        construct_metrics_table_html(metrics, session_id)
        globals[session_id].mc.text["Quantitative Analysis"]["Description"] = (
            globals[session_id].aia.metrics_summary(file_path).replace("\n", "<br>")
            + "<br>"
            + globals[session_id].metrics_table
        )


def call_editor(args, session_id):
    editors = {
        "Model Details": model_details_editor,
        "Considerations": considerations_editor,
        "Training Set": training_set_editor,
        "Eval Set": eval_set_editor,
        "Quantitative Analysis": quantitative_analysis_editor,
        "Level of Details": level_of_details_editor,
    }
    try:
        return editors.get(args.field, lambda x, y: None)(args, session_id)
    except Exception as e:
        print("No valid editor")
        return


def edit_mc(args, session_id):
    print(args)
    call_editor(args, session_id)
    session_templates_path = os.path.join("./UI/templates/sessions", session_id)
    globals[session_id].mc.save(f"{session_templates_path}/~model_card")
