from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from fastapi import UploadFile


class BaseAIAssistant(ABC):
    @abstractmethod
    def __init__(self, config: Dict[str, Any]):
        """Инициализация клиента с конфигурацией"""
        pass

    @abstractmethod
    def create_session(self, files: Optional[List[UploadFile]] = None) -> str:
        """Создание новой сессии (при необходимости)"""
        pass

    @abstractmethod
    def ask_question(self, session_id: str, question: str) -> Dict[str, Any]:
        """Задать вопрос модели"""
        pass

    @abstractmethod
    async def _delete_assistant_via_api(self, assistant_id: str) -> None:
        """Абстрактный метод для удаления ассистента через API"""
        pass

    @abstractmethod
    def close_session(self, session_id: str) -> None:
        """Закрытие сессии и освобождение ресурсов"""
        pass

    @abstractmethod
    def list_sessions(self) -> List[str]:
        """Возвращает список активных сессий"""
        pass
