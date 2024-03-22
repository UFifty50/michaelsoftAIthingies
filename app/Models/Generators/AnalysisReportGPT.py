from overrides import override
from typing import List, Dict

# internal imports
from ..GPTBase import GPTBase
from .. import Prompts
from Doc import CsvDoc


class AnalysisReport(GPTBase):
    @override
    def __init__(self):
        self.prompt = Prompts.ANALYSIS_REPORT_PROMPT
        self.messages = [{"role": "system", "content": self.prompt}]
        
    def concat(self, prompt: str, docArr: List[CsvDoc], dataNeeded: str, calculationAns: Dict[str, str]) -> str:
        nl = "\n"
        return f"""Datasets: {f"{nl}{nl}".join([f"{doc.title}: {doc.content}" for doc in docArr])}

Recommended Data: {dataNeeded}

Calculations: {f"{nl}".join([f"{key}: {value}" for key, value in calculationAns.items()])}

Prompt: {prompt}
"""
    
    def send(self, prompt: str) -> str:
        self.messages.append({"role": "user", "content": prompt})
        return super().send(self.messages, 0.5, 0.9)
