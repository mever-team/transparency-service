import json
import markdown
import os
import importlib.resources
from jinja2 import Environment, BaseLoader
import copy
import pickle


class _HTMLRenderer:
	def __init__(self, json_data, editable_html):
		import copy
		self.json = copy.copy(json_data)
		self.tabs = []
		self.model_details = ""
		self.title = ""

		# Load the template from the package's templates folder and append css js
		template_content = importlib.resources.read_text("transparency_service.model_card_generator", "template.html")
		css_content = importlib.resources.read_text("transparency_service.model_card_generator", "template.css")
		js_content = importlib.resources.read_text("transparency_service.model_card_generator", "template.js")
		template_content = template_content.replace("""<link rel="stylesheet" href="template.css">""",
                                             "<style>" + css_content + "</style>")
		template_content = template_content.replace("""<script src="template.js"></script>""",
													"<script>" + js_content + "</script>")
		# make editable html if chosen
		if editable_html:
			template_content = template_content.replace("<body>", """<body contenteditable = "true">""")
		self.template_env = Environment(loader=BaseLoader())
		self.template = self.template_env.from_string(template_content)

	def add_tab(self, tab_name, tab_content):
		self.tabs.append({'name': tab_name, 'content': tab_content})

	def delete_tab(self, tab_name):
		self.tabs = [tab for tab in self.tabs if tab['name'] != tab_name]

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
			pattern = r'<moreinfo>(.*?)</moreinfo>'

			# process each match
			def replace_match(match):
				# get the content inside the <moreinfo>...</moreinfo>
				content = match.group(1)
				# recursive
				content = recursive_replace(content)
				# Wrap the content inside the 'add_show_more_info' method and return
				return self.add_show_more_info('+', content)

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
			self.model_details = self.__json_to_html_content(self.json.pop("Model Details"))
		for key, value in self.json.items():
			tab_content = self.__json_to_html_content(value)
			self.add_tab(key, tab_content)

		# Render the final HTML using the Jinja2 template
		return self.template.render(
			title=self.title,
			model_details=self.model_details,
			tabs=self.tabs
			)



class _Utils:
	###################################
	####	saves and loads			###
	###################################
	def save(self, filename: str = 'out', editable_html = False):
		self.save_json(f"{filename}.jsonl")
		self.json_to_html()
		self.save_html(f"{filename}.html")
		self.save_pickle(f"{filename}.pkl")

	def save_pickle(self, filename: str):
		with open(filename, 'wb') as out:
			pickle.dump(self, out, pickle.HIGHEST_PROTOCOL)

	def save_json(self, filename: str):
		with open(filename, 'w') as f:
			f.write(json.dumps(self.text) + "\n")
			f.write(json.dumps(self.plots) + "\n")

	def save_html(self, filename: str):
		with open(filename, 'w', encoding="utf-8") as f:
			f.write(self.html_string)

	def json_to_html(self, editable_html = False):
		self.compile()
		htmlout = _HTMLRenderer(self.compiled, editable_html=editable_html)
		self.html_string = htmlout.json_to_html()

	def load_json(self, filename: str):
		with open(filename, 'r') as f:
			first_line = f.readline()
			if 'format_version' in first_line:
				self.format_version = json.loads(first_line)['format_version']
				self.text = json.loads(f.readline())
			else:
				self.text = json.loads(first_line)
			self.plots = json.loads(f.readline())

	def from_pickle(self, filename: str):
		with open(filename, 'rb') as inp:
			return pickle.load(inp)

	###################################
	####		other utils			###
	###################################
	def _json2content(self):
		for tab_name in self.text:
			if tab_name == "Training Set" or tab_name == "Eval Set" or tab_name == "Quantitative Analysis":
				self.content[tab_name] = ''
				for bullet, content in self.text[tab_name].items():
					self.content[tab_name] += f"<p>{content}</p>"
			elif isinstance(self.text[tab_name], str):
				self.content[tab_name] = self.text[tab_name]
			else:
				self.content[tab_name] = ''
				for bullet, content in self.text[tab_name].items():
					self.content[tab_name] += f"<p><strong>{bullet}:</strong> {content}</p>"
		return self.content

	def compile(self):
		self.compiled = copy.deepcopy(self.text)
		for field in self.compiled:
			if field in self.plots:
				for plot in self.plots[field]:
					self.compiled[field] += self.plots[field][plot]