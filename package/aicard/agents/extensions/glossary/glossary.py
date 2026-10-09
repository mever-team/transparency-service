import re
from pathlib import Path
import json
from nltk.stem import SnowballStemmer

class Glossary:
    def __init__(self):
        glossary_path = Path(__file__).resolve().parent / "glossary.json"
        with Path(glossary_path).open("r", encoding="utf-8") as f:
            self.__glossary = json.load(f)
        self.__stemmer = SnowballStemmer("english")
        
            
            
    def find_glossary_entry(self, term: str) -> dict | None:
        for entry in self.__glossary.values():
            for match_term in entry["match_terms"]:
                if self.term_matches_text(match_term, term):
                    return entry
        return None
    
    def find_glossary_terms(self, text: str) -> list[dict]:
        matches = []
        for entry in self.__glossary.values():
            for term in entry["match_terms"]:
                if self.term_matches_text(term, text):
                    matches.append(entry)
                    break
        return matches

    def build_glossary_context(self, text: str) -> str:
        entries = self.find_glossary_terms(text)
        if not entries:
            return ""
        lines = [
            "The following technical terms were found in the original text.",
            "Use these explanations when making the text understandable.",
            "",
        ]
        for entry in entries:
            lines.append(
                f"- {entry['term']}: {entry['explanation']}"
            )
        return "\n".join(lines)

    ##################################
    #   NLP Stemmer
    ##################################
    def normalize_tokens(self, text: str) -> list[str]:
        text = text.lower()

        text = text.replace("-", " ")
        text = text.replace("_", " ")

        # Keep only words and numbers.
        tokens = re.findall(r"\b\w+\b", text)

        return [self.__stemmer.stem(token) for token in tokens]
    
    def term_matches_text(self, term: str, text: str) -> bool:
        term_tokens = self.normalize_tokens(term)
        text_tokens = self.normalize_tokens(text)

        if not term_tokens:
            return False

        term_length = len(term_tokens)

        for i in range(len(text_tokens) - term_length + 1):
            window = text_tokens[i:i + term_length]
            if window == term_tokens:
                return True
        return False