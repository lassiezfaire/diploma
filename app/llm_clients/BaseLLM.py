from abc import ABC, abstractmethod
from typing import Optional

import requests
from pydantic import BaseModel
from app.config.logging_config import logger


class LLM_Response(BaseModel):
    http_status: Optional[int] = None
    answer: Optional[str] = None
    error: Optional[str] = None
    tokens: Optional[int] = None


# базовый абстрактный класс для работы с внешними нейронками
# наследники класса должны реализовать запросы к нейронке с аутентификацией и извлечения результатов из ответа нейронки
# при необходимости можно определить методы для пре- и пост-обработки ответов нейронки
class BaseLLMClient(ABC):
    system_prompt = None
    base_headers = []
    model = ""

    # метод для пользователя данного класса.
    def ask_assistant(self, user_prompt: str, system_prompt: str = None) -> LLM_Response:
        user_prompt = self._preprocess(user_prompt, system_prompt)
        response = self._ask_llm_api(user_prompt, system_prompt)
        response = self._postprocess(response)
        return response

    # выполняет предварительную обработку вопроса пользователя,
    # можно переопределить в наследнике, добавив дополнительную логику, специфическую для конкретной LLM
    def _preprocess(self, user_prompt: str, system_prompt) -> str:
        return user_prompt

    # должен реализовать логику обращения к API конкретной LLM
    @abstractmethod
    def _ask_llm_api(self, user_prompt: str, system_prompt=None) -> LLM_Response:
        pass

    # Выполняет обработку ответа нейронки
    # Можно переопределить в наследнике, добавив доплнительную логику, специческую для конкретной LLM
    def _postprocess(self, response) -> LLM_Response:
        return response

    # Вспомогательный метод, который могут использовать наследники для выполнения HTTP POST запросов
    def _post_request(self, url: str, payload: dict = None) -> requests.Response:
        response = requests.post(url, headers=self.base_headers, json=payload)
        return response

    # Вспомогательный метод, который могут использовать наследники для выполнения HTTP GET запросов
    def _get_request(self, url) -> requests.Response:
        response = requests.get(url, headers=self.base_headers)
        return response
