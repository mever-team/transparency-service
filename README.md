# Transparency-service

This SDK contains a collection of methods to create, manage, 
and edit AI model cards. It can handle text, lists of data, and plots 
which can be used to populate parts of the cards. We also provide methods 
to automatically populate some fields which will be discussed in this document. 
Model Card structure.

## :zap: Quickstart

Clone this repository and install it in your virtual environment per:

```commandline
python -m venv .venv
source .venv/bin/activate
pip install -e package
```

Run manually any evaluation pipeline like so:

```commandline
python -m demo
```

## :brain: About

The SDK offers an initial structure for the Model Cards, represented as a json 
of the following format:

```json
{
  "Title": "",
  "Model Details": {
    "Name": "",
    "Overview": "",
    "Version": "",
    "License": "",
    "References": {}
  },
  "Considerations": {
    "Use Case": {},
    "Limitations": {},
    "Ethical Considerations": {}
  },
  "Training": {
    "Text": ""
  },
  "Testing": {
    "Text": ""
  },
  "Quantitative Analysis": {
    "Text": ""
  }
}
```

## :scroll: License

TBD