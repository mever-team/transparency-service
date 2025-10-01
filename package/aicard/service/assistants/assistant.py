from aicard.card import ModelCard
from aicard.service.logger import Logger


class Assistant:
    def __init__(self, alias=None, description=None):
        self.description = description
        self.alias = alias if alias else self.__class__.__name__
    def start(self, logger: Logger): pass
    def complete(self, card: ModelCard, url: str, logger: Logger, user_messages: list[str]): pass
    def refine(self, card: ModelCard, logger: Logger, user_messages: list[str]): pass
