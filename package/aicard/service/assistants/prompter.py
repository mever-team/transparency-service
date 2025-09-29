from .assistant import Assistant
from aicard.card import ModelCard
from aicard.agents import Agent


class Prompter(Assistant):
    def __init__(self, agent: Agent):
        super().__init__(alias=agent.__class__.__name__ , description="<h1>Prompting assistant</h1>Simplifications are applied only on fields with at least one line break. Any markdown is converted to html.")
        self.agent = agent
    def complete(self, card: ModelCard, url: str):
        pass
    def refine(self, card: ModelCard):
        for category, values in card.data.items():
            if not isinstance(values, dict):
                continue
            for field, value in values.items():
                if not isinstance(value, str):
                    continue
                if len(value.split('\n'))<2:
                    continue
                values[field] = "<h1>Simplified</h1>\n\n"+self.agent.simplification(value)+"\n\n<h1>Original</h1>\n\n"+value
        card.assign(card.to_html_card())

def assist(agent):
    if isinstance(agent, Agent): return Prompter(agent)
    raise Exception("Invalid agent type to assist with: "+str(type(agent)))