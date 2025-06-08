from abc import ABC, abstractmethod


class BaseAIAssistant(ABC):
    @abstractmethod
    def __init__(self):
        """Инициализация клиента с конфигурацией"""
        pass

    @abstractmethod
    def ask_client(self):
        """Задать вопрос клиенту"""
        pass

    @abstractmethod
    def __del__(self):
        """Удалить клиент"""
        pass
