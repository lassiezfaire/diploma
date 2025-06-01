import pathlib
import uuid
from typing import List, Optional
import httpx

from yandex_cloud_ml_sdk import YCloudML
from yandex_cloud_ml_sdk.search_indexes import (
    StaticIndexChunkingStrategy,
    TextSearchIndexType,
)
from fastapi import UploadFile

from app.configs.yandex_config import settings
# from app.configs.logging_config import setup_logging
import logging
from app.llm.base_ai_assistant import BaseAIAssistant


class YandexAIAssistant(BaseAIAssistant):
    def __init__(self):
        self.sdk = YCloudML(
            folder_id=settings.folder_id,
            auth=settings.yc_api_key,
            enable_server_data_logging=False
        )

        self.sessions = {}
        self.api_url = "https://rest-assistant.api.cloud.yandex.net/assistants/v1"

    def create_session(self, files: Optional[List[UploadFile]] = None) -> str:
        """Создает сессию с загруженными файлами"""
        session_id = str(uuid.uuid4())
        files_list = []

        if files:
            # Обработка загруженных файлов
            for file in files:
                temp_path = pathlib.Path(f"temp_{file.filename}")
                with open(temp_path, "wb") as buffer:
                    buffer.write(file.file.read())

                uploaded_file = self.sdk.files.upload(
                    temp_path,
                    ttl_days=5,
                    expiration_policy="static",
                )
                files_list.append(uploaded_file)
                temp_path.unlink()

            # Создание индекса для файлов
            operation = self.sdk.search_indexes.create_deferred(
                files_list,
                index_type=TextSearchIndexType(
                    chunking_strategy=StaticIndexChunkingStrategy(
                        max_chunk_size_tokens=1024,
                        chunk_overlap_tokens=512,
                    )
                ),
            )
            search_index = operation.wait()
            tool = self.sdk.tools.search_index(search_index)
        else:
            search_index = None
            tool = None

        assistant = self.sdk.assistants.create("yandexgpt", tools=[tool] if tool else None)
        print(assistant)
        thread = self.sdk.threads.create()

        self.sessions[session_id] = {
            "assistant": assistant,
            "thread": thread,
            "search_index": search_index,
            "files": files_list
        }

        print(self.sessions)

        return session_id

    async def _delete_assistant_via_api(self, assistant_id: str):
        """Удаление ассистента через REST API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self.api_url}/assistants/{assistant_id}",
                    params={"assistantId": assistant_id},
                    headers={"Authorization": f"Api-Key {settings.yc_api_key}"}
                )
                response.raise_for_status()
        except Exception as e:
            logging.error(f"Failed to delete assistant {assistant_id}: {str(e)}")
            raise

    def close_session(self, session_id: str):
        """Закрывает сессию и освобождает ресурсы"""
        if session_id not in self.sessions:
            return

        session = self.sessions.pop(session_id)

        try:
            # 1. Получаем ID ассистента
            assistant_id = session["assistant"].id

            # 2. Удаляем через API
            import asyncio
            asyncio.run(self._delete_assistant_via_api(assistant_id))

            # 3. Удаляем остальные ресурсы
            if "search_index" in session:
                session["search_index"].delete()
            if "thread" in session:
                session["thread"].delete()
            if "files" in session:
                for file in session["files"]:
                    file.delete()

        except Exception as e:
            logging.error(f"Ошибка при очистке сессии {session_id}: {e}")

    def list_sessions(self) -> List[str]:
        """Возвращает список активных session_id"""
        return list(self.sessions.keys())
