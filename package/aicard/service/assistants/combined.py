from .assistant import Assistant
from aicard.card import ModelCard
from aicard.service.logger import Logger


class Combined(Assistant):
    def __init__(self, complete, refine, description:str = None, refine_immediately:bool = False):
        assert isinstance(complete, Assistant)
        assert isinstance(refine, Assistant)
        self.description = description if description else "<h1>Run</h1>Our assistant switches to "+complete.alias+" for import and "+refine.alias+" for refinement."
        super().__init__(
            alias="Agent",
            description=self.description
        )
        self._complete = complete
        self._refine = refine
        self._refine_immediately = refine_immediately

    def start(self, logger: Logger):
        self._complete.start(logger)
        self._refine.start(logger)

    def complete(self, card: ModelCard, url: str, logger: Logger, user_messages: list[str]):
        ret = self._complete.complete(card, url, logger, user_messages)
        if not self._refine_immediately: return ret
        return self._refine.refine(card, logger, user_messages)

    def refine(self, card: ModelCard, logger: Logger, user_messages: list[str]):
        return self._refine.refine(card, logger, user_messages)
    
    def refine_field(self, text: str, logger: Logger):
        return self._refine.refine_field(text, logger)