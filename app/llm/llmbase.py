from abc import ABC, abstractmethod
from typing import List, Dict

class LLMBase(ABC):

    @abstractmethod
    def generate_text(self, messages: List[Dict], model: str|None,  temperature: float|None):
        pass
          
    @abstractmethod
    def generate_stream(self, messages: List[Dict], model: str|None,  temperature: float|None):
        pass


    @abstractmethod
    def model(self):
        pass

    @abstractmethod
    def temperature(self):
        pass

if __name__=='__main__':
    pass