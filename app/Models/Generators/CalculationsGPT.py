from overrides import override

# internal imports
from ..GPTBase import GPTBase
from .. import Prompts


class Calculations(GPTBase):
    @override
    def __init__(self):
        self.prompt = Prompts.CALCULATION_GENERATOR_PROMPT
        self.messages = [{"role": "system", "content": self.prompt}]
        
    def concat(self, prompt: str, calculations: str) -> str:
        return prompt + "\n\n" + calculations
    
    
    def send(self, prompt: str) -> str:
        self.messages.append({"role": "user", "content": prompt})
        return super().send(self.messages, 0, 1)
