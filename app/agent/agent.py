from app.llm.base_client import BaseLLMClient
from app.grafana.client import GrafanaClient
from app.configs.config import settings


class Agent:
    def __init__(self, llm_client: BaseLLMClient):
        self.grafana_client = GrafanaClient(base_url=f"{settings.grafana_url}:{settings.grafana_port}/api",
                                            api_key=settings.grafana_token)

        self.llm_client = llm_client

    def process_request(self, user_prompt: str):

        data = self.llm_client.request(user_prompt=user_prompt)

        response = self.grafana_client.post("/dashboards/db", data=data)

        return response
