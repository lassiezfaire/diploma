from typing import List, Dict

from yandex_cloud_ml_sdk import YCloudML
from yandex_cloud_ml_sdk.auth import APIKeyAuth

from basellmodel import BaseLLModel
from app.config import settings

class YandexGPT5(BaseLLModel):
    def __init__(self,
                 folder_id: str,
                 auth: str,
                 model_name: str = "yandexgpt",
                 model_version: str = "rc",
                 temperature: float = 0.3):

        self.sdk = YCloudML(
            folder_id=folder_id,
            auth=APIKeyAuth(auth),
            enable_server_data_logging=False
        )

        self.model = self.sdk.models.completions(model_name=model_name, model_version=model_version)
        self.model = self.model.configure(temperature=temperature)

    def request(self, messages: List[Dict[str, str]]):

        result = (
            self.model.run(messages)
        )

        return result[0].text

def main() -> None:

    yandexgpt5 = YandexGPT5(settings.folder_id, auth=settings.yc_api_key)

    messages = [
        {
            "role": "system",
            "text": "Ты умный ассистент",
        },
        {
            "role": "user",
            "text": "Привет! Какими науками занимался Альберт Эйнштейн?",
        },
    ]

    print(yandexgpt5.request)


if __name__ == "__main__":
    main()
