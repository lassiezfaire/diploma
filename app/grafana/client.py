from typing import Optional, Dict, Any

import httpx

from app.config.api_config import grafana_settings


class GrafanaClient:
    def __init__(self):
        self.grafana_url = grafana_settings.grafana_url
        self.grafana_port = grafana_settings.grafana_port
        self.grafana_token = grafana_settings.grafana_token

        self.client = httpx.Client(
            base_url=f'{self.grafana_url}:{self.grafana_port}',
            headers={
                "Authorization": f"Bearer {self.grafana_token}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        )

    def get(self, endpoint: str) -> Optional[Dict[str, Any]]:
        response = self.client.get(endpoint)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: dict) -> Optional[Dict[str, Any]]:
        response = self.client.post(endpoint, json=data)
        response.raise_for_status()
        return response.json()


grafana_client = GrafanaClient()
