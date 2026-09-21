import re
def extract_paragraphs(model_card: dict, excluded_fields=None):
    excluded_fields = excluded_fields or {"title"}

    paragraphs = []
    paragraph_id = 0

    for section in model_card.get("data", []):
        section_name = section.get("name")

        if section_name in excluded_fields:
            continue

        values = section.get("value", [])

        if not isinstance(values, list):
            continue

        for field in values:
            field_name = field.get("name")

            if not field_name:
                continue

            full_field_name = f"{section_name}.{field_name}"

            if full_field_name in excluded_fields:
                continue

            value = field.get("value", "")

            if value is None:
                continue

            if not isinstance(value, str):
                value = str(value)

            for text in value.split("<span id='agent-eval-mark'></span>"):# re.split(r'\.\s+', value): #value.split("."):
                text = text.strip()

                if not text:
                    continue

                paragraphs.append({
                    "id": paragraph_id,
                    "field": full_field_name,
                    "text": text,
                })

                paragraph_id += 1

    return paragraphs