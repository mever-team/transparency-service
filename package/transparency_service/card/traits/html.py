import re
import copy
from importlib.resources import read_text as read
from jinja2 import Environment, BaseLoader
from typing import TypeAlias
JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None


class HTMLRenderer:
    def __init__(self, data: JSON, edit: bool=False):
        self.json = copy.copy(data)  # TODO: why is this needed?
        self.tabs = []
        self.model_details = ""
        self.title = ""

        package = "transparency_service.card.traits.html_template"
        template = (
            read(package, "template.html")
            .replace(
                """<link rel="stylesheet" href="template.css">""",
                "<style>" + read(package, "template.css") + "</style>",
            )
            .replace(
                """<script src="template.js"></script>""",
                "<script>" + read(package, "template.js") + "</script>",
            )
        )
        if edit:
            template = template.replace("<body>", """<body contenteditable = "true">""")
        self.template_env = Environment(loader=BaseLoader())
        self.template = self.template_env.from_string(template)

    def add_tab(self, tab_name, tab_content):
        self.tabs.append({"name": tab_name, "content": tab_content})

    def delete_tab(self, tab_name):
        self.tabs = [tab for tab in self.tabs if tab["name"] != tab_name]

    def add_show_more_info(self, title, content):
        show_more_html = f"""
	    <div class="show-more-container">
	        <button class="show-more-btn" onclick="toggleShowMoreContent(this)">{title}</button>
	        <div class="show-more-content" style="display: none;">
	            {content}
	        </div>
	    </div>
	    """
        return show_more_html

    def process_moreinfo_sections(self, input_string):
        def recursive_replace(string):
            # pattern to find
            pattern = r"<moreinfo>(.*?)</moreinfo>"

            # process each match
            def replace_match(match):
                # get the content inside the <moreinfo>...</moreinfo>
                content = match.group(1)
                # recursive
                content = recursive_replace(content)
                # Wrap the content inside the 'add_show_more_info' method and return
                return self.add_show_more_info("+", content)

            # Replace all <moreinfo>...</moreinfo> occurrences with the processed version
            return re.sub(pattern, replace_match, string, flags=re.DOTALL)

        # Start the recursive replacement process
        return recursive_replace(input_string)

    def __json_to_html_content(self, data, level=1):
        html_content = ""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    # Add sub-section header
                    html_content += f"<h{level}>{key}</h{level}>"
                    html_content += self.__json_to_html_content(value, level + 1)
                else:
                    # Key-Value pair
                    if value.startswith('<div class="plot-inline-div">'):
                        html_content += f"{value}"
                    elif key == "Text":
                        html_content += f"<p>{value}</p>"
                    else:
                        html_content += f"<p><strong>{key}:</strong> {value}</p>"
        elif isinstance(data, list):
            # Render lists as bullet points
            html_content += "<ul>"
            for item in data:
                html_content += f"<li>{self.__json_to_html_content(item, level)}</li>"
            html_content += "</ul>"
        elif isinstance(data, str):
            # Handle images or regular text
            if data.startswith(("data:image/png;base64,", "data:image/jpeg;base64,")):
                html_content += f'<img src="{data}" alt="Image" style="max-width:100%;height:auto;">'
            else:
                html_content += f"<p>{data}</p>"
        else:
            # Render other data types (numbers, booleans, etc.)
            html_content += f"<p>{data}</p>"
        return html_content

    def json_to_html(self):
        if "Title" in self.json:
            self.title = self.json.pop("Title")
        if "Model Details" in self.json:
            self.model_details = self.__json_to_html_content(
                self.json.pop("Model Details")
            )
        for key, value in self.json.items():
            tab_content = self.__json_to_html_content(value)
            self.add_tab(key, tab_content)

        # Render the final HTML using the Jinja2 template
        return self.template.render(
            title=self.title, model_details=self.model_details, tabs=self.tabs
        )
