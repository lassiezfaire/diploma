from typing import List, Dict

from yandex_cloud_ml_sdk import YCloudML
from yandex_cloud_ml_sdk.auth import APIKeyAuth

from app.llm.basellmodel import BaseLLModel
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

        # operation = (
        #     self.model.run_deferred(messages)
        # )
        #
        # result = operation.wait()

        result = (
            self.model.run(messages)
        )

        return result
