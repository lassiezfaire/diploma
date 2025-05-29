from typing import Dict, Any, List, Optional

from fastapi import UploadFile

from app.grafana.client import grafana_client
from app.llm.base_ai_assistant import BaseAIAssistant


class Agent:
    def __init__(self, ai_assistant: BaseAIAssistant):
        self.ai_assistant = ai_assistant
        self.grafana_client = grafana_client

    def process_request(self, user_prompt: str, files: Optional[List[UploadFile]] = None) -> Dict[str, Any]:
        # Создаем сессию (если нужно)
        session_id = self.ai_assistant.create_session(files=files)

        try:
            llm_response = self.ai_assistant.ask_question(session_id, user_prompt)

            grafana_response = self.grafana_client.post("/api/dashboards/db", data=llm_response)

            return grafana_response
        finally:
            # Всегда закрываем сессию
            self.ai_assistant.close_session(session_id)
