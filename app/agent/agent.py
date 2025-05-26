from app.llm.base_client import BaseLLMClient
from app.grafana.client import GrafanaClient
from app.grafana.client import grafana_client


class Agent:
    def __init__(self, llm_client: BaseLLMClient):
        self.grafana_client = grafana_client

        self.llm_client = llm_client

    def process_request(self, user_prompt: str):

        data = self.llm_client.request(user_prompt=user_prompt)

        response = self.grafana_client.post("/api/dashboards/db", data=data)

        return response
