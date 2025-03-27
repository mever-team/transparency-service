import datasets
import pandas as pd
import transformers
import shap

# load the emotion dataset
dataset = datasets.load_dataset("emotion", split="train")
data = pd.DataFrame({"text": dataset["text"], "emotion": dataset["label"]})

# load the tokenizer
tokenizer = transformers.AutoTokenizer.from_pretrained("nateraw/bert-base-uncased-emotion", use_fast=True)

# Ensure the model is loaded inside the main block to avoid multiprocessing issues on Windows
if __name__ == "__main__":
    # Load the model
    model = transformers.AutoModelForSequenceClassification.from_pretrained("nateraw/bert-base-uncased-emotion")
    #print("Model loaded successfully!")

    # build a pipeline object to do predictions
    pred = transformers.pipeline(
        "text-classification",
        model=model,
        tokenizer=tokenizer,
        device=0,
        return_all_scores=True,
    )

    # Create SHAP explainer
    explainer = shap.Explainer(pred)

    # Generate SHAP values for the first 3 text samples
    shap_values = explainer(data["text"][:1])

    # Plot the SHAP values for explanation
    a = shap.plots.text(shap_values, display = False)

    import re
    import numpy as np



    def correct_float64_in_html(html):
        # Regular expression to match np.float64(value)
        return re.sub(r'np\.float64\(([\d\.]+)\)', r'\1', html)


    # Example usage:
    corrected_html = correct_float64_in_html(a)


    with open('html_file.html', 'w') as f:
        f.write(corrected_html)
