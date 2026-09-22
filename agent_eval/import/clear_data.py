import os
import re
from bs4 import BeautifulSoup

INPUT_DIR = "original_md"
OUTPUT_DIR = "no_html_md"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def remove_yaml_front_matter(text):
    if text.lstrip().startswith("---"):
        text = re.sub(
            r"^\s*---\s*\n.*?\n---\s*\n?",
            "",
            text,
            count=1,
            flags=re.DOTALL
        )

    return text


def remove_markdown_tables(text):
    lines = text.splitlines()
    result = []

    i = 0

    while i < len(lines):
        line = lines[i]

        # Detect Markdown table header + separator
        if (
            "|" in line
            and i + 1 < len(lines)
            and re.match(
                r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$",
                lines[i + 1]
            )
        ):
            # Skip the entire table
            i += 2

            while i < len(lines) and "|" in lines[i]:
                i += 1

            continue

        result.append(line)
        i += 1

    return "\n".join(result)


def remove_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


def remove_short_lines(text, min_length=30):
    lines = text.splitlines()

    lines = [
        line for line in lines
        if len(line.strip()) >= min_length
    ]

    return "\n".join(lines)


def clean_markdown(text):
    # 1. Remove YAML front matter
    text = remove_yaml_front_matter(text)

    # 2. Remove Markdown tables
    text = remove_markdown_tables(text)

    # 3. Remove HTML tags
    text = remove_html_tags(text)

    # 4. Remove lines shorter than 30 characters
    text = remove_short_lines(text, min_length=30)

    return text


for filename in os.listdir(INPUT_DIR):
    if not filename.endswith(".md"):
        continue

    input_path = os.path.join(INPUT_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, filename)

    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    cleaned_text = clean_markdown(text)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    print(f"Processed: {filename}")

print(f"\nCleaned files saved to: {OUTPUT_DIR}/")