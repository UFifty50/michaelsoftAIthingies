from overrides import override
from typing import List

from ..GPTBase import GPTBase
from .. import Prompts
from Doc import CsvDoc


class FinalReport(GPTBase):
    @override
    def __init__(self):
        self.prompt = Prompts.FINAL_REPORT_PROMPT
        self.messages = [{"role": "system", "content": self.prompt}]
        
    def concat(self, prompt: str, docArr: List[CsvDoc], dataNeeded: str, analysisReport: str) -> str:
        nl = "\n"
        return prompt + f"""Datasets: {f"{nl}{nl}".join([f"{doc.title}: {doc.content}" for doc in docArr])}
    
    Recommended Data: {dataNeeded}
    
    Analysis Report: {analysisReport}
    
    Prompt: {prompt}
"""
    
    def send(self, prompt: str) -> str:
        self.messages.append({"role": "user", "content": prompt})
        return super().send(self.messages, 1, 1)
