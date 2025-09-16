import time
from aicard.card import ModelCard
from aicard.agents import Agent
from aicard.service.client import Client


class Assistant:
    def __init__(self, alias=None, description=None):
        self.description = description
        self.alias = alias if alias else self.__class__.__name__
    def complete(self, card: ModelCard, url: str): pass
    def refine(self, card: ModelCard): pass

class TestAssistant(Assistant):
    def __init__(self, delay: float=0):
        super().__init__(description="<h1>Test assistant</h1>This AI assistant is primarily used for testing. For now, it does nothing, but some simple ad-hoc functionality for autocompleting and refining model cards may be added.")
        self.delay = delay
    def complete(self, card: ModelCard, url: str):
        if self.delay: time.sleep(self.delay)
    def refine(self, card: ModelCard):
        if self.delay: time.sleep(self.delay)

class Prompter(Assistant):
    def __init__(self, agent: Agent):
        super().__init__(alias=agent.__class__.__name__ , description="<h1>Test assistant</h1>This AI assistant is primarily used for testing.")
        self.agent = agent
    def complete(self, card: ModelCard, url: str):
        pass
    def refine(self, card: ModelCard):
        pass

def assist(agent):
    if isinstance(agent, Agent): return Prompter(agent)
    raise Exception("Invalid agent type to assist with: "+str(type(agent)))