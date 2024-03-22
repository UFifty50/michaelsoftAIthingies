from abc import ABC, abstractmethod
from typing import List, Dict
import openai
import os


class GPTBase(ABC):
    prompt: str
    messages: List[Dict[str, str]]
    
    @abstractmethod
    def __init__(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def send(self, messages: List[Dict[str, str]], temp: float = 0.7, topP: float = 0.95) -> str:
        response = openai.ChatCompletion.create(
            engine="gpt-35-hackathon",  # os.environ.get("GPT_ENGINE"),
            temperature=temp,
            top_p=topP,
            frequency_penalty=0,
            presence_penalty=0,
            max_tokens=4000,
            messages=messages,
        )
        return response["choices"][0]["message"]["content"] # type: ignore
    