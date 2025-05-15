import json
import logging

from yandex_cloud_ml_sdk import YCloudML
from yandex_cloud_ml_sdk.auth import APIKeyAuth

from app.llm.base_client import BaseLLMClient
from app.configs.logging_config import setup_logging

setup_logging()


class YandexGPT5Client(BaseLLMClient):
    def __init__(self,
                 folder_id: str,
                 auth: str,
                 system_prompt: str,
                 model_name: str = "yandexgpt",
                 model_version: str = "rc",
                 temperature: float = 0.1):

        self.sdk = YCloudML(
            folder_id=folder_id,
            auth=APIKeyAuth(auth),
            enable_server_data_logging=False
        )

        self.model = self.sdk.models.completions(model_name=model_name, model_version=model_version)
        self.model = self.model.configure(temperature=temperature)

        self.system_prompt = system_prompt

    def request(self, user_prompt: str):

        logging.info(f"Пользовательский промпт: {user_prompt}")
        logging.info(f"Системный промпт: {self.system_prompt}")

        messages = [
            {
                "role": "system",
                "text": self.system_prompt,
            },
            {
                "role": "user",
                "text": user_prompt,
            },
        ]

        request_result = self.model.run(messages)

        result_role = request_result.alternatives[0].role
        result_text = request_result.alternatives[0].text

        data = json.loads(result_text.replace("```", "").strip())

        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        logging.info(f"JSON представление дашборда Grafana: \n{json_data}")

        return data
