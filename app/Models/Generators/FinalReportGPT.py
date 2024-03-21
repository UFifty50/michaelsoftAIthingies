from ..GPTBase import GPTBase
from .. import Prompts


class FinalReport(GPTBase):
    def __init__(self):
        self.prompt = Prompts.FINAL_REPORT_PROMPT
        self.messages = [{"role": "system", "content": self.prompt}]
        
    def concat(self, prompt: str, dataNeeded: str, analysisReport: str) -> str:
        return prompt + '\n\nData: ' + dataNeeded + '\nReport: ' + analysisReport
    
    def send(self, prompt: str) -> str:
        self.messages.append({"role": "user", "content": prompt})
        return super().send(self.messages, 1, 1)
