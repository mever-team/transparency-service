# Maintainer docs

The structure can be changed but this is a convenient starting point to start building the Model Card. This json is stored in the instance variable self.json. Moreover, several more instance variable are created during the __init__ (self) method analyzed bellow.

- `self.json` This is the json as discussed above which stores the whole Model Card
- `self.markdown_string` This is the markdown automatically created from self.json by using a class method
- `self.html_string` This is the html automatically created from self.markdown_string by using a class method
- `self.pdf_chunks_for_llm` This is a list that stores big text in chunks in order to be used as inputs in an llm. This helps to automatically populate parts of the Model Card using an llm based on the input. This variable is handled by the class methods and it should usually not be a concern when using the SDK
- `self.bar_plot_data` This variable stores data for several bar plots when creating the plot with a method.  e.g. `“plot1”: {"bars": [(name_of_the_bar, value), …], "xlabel": “…”, "ylabel": “…”}`
- `self.acc_data` This variable stores the accuracy of a several models and sets, e.g. `“model1”: {“set1”: 94, “set2” 83, …}`
- `self.ap_data` This variable stores the average precision of a several models and sets , e.g. `“model1”: {“set1”: 100, “set2” 98, …}`

Automatic field population
We provide several tools to automatically populate parts of the Model Card. Below we present several methods to help you in this maner. 
### `self.create_openai_overview(self, input)` 
This method uses an openai model to create an overview based on the input. The input is a string which can contain any information about the model. The openai is provided with: `"role": "system", "content": "You are a helpful assistant to create an overview for a model card. Your output will be the text that i will directly use for the Overview section of my model card. Keep the text simple and profesional."` After this process, the overview of the model card self.json['Model Details']['Overview'] is populated directly from the openai output.

### `self.create_openai_json(self, pdf_path)`
This method tries to populate the whole josn self.json based on a pdf file. The intended use if for models that are already well documented e.g. published models which do not provide a Model Card yet. The instructions for this are long and are not presented in this document. You can find the instruction in input_for_create_openai_create_openai_json.txt. After using this method the whole model card should be populated based on the pdf provided. The pdf is split into chunks to make it possible for the openai model to read it.

### `improve_json_with_openai(self, text_file_path)`
TODO

### `plit_pdf_to_chunks(self, pdf_path, max_characters=4000)` 
not relevant for this doc. Should remove

- `git_get_license(self, owner, repo)` 
Provided by the github repository, populate the `self.json['Model Details']['License']`

### `get_git_info(self, owner, repo)`

Provided the github repository, populate the: 

```python
self. json ['Model Details']['License'] 
self. json ['Model Details']['Version'] 
self. json ['Model Details']['Name'] 
self. json ['Model Details']['References']['github']
```


## Metrics and Plots
The SDK has a built-in function to handle metrics and plots and insert them into the Model Card. 
- `self.generate_ap_data(self, y_true, y_pred, model, data_set)`
Create and store average precision from y_true, y_pred in self.data[‘ap’]. model and data_set are the name of the model and data set respectively and are used internally to manage and identify the data that are created. 
- `self.generate_acc_data(self, y_true, y_pred, model, data_set)`
Create and store average precision from y_true, y_pred in self.data[‘acc’].
- `self.init_bar_plot(self, title, xlabel = " ", ylabel = " ")`
- 
Initialize a bar plot with a given title and x,y labels.
- `self.fill_bar_plot_from_data(self, plot_title, model, data)`
- `self.append_bar_to_plot(self, title, name_of_the_bar, value)`
- `self.add_plot_to(self, title, destination)`
- `self.show_plot(self, title)`


