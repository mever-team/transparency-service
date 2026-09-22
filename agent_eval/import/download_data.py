import requests
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from huggingface_hub import HfApi
import re

LIMIT = 1000
MIN_WORDS = 1000
MAX_WORKERS = 20

api = HfApi()

# Get the 1,000 most-liked models
models = list(api.list_models(
    sort="likes",
    limit=LIMIT,
))

print(f"Found {len(models)} models")


def check_model(model):
    model_id = model.id
    url = f"https://huggingface.co/{model_id}/raw/main/README.md"

    try:
        response = requests.get(url, timeout=15)

        if response.status_code != 200:
            return model_id, 0, False

        readme = response.text

        # Remove fenced code blocks
        text_for_count = re.sub(
            r"```.*?```",
            "",
            readme,
            flags=re.DOTALL
        )

        # Remove Markdown tables
        lines = text_for_count.splitlines()
        filtered_lines = []

        for line in lines:
            if line.strip().startswith("|") and line.strip().endswith("|"):
                continue

            if re.match(
                r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$",
                line
            ):
                continue

            filtered_lines.append(line)

        text_for_count = "\n".join(filtered_lines)

        # Check README word count excluding code and tables
        word_count = len(text_for_count.split())

        if word_count < MIN_WORDS:
            return model_id, word_count, False

        # Extract YAML front matter
        base_model = None

        if readme.startswith("---"):
            parts = readme.split("---", 2)

            if len(parts) >= 3:
                try:
                    metadata = yaml.safe_load(parts[1]) or {}
                    base_model = metadata.get("base_model")
                except yaml.YAMLError:
                    pass

        # A model with base_model metadata is considered a derivative
        is_base_model = base_model is None

        return model_id, word_count, is_base_model

    except requests.RequestException:
        return model_id, 0, False


# Check README files in parallel
valid_ids = set()

print("Checking README files...")

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [
        executor.submit(check_model, model)
        for model in models
    ]

    for i, future in enumerate(as_completed(futures), 1):
        model_id, word_count, is_base_model = future.result()

        if is_base_model:
            valid_ids.add(model_id)

        print(
            f"\rChecked {i}/{len(models)} | "
            f"Valid base models: {len(valid_ids)}",
            end="",
            flush=True,
        )

print("\n")


# Keep only the top-liked model from each organization
selected_models = []
organizations = set()

for model in models:
    if model.id not in valid_ids:
        continue

    # Extract organization
    if "/" in model.id:
        organization = model.id.split("/", 1)[0]
    else:
        organization = model.id

    # Keep only the first (highest-liked) model
    # from each organization
    if organization in organizations:
        continue

    organizations.add(organization)
    selected_models.append(model)


# Write URLs
with open("repos_urls.txt", "w") as f:
    for model in selected_models:
        f.write(f"https://huggingface.co/{model.id}\n")


print(f"Final number of models: {len(selected_models)}")
print("URLs saved to repos_urls.txt")

import os

# Create output directories
html_output_dir = "original_web_pages"
md_output_dir = "original_md"

os.makedirs(html_output_dir, exist_ok=True)
os.makedirs(md_output_dir, exist_ok=True)

print("Downloading original Hugging Face webpages and README files...")

for i, model in enumerate(selected_models, 1):
    model_id = model.id

    # Convert organization/model into a safe filename
    filename = model_id.replace("/", "@")

    html_path = os.path.join(
        html_output_dir,
        filename + ".html"
    )

    md_path = os.path.join(
        md_output_dir,
        filename + ".md"
    )

    try:
        # Download HTML webpage
        html_url = f"https://huggingface.co/{model_id}"
        response = requests.get(html_url, timeout=30)
        response.raise_for_status()

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        # Download README.md
        md_url = f"https://huggingface.co/{model_id}/raw/main/README.md"
        response = requests.get(md_url, timeout=30)
        response.raise_for_status()

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(
            f"\rDownloaded {i}/{len(selected_models)}",
            end="",
            flush=True,
        )

    except requests.RequestException as e:
        print(f"\nFailed: {model_id} ({e})")

print(f"\nWebpages saved to: {html_output_dir}/")
print(f"README files saved to: {md_output_dir}/")