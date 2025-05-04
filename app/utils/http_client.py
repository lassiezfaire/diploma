import httpx
from app.config import settings

class HttpClient:
    def __init__(self, base_url: str, api_key: str):
        self.client = httpx.Client(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        )

    def get(self, url: str):
        return self.client.get(url)

    def post(self, url: str, data: dict):
        return self.client.post(url, json=data)

grafana_client = HttpClient(base_url=f"{settings.grafana_url}:{settings.grafana_port}/api", api_key=settings.grafana_token)
