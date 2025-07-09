# Step 1: Load data
from datasets import load_dataset

dataset = load_dataset("lytang/LLM-AggreFact")
data_test = dataset["test"]

# Step 2: Call AI-Assistant
from modelcard.assistant import AI_Assistant

aia = AI_Assistant(model="gpt-3.5-turbo")
aia.dataset_summary(data_test)

# Output:
# The dataset comprises 29,320 instances with five main attributes: 'dataset', 'doc', 'claim', 'label', and 'contamination_identifier'. The 'dataset' attribute includes various datasets such as AggreFact-CNN, Wice, AggreFact-XSum, FactCheck-GPT, and others, with different numbers of instances ranging from 358 to 16,371.
#
# The 'doc' attribute contains textual information in the form of news articles or reports, as evidenced by samples mentioning topics like child prodigies, a boxer's activities, and a Palestinian teenager. Similarly, the 'claim' attribute provides statements related to the content in 'doc', such as a child shooting hoops, a boxer's family day out, and a teenager's memorialization.
#
# The 'label' attribute indicates two classes, '0' and '1', with no instances specified for either class. This suggests a potential class imbalance, although the extent is not detailed.
#
# Lastly, the 'contamination_identifier' attribute seems to contain unique identifiers associated with data contamination, possibly for tracking or analysis purposes. Samples from this attribute suggest encoded identifiers like 'LLM-AggreFact' followed by a string of characters.
#
# In summary, this dataset contains textual data from various sources, paired with corresponding claims and potential contamination identifiers. The imbalance in the label distribution could be a point of interest for further analysis or preprocessing to ensure model performance and generalizability.

# Step 1: Load Data Set
from datasets import load_dataset

dataset = load_dataset("google-research-datasets/go_emotions", split="test")

# Step 2: Call AI-Assistant
from modelcard.assistant import AI_Assistant

aia = AI_Assistant(model="gpt-3.5-turbo")
aia.dataset_summary(dataset)

# Output:
# The dataset consists of 5427 instances with three columns: 'text', 'labels', and 'id'. The 'text' column contains various textual entries, such as messages or comments. A sample of the first 5 rows from the 'text' column indicates a diverse range of content, including expressions of empathy, sports-related comments, expressions of gratitude, and references to supernatural themes.
#
# The 'labels' column seems to categorize the entries into different classes, with a total of 28 unique labels ranging from 0 to 27. The distribution of instances across these labels varies significantly, with label 27 having the highest frequency of 1787 instances, while labels like 16, 19, 21, and 23 have very few instances (6, 23, 16, and 11 instances respectively). This imbalance in label distribution may impact the performance of certain machine learning models trained on this dataset.
#
# Each instance is associated with a unique identifier stored in the 'id' column. The sample of the first 5 rows of 'id' shows alphanumeric identifiers assigned to each entry.
#
# The purpose of this dataset appears to be multi-class classification or categorization of text data based on the given labels. The text entries seem to cover a wide range of topics and sentiments, making it a potentially rich dataset for training models to classify text into one of the 28 specified categories. Further analysis and preprocessing may be necessary to handle the imbalances in label distribution before using this dataset for machine learning tasks.
