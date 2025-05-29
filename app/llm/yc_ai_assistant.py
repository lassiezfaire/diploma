import pathlib
import uuid
from typing import List

from yandex_cloud_ml_sdk import YCloudML
from yandex_cloud_ml_sdk.search_indexes import (
    StaticIndexChunkingStrategy,
    TextSearchIndexType,
)

from app.configs.yandex_config import settings
from app.llm.base_ai_assistant import BaseAIAssistant


class AssistantSession(BaseAIAssistant):
    def __init__(self):
        self.sdk = YCloudML(
            folder_id=settings.folder_id,
            auth=settings.yc_api_key,
            enable_server_data_logging=False
        )

        self.sessions = {}

    def create_session(self, files_path: str = None) -> str:
        """Создает новую сессию ассистента"""
        session_id = str(uuid.uuid4())

        files = []

        # Загружаем файлы
        paths = pathlib.Path(files_path).iterdir()
        for path in paths:
            file = self.sdk.files.upload(
                path,
                ttl_days=5,
                expiration_policy="static",
            )
            files.append(file)

        # Создаем индекс
        operation = self.sdk.search_indexes.create_deferred(
            files,
            index_type=TextSearchIndexType(
                chunking_strategy=StaticIndexChunkingStrategy(
                    max_chunk_size_tokens=1024,
                    chunk_overlap_tokens=512,
                )
            ),
        )

        search_index = operation.wait()
        tool = self.sdk.tools.search_index(search_index)
        assistant = self.sdk.assistants.create("yandexgpt", tools=[tool])
        thread = self.sdk.threads.create()

        self.sessions[session_id] = {
            "assistant": assistant,
            "thread": thread,
            "search_index": search_index,
            "files": files
        }

        return session_id

    def ask_question(self, session_id: str, question: str) -> dict:
        """Задает вопрос ассистенту в указанной сессии"""
        if session_id not in self.sessions:
            raise ValueError("Сессия не найдена")

        session = self.sessions[session_id]
        session["thread"].write(question)

        run = session["assistant"].run(session["thread"])
        result = run.wait()

        return {
            "answer": result.text
        }

    def close_session(self, session_id: str):
        """Закрывает сессию и освобождает ресурсы"""
        if session_id not in self.sessions:
            return

        session = self.sessions.pop(session_id)

        try:
            session["search_index"].delete()
            session["thread"].delete()
            session["assistant"].delete()

            for file in session["files"]:
                file.delete()
        except Exception as e:
            print(f"Ошибка при очистке сессии: {e}")

    def list_sessions(self) -> List[str]:
        """Возвращает список активных session_id"""
        return list(self.sessions.keys())
