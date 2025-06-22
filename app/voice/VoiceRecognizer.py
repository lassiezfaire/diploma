import httpx
import os
import time
from dotenv import load_dotenv

from fastapi import HTTPException

from app.llm_clients.YandexGPT5rc import YandexGPT5rc
from app.config.yandex_config import yandex_settings

load_dotenv()


class Token:
    iam: str = ""
    expiresAt: str = ""


class VoiceRecognizer:
    htmlFile: str = "recorder.html"
    scriptFile: str = "recorder.js"
    refresh_token_url: str = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
    yandex_passport_oauth_token: str = os.getenv("VOICE_RECOGNIZER_PASSPORT_TOKEN")
    folder_id: str = yandex_settings.yc_folder_id
    recognize_url = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"
    token: str = os.getenv("VOICE_RECOGNIZER_TOKEN")
    token_expires_at: str = "2025-06-15T04:03:16.762495114Z"

    def _read_file(self, file_name: str):
        """
        :return: Возвращает содержание файла file_name, который хранится в той же папке, где данный скрипт
        """
        dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(dir, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            source = file.read()
        return source

    def _is_token_expired(self) -> bool:
        trimmed_str = self.token_expires_at.split('.')[0]
        time_struct = time.strptime(trimmed_str, "%Y-%m-%dT%H:%M:%S")
        timestamp = time.mktime(time_struct)
        return (self.token == "") or (time.time() >= timestamp)

    def _refresh_token(self):
        #    Обновляет IAM токен
        with httpx.Client() as client:
            response = client.post(
                self.refresh_token_url,
                json={"yandexPassportOauthToken": self.yandex_passport_oauth_token},
            )
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch token")
        token_data = response.json()
        self.token = token_data['iamToken']
        self.token_expires_at = token_data['expiresAt']

    def process_voice(self, audio):
        if self._is_token_expired():
            self._refresh_token()
        headers = {
            "Authorization": f"Bearer {self.token}",
        }
        params = {
            "topic": "general",
            "lang": ["ru-RU", "en-US"],
            "folderId": self.folder_id,
        }
        with httpx.Client() as client:
            response = client.post(self.recognize_url, headers=headers, params=params, content=audio)
        if response.status_code == 200:
            text = response.json()['result']
        else:
            text = "Ошибка!!! " + response.json()['error_message']
        return text

    # Пытается с помощью ИИ заменить транслит в английских терминах на латиницу
    def correct_translit(self, text: str) -> str:
        ya_assistant = YandexGPT5rc()
        text = ya_assistant._ask_llm_api(text,
                                        "В тексте некоторые английский термины и названия слова записаны кириллицей. Замени в этих словах кириллицу на латиницу")
        return text
