from abc import ABC, abstractmethod

class BaseLLMClient(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def request(self, message):
        pass
