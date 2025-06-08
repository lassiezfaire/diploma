from app.config.api_config import yandex_settings
from app.llm_clients.base_client import BaseAIAssistant


class YandexAssistant(BaseAIAssistant):
    def __init__(self):
        """Инициализация клиента Yandex AI Assistant API с конфигурацией"""
        pass

    def ask_client(self):
        """Задать вопрос клиенту Yandex AI Assistant API"""
        pass

    def __del__(self):
        """Удалить клиент Yandex AI Assistant API"""
        pass
