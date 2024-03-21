from overrides import override
from typing import List

# internal imports
from ..GPTBase import GPTBase
from .. import Prompts
from Doc import CsvDoc


class DataExtractor(GPTBase):
    @override
    def __init__(self):
        self.prompt = Prompts.DATA_EXTRACTOR_PROMPT
        self.messages = [{"role": "system", "content": self.prompt}]
        
    def concat(self, prompt: str, docArr: List[CsvDoc]) -> str:
        return prompt + '\n' + "\n\n".join([f"{doc.title}: {doc.content}" for doc in docArr])
    
    def send(self, prompt: str) -> str:
        self.messages.append({"role": "user", "content": prompt})
        return super().send(self.messages, 0, 1)
