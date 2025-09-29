from .assistant import Assistant
from aicard.card import ModelCard
from nltk.corpus import wordnet as wn
import nltk
import re


class WordNet(Assistant):
    def __init__(self):
        super().__init__(
            description=(
                "<h1>Test assistant</h1>"
                "Highlights scientific terms from WordNet domain tags "
                "and adds tooltips with their definitions."
            )
        )
        nltk.download("wordnet", quiet=False)
        nltk.download("omw-1.4", quiet=False)
        sci_lexnames = {
            "noun.cognition", "noun.artifact", "noun.process",
            "noun.substance", "noun.attribute",
        }
        scientific_defs = {}
        for syn in wn.all_synsets():
            if syn.lexname() in sci_lexnames:
                gloss = syn.definition()
                for lemma in syn.lemmas():
                    word = lemma.name().replace("_", " ").lower()
                    scientific_defs.setdefault(word, gloss)
        print(f"Collected {len(scientific_defs)} scientific terms")
        self.scientific_defs = scientific_defs

    def complete(self, card: ModelCard, url: str):
        pass

    def refine(self, card: ModelCard):
        for cat, vals in card.data.items():
            if not isinstance(vals, dict):
                continue
            for field, value in vals.items():
                if not isinstance(value, str):
                    continue
                for def_name, def_value in self.scientific_defs.items():
                    value = value.replace(def_name, def_name+" ("+def_value+")")
                vals[field] = value
        print(card.to_markdown())
        card.assign(card.to_html_card())

