import csv
import io
import json
import re
from pathlib import Path

import requests


OUTPUT_FILE = Path("glossary.json")

GOOGLE_CSV_URL = (
    "https://raw.githubusercontent.com/"
    "darigovresearch/Google-Machine-Learning-Glossary-Flashcards/"
    "master/Google%20Machine%20Learning%20Glossary.csv"
)

AI_HANDBOOK_URL = (
    "https://raw.githubusercontent.com/"
    "h9-tec/AI-Glossary-Handbook/main/README.md"
)

OPENL_URL = (
    "https://raw.githubusercontent.com/"
    "openl-translate/ai-dictionary/main/README.md"
)



# ----------------------------------------------------------------------
# Normalization
# ----------------------------------------------------------------------

def normalize_term(term: str) -> str:
    """
    Normalize a term for dictionary keys and matching.
    """
    term = term.lower().strip()

    # Markdown formatting
    term = re.sub(r"\*+", "", term)
    term = re.sub(r"`+", "", term)

    # Normalize separators
    term = term.replace("_", " ")
    term = term.replace("-", " ")

    # Remove remaining punctuation
    term = re.sub(r"[^\w\s]", " ", term)

    # Collapse whitespace
    term = re.sub(r"\s+", " ", term)

    return term.strip()


def clean_definition(definition: str) -> str:
    """
    Remove unnecessary Markdown formatting from definitions.
    """
    definition = definition.strip()

    definition = re.sub(r"\*\*(.*?)\*\*", r"\1", definition)
    definition = re.sub(r"\*(.*?)\*", r"\1", definition)
    definition = re.sub(r"`(.*?)`", r"\1", definition)

    definition = re.sub(r"\s+", " ", definition)

    return definition.strip()


# ----------------------------------------------------------------------
# Term / alias handling
# ----------------------------------------------------------------------

def extract_aliases(raw_term: str):
    """
    Extract aliases from parenthetical abbreviations.

    Examples:

        Dialect Identification (DID)
            -> Dialect Identification
            -> DID

        Variational Autoencoder (VAE)
            -> Variational Autoencoder
            -> VAE

        Mixture of Experts (MoE)
            -> Mixture of Experts
            -> MoE
    """

    raw_term = raw_term.strip()

    aliases = []

    # Look for a final "(XXX)" part.
    match = re.search(r"\s*\(([^()]+)\)\s*$", raw_term)

    if match:
        inside = match.group(1).strip()

        # Remove the parenthetical part from the canonical term.
        canonical = raw_term[:match.start()].strip()

        # Add the abbreviation/alias.
        if inside:
            aliases.append(inside)

        return canonical, aliases

    return raw_term, aliases


def make_match_terms(term: str, aliases):
    """
    Create all normalized forms that can be used for matching.
    """

    candidates = [term]

    # Original term with parenthetical abbreviation removed.
    candidates.extend(aliases)

    # Keep the full form as well, e.g.
    # "Dialect Identification (DID)"
    for alias in aliases:
        candidates.append(f"{term} {alias}")

    result = []

    for candidate in candidates:
        normalized = normalize_term(candidate)

        if normalized and normalized not in result:
            result.append(normalized)

    return result


# ----------------------------------------------------------------------
# Glossary storage
# ----------------------------------------------------------------------

glossary = {}


def add_entry(
    raw_term: str,
    explanation: str,
    source: str,
):
    """
    Add one glossary entry.

    Entries are merged when their normalized canonical terms match.
    """

    raw_term = raw_term.strip()
    explanation = clean_definition(explanation)

    if not raw_term or not explanation:
        return

    canonical_term, aliases = extract_aliases(raw_term)

    canonical_key = normalize_term(canonical_term)

    if not canonical_key:
        return

    match_terms = make_match_terms(
        canonical_term,
        aliases,
    )

    if canonical_key not in glossary:
        glossary[canonical_key] = {
            "term": canonical_term,
            "aliases": aliases,
            "match_terms": match_terms,
            "explanation": explanation,
            "sources": [source],
        }

    else:
        entry = glossary[canonical_key]

        # Merge aliases
        for alias in aliases:
            if alias not in entry["aliases"]:
                entry["aliases"].append(alias)

        # Rebuild match terms
        entry["match_terms"] = make_match_terms(
            entry["term"],
            entry["aliases"],
        )

        # Keep track of all sources
        if source not in entry["sources"]:
            entry["sources"].append(source)


# ----------------------------------------------------------------------
# Google ML Glossary
# ----------------------------------------------------------------------

def parse_google(content: str):
    """
    Parse the Google ML glossary CSV.
    """

    reader = csv.reader(io.StringIO(content))

    for row in reader:
        if len(row) < 2:
            continue

        term = row[0].strip()
        definition = row[1].strip()

        if not term or not definition:
            continue

        # Skip obvious header rows
        if term.lower() in {
            "term",
            "word",
            "front",
        }:
            continue

        add_entry(
            term,
            definition,
            "google_ml_glossary",
        )

# ----------------------------------------------------------------------
# AI Glossary Handbook
# ----------------------------------------------------------------------

def parse_ai_handbook(content: str):
    """
    Parse entries such as:

        * Neural Network: A function built from...
        * Variational Autoencoder (VAE): A model that...
    """

    for line in content.splitlines():

        line = line.strip()

        if not line.startswith("*"):
            continue

        # Remove bullet
        line = re.sub(r"^\*\s*", "", line)

        # Remove Markdown emphasis
        line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
        line = re.sub(r"\*(.*?)\*", r"\1", line)

        # Split only on the first colon.
        if ":" not in line:
            continue

        term, definition = line.split(":", 1)

        term = term.strip()
        definition = definition.strip()

        if not term or not definition:
            continue

        add_entry(
            term,
            definition,
            "ai_handbook",
        )


# ----------------------------------------------------------------------
# OpenL AI Dictionary
# ----------------------------------------------------------------------

def parse_openl(content: str):
    """
    Parse Markdown table rows such as:

        | AGI | ... | Artificial General Intelligence... |
    """

    for line in content.splitlines():

        line = line.strip()

        if not line.startswith("|"):
            continue

        # Split Markdown table columns
        columns = [
            column.strip()
            for column in line.strip("|").split("|")
        ]

        if len(columns) < 3:
            continue

        term = columns[0]
        definition = columns[-1]

        # Skip header/separator rows
        if (
            not term
            or not definition
            or term.lower() in {
                "terms",
                "term",
                "pronunciation",
            }
            or re.fullmatch(r"[-: ]+", term)
        ):
            continue

        add_entry(
            term,
            definition,
            "openl_dictionary",
        )


# ----------------------------------------------------------------------
# Download
# ----------------------------------------------------------------------

def download(url: str) -> str:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main():

    # print("Downloading Google ML Glossary...")
    # google_content = download(GOOGLE_CSV_URL)
    # parse_google(google_content)

    print("Downloading AI Glossary Handbook...")
    handbook_content = download(AI_HANDBOOK_URL)
    parse_ai_handbook(handbook_content)

    print("Downloading OpenL AI Dictionary...")
    openl_content = download(OPENL_URL)
    parse_openl(openl_content)

    # Sort alphabetically
    sorted_glossary = dict(
        sorted(
            glossary.items(),
            key=lambda item: item[0],
        )
    )

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            sorted_glossary,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Created {OUTPUT_FILE} "
        f"with {len(sorted_glossary)} terms."
    )


if __name__ == "__main__":
    main()