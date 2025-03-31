import openai
import PyPDF2
import os
import json
from typing import List, Union, Optional
import transformers
import torch
import importlib.resources
from ..utils._extract_dataset_info import _extract_data_info
import re
import ast

class AI_Assistant:
	def __init__(self, model = "meta-llama/Llama-3.2-3B-Instruct", model_card = None):
		# gpt-3.5-turbo
		if 'gpt' in model:
			openai.api_key = os.getenv("OPENAI_API_KEY")
			self.model_type = 'gpt'
			self.model = model
		elif 'llamma' in model or 'Llama' in model:
			self.pipeline = transformers.pipeline(
				"text-generation",
				model=model,
				model_kwargs={"torch_dtype": torch.bfloat16},
				device_map="auto",
			)
			self.model_type = 'llama'
		self.model_card = model_card
		self.pdf_chunks_for_llm = []

	def _create_hints(self, text: "str"):
		messages = [{"role": "system",
					 "content": '''
							 You will be given a text. Your goal is to provide explanation for all technical words so a non expert can understand its content. Your output should be a JSON where the keys will be the word to be explained and the values will be the explanation of this word.							 
							 		 '''},
					{"role": "user", "content": f'{re.sub(r"<.*?>", " ", text).strip()}'}]
		tips = self.__run_model(messages, max_tokens=4000, temperature=0.7, top_p=1)

		# extract JSON
		match = re.search(r'\{.*\}', tips.replace('\n',''))
		if match:
			dict_string = match.group(0)
			# Convert string to dictionary
			try:
				tips = ast.literal_eval(dict_string)
			except (ValueError, SyntaxError) as e:
				print(f"Error converting string to dictionary: {e}")
		else:
			print("No dictionary found in the string.")

		return tips


	def _inject_text_with_hints(self, text: "str", tips: "dict"):
		# inject text with tips
		pattern = re.compile('|'.join(re.escape(key) for key in tips.keys()), re.IGNORECASE)
		def replacement_function(match):
			matched_text = match.group(0)
			# Find the corresponding value in the dictionary, ignoring case
			key = next(key for key in tips.keys() if key.lower() == matched_text.lower())
			value = tips[key]
			# Preserve the original case of the matched text
			#return f'<span class="default">{matched_text}<span class="tooltiptext">{value}</span></span>'
			return f'<span class="tooltip">{matched_text}<span class="tooltiptext">{value}</span></span>'

		return pattern.sub(replacement_function, text)


	def dataset_summary(self, dataset: "path to csv, json, tsv, parquet and more or dict, list, datasets.Dataset", anns = [None]):
		dataset_info = _extract_data_info(dataset, anns=anns)
		messages = [{"role": "system",
					 "content":
					 '''You will be given a Python dictionary containing information about a dataset. Your goal is to produce an informative description of the dataset and its purpose. Focus on presenting the content naturally, avoid mentioning the dictionary given and pretend as if the reader doesn't know of its existence. Don't use sentences like "this column contains that information and that column contains that information" instead use sentences like "the dataset contains this and that information". Instead, describe the data as a whole, mentioning its structure and what it contains. Discuss any imbalances providing the number of instances, and write the description as if it were part of an academic paper. Avoid making assumptions about the data beyond what is explicitly stated'''
					 # '''
					 # You will be given a python dictionary with various dataset information. Your goal is to produce an informative description of the dataset, and its purpose. Mention if there are imbalances or not. Avoid using bullet points, instead write as if this is part of a paper. Also do not make any assumptions of what the information you are given means. Your output should include information that is given to you or are logically derived by them.
					 # '''
					 },
					{"role": "user", "content": f'{dataset_info}'}]
		summary = self.__run_model(messages, max_tokens=4000, temperature=0.7, top_p=1)
		print(summary)
		return summary

	def metrics_summary(self, metrics_file_path: "path to jsonl", anns = [None]):
		with open(metrics_file_path, 'r') as file:
			metrics_str = file.read()
		messages = [{"role": "system",
					 "content":
					 '''You will be given a jsonl containing metrics. Your goal is to produce an informative analysis of the model based on these metrics. Focus on presenting the content naturally, do not be too thorough since the user will be given a table with the metrics. Instead highlight the most important results. Along with your answer you should also include what the metrics mean in a real world use. Description as if it were part of an academic paper. Avoid making assumptions beyond what is explicitly stated'''
					 # '''
					 # You will be given a python dictionary with various dataset information. Your goal is to produce an informative description of the dataset, and its purpose. Mention if there are imbalances or not. Avoid using bullet points, instead write as if this is part of a paper. Also do not make any assumptions of what the information you are given means. Your output should include information that is given to you or are logically derived by them.
					 # '''
					 },
					{"role": "user", "content": f'{metrics_str}'}]
		summary = self.__run_model(messages, max_tokens=4000, temperature=0.7, top_p=1)
		print(summary)
		return summary

	def suggest_ethical_considerations(self,
									   user_prompt: str= '',  # The raw text
									   output_file: str = "",  # If specified output to this file
									   full_message_list = None
									   ) -> Optional[Union[str, bool]]:
		messages = [{"role": "system",
					 "content": """You are an expert in ethical AI and technology. Your role is to provide detailed and nuanced ethical considerations for any given AI system or machine learning application. 
					 Consider the following categories: 
					 - misuse and dual-use concerns, 
					 - bias and fairness, 
					 - privacy and data security, 
					 - transparency and accountability, 
					 - societal impact, 
					 - environmental sustainability, 
					 - safety and reliability, 
					 - equity and accessibility, 
					 - legal and regulatory challenges.

					 You do not need to address all of these categories in every response. Instead, assess the context of the AI system or application being evaluated and decide which categories are most relevant. Address only those that are crucial, explaining the potential risks, providing examples when applicable, and suggesting mitigation strategies where necessary. Your responses should be tailored, comprehensive, and structured, with a focus on the most important ethical aspects for the given case."""
					 }]
		if full_message_list is None:
			messages.append({"role": "user", "content": user_prompt})
		else:
			messages.extend(full_message_list)

		ethics = self.__run_model(messages, max_tokens=4000, temperature=0.7, top_p=1)

		if output_file:
			with open(output_file, "w", encoding="utf-8") as file:
				file.write(ethics)
			print(f"Ethical considerations written to {output_file}")
			return True
		return ethics


	# Crate the overview with openai. Fills the self.json['Model Details']['Overview']
	# def create_overview(self,
	# 						   user_prompt, # The raw text
	# 						   model_card = None
	# 						   ) -> Optional[str]:
	# 	if model_card is None:
	# 		model_card = self.model_card
	# 	Make it simple so a non-expert can read it and understand the use of this model. Assume that the reader doesn't know anything about Machine learning. Don't use technical terminology
		# system_prompts = """You are a helpful assistant to create an overview for a model card.
		# 					Your output will be the text that i will directly use for the Overview section of
		# 					my model card. That means that you should not add any comments to your output.
		# 					Give me just the Overview of the text you are given.
		# 					Keep the text simple and professional."""
		#
		# messages = [
		# 			{"role": "system", "content": system_prompts},
		# 			{"role": "user", "content": user_prompt}
		# 		]
		# overview = self.__run_model(messages, max_tokens=4000, temperature=0.7, top_p=1)
		#
		# model_card.text['Model Details']['Overview'] = overview + self.__ai_generated_html_indicator()
		# return overview


	def __split_pdf_to_chunks(self,
							  pdf_path: str,  # path to pdf
							  max_characters: int=10000
							  ) -> List[str]:
		with open(pdf_path, 'rb') as pdf_file:
			reader = PyPDF2.PdfReader(pdf_file)
			current_chunk = ""
			for page in reader.pages:
				text = page.extract_text()
				for line in text.splitlines():
					if len(current_chunk) + len(line) > max_characters:
						# Ensure the chunk ends with a complete sentence
						last_period = current_chunk.rfind(".")
						if last_period != -1:
							self.pdf_chunks_for_llm.append(current_chunk[:last_period + 1])
							current_chunk = current_chunk[last_period + 1:].strip() + line + "\n"
						else:
							# If no period is found, append the chunk as is
							self.pdf_chunks_for_llm.append(current_chunk)
							current_chunk = line + "\n"
					else:
						current_chunk += line + "\n"
			# Add the last chunk if any text is left
			if current_chunk.strip():
				last_period = current_chunk.rfind(".")
				if last_period != -1:
					self.pdf_chunks_for_llm.append(current_chunk[:last_period + 1])
					remainder = current_chunk[last_period + 1:].strip()
					if remainder:
						self.pdf_chunks_for_llm.append(remainder)
				else:
					self.pdf_chunks_for_llm.append(current_chunk.strip())
		return self.pdf_chunks_for_llm

	# # Improve on json based on input using openai
	# def improve_json_with_openai(self,
	# 							 text_file_path: str, # Path to the txt file
	# 							 model_card = None
	# 							 ) -> str:
	# 	if model_card is None:
	# 		model_card = self.model_card
	# 	# Read the text file
	# 	with open(text_file_path, 'r') as f:
	# 		text_data = f.read()
	# 	# Split the text into chunks (you can adjust the chunk size as needed)
	# 	chunk_size = 4000  # Example chunk size, can be adjusted
	# 	text_chunks = [text_data[i:i + chunk_size] for i in range(0, len(text_data), chunk_size)]
	# 	last_output = model_card.text
	# 	role_for_improve_json_with_openai = importlib.resources.read_text("transparency_service.ai_assistant", "role_for_improve_json_with_openai.txt")
	# 	for i, chunk in enumerate(text_chunks):
	# 		prompt = f"{last_output}\n\n{chunk}" if last_output else chunk
	# 		try:
	# 			# Send the prompt to the OpenAI model
	# 			response = openai.chat.completions.create(
	# 				model="gpt-3.5-turbo",  # gpt-4
	# 				messages=[
	# 					{"role": "system", "content": role_for_improve_json_with_openai},
	# 					{"role": "user", "content": f"{prompt}"}
	# 				],
	# 				max_tokens=1000,
	# 				temperature=0.0001,
	# 				top_p=0.0001
	# 			)
	# 			# Get the model's response
	# 			model_output = response.choices[0].message.content
	# 			# Update the cumulative output
	# 			last_output = model_output + "\n"
	# 			print(last_output)
	# 		except Exception as e:
	# 			print(f"Error processing chunk {i + 1}: {e}")
	# 			break  # Exit the loop on error
	# 	try:
	# 		model_card.text = json.loads(last_output)
	# 	except json.JSONDecodeError as e:
	# 		print(f"Error parsing JSON: {e}")
	# 		model_card.text = None
	# 	return last_output

	# Create the whole json based on a pdf (e.g. a paper)
	def create_openai_json(self,
						   pdf_path: str, # Path to pdf
						   model_card = None
						   ) -> str:
		if model_card is None:
			model_card = self.model_card
		self.__split_pdf_to_chunks(pdf_path)
		last_output = json.dumps(model_card.text)
		system_prompt = importlib.resources.read_text("transparency_service.ai_assistant", "role_for_improve_json_with_openai.txt")

		for i, chunk in enumerate(self.pdf_chunks_for_llm):
			prompt = f"{last_output}\n\n{chunk}" if last_output else chunk
			messages = [
					{"role": "system", "content": system_prompt},
					{"role": "user", "content": f"{prompt}"}
				]
			model_output = self.__run_model(messages, max_tokens=4000, temperature=0.000001, top_p=0.000001)
			# Update the cumulative output
			last_output = model_output + "\n"
			print(last_output)

		model_card.text = json.loads(last_output)
		return json.loads(last_output)

	def create_overview(self,
						   pdf_path: str, # Path to pdf
						   ) -> str:
		self.__split_pdf_to_chunks(pdf_path)
		last_output = ''
		#system_prompt = importlib.resources.read_text("transparency_service.ai_assistant", "role_for_improve_json_with_openai.txt")
		system_prompt = importlib.resources.read_text("transparency_service.ai_assistant", "summ.ai")

		for i, chunk in enumerate(self.pdf_chunks_for_llm):
			prompt = f"{last_output}\n\n{chunk}" if last_output else chunk
			messages = [
					{"role": "system", "content": system_prompt},
					{"role": "user", "content": f"{prompt}"}
				]
			model_output = self.__run_model(messages, max_tokens=4000, temperature=0.000001, top_p=0.000001)
			# Update the cumulative output
			last_output = model_output + "\n"
			print(last_output)

		return last_output



	def __run_model(self, messages, max_tokens, temperature, top_p):
		if self.model_type == 'gpt':
			# Send the prompt to the OpenAI model
			response = openai.chat.completions.create(
				model=self.model,
				messages=messages,
				max_tokens=max_tokens,
				temperature=temperature,
				top_p=top_p
			)
			# Get the model's response
			model_output = response.choices[0].message.content
		elif self.model_type == 'llama':
			response = self.pipeline(
				messages,
				max_new_tokens=max_tokens,
				temperature=temperature,
				top_p=top_p,
			)
			model_output = response[0]["generated_text"][-1]['content']
		return model_output

	def __ai_generated_html_indicator(self):
		return """<span class="ai_generated">*<span class="text">AI generated</span></span>"""