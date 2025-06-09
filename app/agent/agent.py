from typing import Dict, Any, List

from app.grafana.client import grafana_client
from app.llm_clients.base_client import BaseLLMClient


class AIAgent:
    def __init__(self, llm_client: BaseLLMClient):
        self.llm_client = llm_client

        self.grafana_client = grafana_client

    def create_agent(self, system_prompt: str, file_path: str = None) -> str:
        """Создает новую сессию ассистента"""
        session_id = self.llm_client.create_assistant(
            system_prompt=system_prompt,
            file_path=file_path
        )

        return session_id

    def request(self, session_id: str, question: str) -> Dict[str, Any]:
        """Задаёт вопрос ассистенту и отправляет его ответ в Grafana"""
        # llm_response = self.llm_client.ask_assistant(session_id, question)

        # grafana_response = self.grafana_client.post("/api/dashboards/db", data=llm_response)

        return self.llm_client.ask_assistant(session_id, question)

    def delete_agent(self, assistant_id: str) -> None:
        """Удаляет ненужный ассистент."""
        self.llm_client.delete_assistant(assistant_id)

    def list_assistants(self) -> List[dict]:
        """Выводит список всех ассистентов"""
        return self.llm_client.list_assistants()
