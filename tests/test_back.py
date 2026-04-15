import unittest

from aicard import ModelCard
from aicard.agents import Ollama

class CardTestCase(unittest.TestCase):
    def test_create_card(self):
        card = ModelCard()
        self.assertTrue(isinstance(card, ModelCard))
        
class AgentsTestCase(unittest.TestCase):
    def test_ollama_init(self):
        agent = Ollama()
        self.assertTrue(isinstance(agent, Ollama))
    def test_ollama_response(self):
        agent = Ollama()
        response_text = agent._run('Density functional theory describes electron distribution', 'simplification')
        self.assertTrue(isinstance(response_text, str))