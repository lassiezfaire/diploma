from app.config.yandex_config import yandex_settings
from . import BaseLLMClient


class YandexGPT5rc(BaseLLMClient):
    assistant_id: str = None
    thread_id: str = None

    def __init__(self):
        self.api_key = yandex_settings.yc_api_key
        self.folder_id = yandex_settings.yc_folder_id
        self.url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
        self.model = 'yandexgpt/rc'
        self.base_headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "application/json"
        }

    def _ask_llm_api(self, question: str, system_prompt=None):
        payload = {
            "modelUri": f'gpt://{self.folder_id}/{self.model}',
            "completionOptions": {
                "temperature": 0.3,
                "maxTokens": "100000",
                "reasoningOptions": {
                    "mode": "ENABLED_HIDDEN"
                }
            },
            "messages": [
                {"role": "system", "text": system_prompt},
                {"role": "user", "text": question}
            ]
        }
        result = self._post_request(self.url, payload)
        answer = result["result"]["alternatives"][0]["message"]["text"]
        return answer
