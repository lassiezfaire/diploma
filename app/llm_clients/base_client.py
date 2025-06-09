from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseLLMClient(ABC):
    @abstractmethod
    def create_assistant(self, system_prompt: str, file_path: str = None) -> str:
        """Создает ассистента с системным промптом и опциональным файлом"""
        pass

    @abstractmethod
    def ask_assistant(self, assistant_id: str, question: str) -> Dict[str, Any]:
        """Задает вопрос ассистенту"""
        pass

    @abstractmethod
    def delete_assistant(self, assistant_id: str) -> None:
        """Удаляет ассистента"""
        pass

    @abstractmethod
    def list_assistants(self) -> List[dict]:
        """Возвращает список всех ассистентов"""
        pass
