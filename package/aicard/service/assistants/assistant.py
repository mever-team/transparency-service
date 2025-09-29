from aicard.card import ModelCard


class Assistant:
    def __init__(self, alias=None, description=None):
        self.description = description
        self.alias = alias if alias else self.__class__.__name__
    def complete(self, card: ModelCard, url: str): pass
    def refine(self, card: ModelCard): pass
