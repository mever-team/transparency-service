from aicard.card.fields import Field
from flask import abort
from io import BytesIO
import json


def dynamic2dict(data, mixed: set=None):
    if mixed:
        if not isinstance(data, dict): return dynamic2dict(data)
        if "data" not in data: return dynamic2dict(data)
        for mix in mixed: assert mix in data, f"No {mix} key dictionary key found"
        data_segment = dynamic2dict(data["data"])
        assert isinstance(data_segment, dict), "Data segment could not be parsed into a dictionary"
        return {mix: data[mix] for mix in mixed}|data_segment
    if isinstance(data, list) and all(isinstance(item, dict) and "name" in item and "value" in item for item in data):
        return {item["name"]: dynamic2dict(item["value"]) for item in data}
    return data

def dict2dynamic(data, mixed: set=None):
    if mixed is not None:
        assert isinstance(data, dict)
        for mix in mixed: assert mix in data
        return {mix: data[mix].get() for mix in mixed}|{"data": dict2dynamic({k: v for k, v in data.items() if k not in mixed})}
    if isinstance(data, dict): return [{"name": k, "value": dict2dynamic(v)} if not isinstance(v, Field)
                                       else ({"name":k}|v.__html__()) for k, v in data.items()]
    return data if data else ""

def card2format(card, fformat):
    if fformat == "json":
        content = json.dumps(dict2dynamic(card.data, {"title"})).encode('utf-8')
        filename = f"{card.title}.json"
        mimetype = "text/html"
    elif fformat == "markdown":
        content = card.to_markdown().encode('utf-8')
        filename = f"{card.title}.md"
        mimetype = "text/html"
    elif fformat == "pdf":
        html_content = card.to_html() + """
            <style>
            body {
                margin: 1cm;
                font-size: 12px;
                word-wrap: break-word;
            }
            img {
                max-width: 100%;
                height: auto;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                table-layout: fixed;
                font-size: 11px;
            }
            th, td {
                word-wrap: break-word;
                overflow-wrap: break-word;
                text-overflow: ellipsis;
                padding: 4px;
                border: 1px solid #ccc;
            }
            </style>
            """
        from weasyprint import HTML

        pdf_io = BytesIO()
        HTML(string=html_content).write_pdf(pdf_io)
        pdf_io.seek(0)
        content = pdf_io.read()
        mimetype = "application/pdf"
        filename = f"{card.title}.pdf"
    else:
        abort(400, description="Invalid card conversion format. Must be 'json', 'markdown', or 'pdf.")
    return content, mimetype, filename