from typing import Dict, Any, Optional, List
from fastapi import UploadFile

from app.llm.base_ai_assistant import BaseAIAssistant
from app.grafana.client import grafana_client


class Agent:
    def __init__(self, ai_assistant: BaseAIAssistant):
        self.ai_assistant = ai_assistant
        self.grafana_client = grafana_client

    def create_session(self, files: Optional[List[UploadFile]] = None) -> str:
        """Создает новую сессию с возможностью загрузки файлов"""
        return self.ai_assistant.create_session(files=files)

    def close_session(self, session_id: str) -> None:
        """Закрывает сессию"""
        self.ai_assistant.close_session(session_id)
