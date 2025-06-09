import base64
import time
from typing import Dict, List, Any
import uuid

import httpx

from app.config.yandex_config import yandex_settings
from app.llm_clients.base_client import BaseLLMClient


class YandexClient(BaseLLMClient):
    def __init__(self):
        """Инициализация клиента Yandex AI Assistant API с конфигурацией"""
        self.api_key = yandex_settings.yc_api_key
        self.folder_id = yandex_settings.yc_folder_id
        self.base_headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "application/json"
        }
        self.sessions: Dict[str, dict] = {}  # Хранилище сессий

    def _make_request(self, method: str, url: str, payload: dict = None) -> dict:
        """Базовый метод для выполнения HTTP-запросов"""
        with httpx.Client() as client:
            response = client.request(
                method,
                url,
                headers=self.base_headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()

    def _upload_file_and_create_index(self, file_path: str) -> tuple:
        """Загружает файл и создает поисковой индекс"""
        with open(file_path, "rb") as f:
            base64_encoded = base64.b64encode(f.read()).decode("utf-8")

        # Загрузка файла
        file_data = self._make_request(
            "POST",
            "https://rest-assistant.api.cloud.yandex.net/files/v1/files",
            {
                "folderId": self.folder_id,
                "mimeType": "application/json",
                "content": base64_encoded
            }
        )
        file_id = file_data['id']

        # Создание поискового индекса
        index_data = self._make_request(
            "POST",
            "https://rest-assistant.api.cloud.yandex.net/assistants/v1/searchIndex",
            {
                "folderId": self.folder_id,
                "fileIds": [file_id],
                "hybridSearchIndex": {}
            }
        )

        # Ждем завершения операции
        operation_id = index_data['id']
        start_time = time.time()
        while time.time() - start_time < 60:
            op_data = self._make_request(
                "GET",
                f"https://operation.api.cloud.yandex.net/operations/{operation_id}"
            )
            if op_data.get('done', False):
                search_index_id = op_data['response']['id']
                return file_id, search_index_id
            time.sleep(2)

        raise TimeoutError("Index creation timeout")

    def _create_assistant(self, system_prompt: str, search_index_id: str) -> str:
        """Создает ассистента"""
        assistant_data = self._make_request(
            "POST",
            "https://rest-assistant.api.cloud.yandex.net/assistants/v1/assistants",
            {
                "folderId": self.folder_id,
                "modelUri": f"gpt://{self.folder_id}/yandexgpt/rc",
                "instruction": system_prompt,
                "tools": [{"searchIndex": {"searchIndexIds": [search_index_id]}}]
            }
        )
        return assistant_data['id']

    def _create_thread(self, search_index_id: str) -> str:
        """Создает тред"""
        thread_data = self._make_request(
            "POST",
            "https://rest-assistant.api.cloud.yandex.net/assistants/v1/threads",
            {
                "folderId": self.folder_id,
                "tools": [{"searchIndex": {"searchIndexIds": [search_index_id]}}]
            }
        )
        return thread_data['id']

    def _delete_session_resources(self, session: dict) -> None:
        """Удаляет все ресурсы сессии в правильном порядке"""
        resources = [
            ('assistant', session['assistant_id']),
            ('thread', session['thread_id']),
            ('searchIndex', session['search_index_id']),
            ('file', session['file_id'])
        ]

        for resource_type, resource_id in resources:
            if not resource_id:
                continue

            try:
                plural = f"{resource_type}s" if resource_type != "searchIndex" else "searchIndex"
                api_url = ('files' if resource_type == 'file' else 'assistants')

                self._make_request(
                    "DELETE",
                    f"https://rest-assistant.api.cloud.yandex.net/{api_url}/v1/{plural}/{resource_id}"
                )

            except Exception as e:
                raise RuntimeError(f"Failed to delete {resource_type} {resource_id}: {str(e)}")

    def create_assistant(self, system_prompt: str, file_path: str = None) -> str:
        """Создает ассистента Yandex AI Assistant API с системным промптом и опциональным файлом"""
        session_id = str(uuid.uuid4())

        try:
            # Загрузка файла и создание поискового индекса
            file_id, search_index_id = self._upload_file_and_create_index(file_path)

            # Создание ассистента
            assistant_id = self._create_assistant(system_prompt, search_index_id)

            # Создание треда
            thread_id = self._create_thread(search_index_id)

            # Сохраняем сессию
            self.sessions[session_id] = {
                "file_id": file_id,
                "search_index_id": search_index_id,
                "assistant_id": assistant_id,
                "thread_id": thread_id
            }

            return session_id

        except Exception as e:
            # Если ошибка - удаляем уже созданные ресурсы
            self._delete_session_resources({
                "file_id": file_id if 'file_id' in locals() else None,
                "search_index_id": search_index_id if 'search_index_id' in locals() else None,
                "assistant_id": assistant_id if 'assistant_id' in locals() else None,
                "thread_id": thread_id if 'thread_id' in locals() else None
            })
            raise RuntimeError(f"Failed to create session: {str(e)}")

    def ask_assistant(self, assistant_id: str, question: str) -> Dict[str, Any]:
        """Задает вопрос ассистенту Yandex AI Assistant API в указанной сессии"""
        if assistant_id not in self.sessions:
            raise ValueError("Session not found")

        session = self.sessions[assistant_id]

        # Отправка сообщения
        self._make_request(
            "POST",
            "https://rest-assistant.api.cloud.yandex.net/assistants/v1/messages",
            {
                "threadId": session['thread_id'],
                "content": {"content": [{"text": {"content": question}}]}
            }
        )

        # Запуск ассистента
        run_data = self._make_request(
            "POST",
            "https://rest-assistant.api.cloud.yandex.net/assistants/v1/runs",
            {
                "assistantId": session['assistant_id'],
                "threadId": session['thread_id']
            }
        )
        run_id = run_data['id']

        # Ожидаем завершения
        start_time = time.time()
        while time.time() - start_time < 60:
            run_status = self._make_request(
                "GET",
                f"https://rest-assistant.api.cloud.yandex.net/assistants/v1/runs/{run_id}"
            )

            status = run_status.get('state', {}).get('status')
            if status == 'COMPLETED':
                return run_status['state']['completed_message']['content']['content'][0]['text']['content']
            elif status == 'FAILED':
                raise RuntimeError("Assistant execution failed")

            time.sleep(2)

        raise TimeoutError("Assistant response timeout")

    def delete_assistant(self, assistant_id: str) -> None:
        """Удаляет ассистента Yandex AI Assistant API и все связанные ресурсы"""
        if assistant_id not in self.sessions:
            raise ValueError("Session not found")

        session = self.sessions.pop(assistant_id)
        self._delete_session_resources(session)

    def list_assistants(self) -> List[dict]:
        """Возвращает список всех ассистентов"""
        pass
