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
            "noun.substance", "noun.attribute",  # adjust to taste
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

    import re

    def refine(self, card: ModelCard):
        # Regex to locate <span ...>...</span> blocks and quoted text
        span_re = re.compile(r"<span\b[^>]*?>.*?</span>", re.IGNORECASE | re.DOTALL)
        quote_re = re.compile(r'"[^"]*"')

        splitter = re.compile(r"([.,\s])")

        for cat, vals in card.data.items():
            if not isinstance(vals, dict):
                continue
            for field, value in vals.items():
                if not isinstance(value, str):
                    continue

                # Collect all protected segments (span blocks + quoted strings)
                protected = []
                for m in span_re.finditer(value):
                    protected.append((m.start(), m.end()))
                for m in quote_re.finditer(value):
                    protected.append((m.start(), m.end()))
                # merge & sort
                protected.sort()

                result = []
                last = 0
                for start, end in protected:
                    # normal (unprotected) chunk before this protected block
                    chunk = value[last:start]
                    result.append(self._highlight_scientific(chunk, splitter))
                    # keep protected block exactly as is
                    result.append(value[start:end])
                    last = end
                # any trailing normal chunk
                result.append(self._highlight_scientific(value[last:], splitter))

                card.data[cat][field] = "".join(result)

        card.assign(card.to_html_card())

    def _highlight_scientific(self, text, splitter):
        """Highlight scientific words in a plain-text segment."""
        tokens = splitter.split(text)
        out = []
        for tok in tokens:
            if not tok or tok.isspace() or tok in {".", ","}:
                out.append(tok)
                continue
            lw = tok.lower()
            if lw in self.scientific_defs:
                gloss = self.scientific_defs[lw]
                tooltip = f'<span class="sci-term" title="{gloss}">{tok}</span>'
                out.append(tooltip)
            else:
                out.append(tok)
        return "".join(out)
