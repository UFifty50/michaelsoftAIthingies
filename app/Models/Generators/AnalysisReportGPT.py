from overrides import override
from typing import Dict

# internal imports
from ..GPTBase import GPTBase
from .. import Prompts


class AnalysisReport(GPTBase):
    @override
    def __init__(self):
        self.prompt = Prompts.ANALYSIS_REPORT_PROMPT
        self.messages = [{"role": "system", "content": self.prompt}]
        
    def concat(self, prompt: str, calculationAns: Dict[str, str]) -> str:
        return prompt + '\n'.join([f"{key}: {value}" for key, value in calculationAns.items()])
    
    def send(self, prompt: str) -> str:
        self.messages.append({"role": "user", "content": prompt})
        return super().send(self.messages, 0.5, 0.9)
