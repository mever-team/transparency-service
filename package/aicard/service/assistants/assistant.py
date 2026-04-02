from aicard.card import ModelCard
from aicard.service.logger import Logger
from aicard.service.cards_status import CardStatus



class Assistant:
    def __init__(self, alias=None, description=None):
        self.description = description
        self.alias = alias if alias else self.__class__.__name__
    def start(self, logger: Logger): pass
    def complete(self, card: ModelCard, url: str, logger: Logger, user_messages: list[str]): pass
    def refine(self, card: ModelCard, card_id: int, logger: Logger, user_messages: list[str], card_status: CardStatus): pass
    def refine_field(self, text: str, logger: Logger): pass
    def refine_field_ndjson(self, text: str, logger: Logger): pass