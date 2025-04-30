import httpx
from config import settings

class HttpClient:
    def __init__(self, base_url: str, api_key: str):
        self.client = httpx.AsyncClient(base_url=base_url, headers={"Authorization": f"Bearer {api_key}"})

    async def get(self, url: str):
        return await self.client.get(url)

    async def post(self, url: str, data: dict):
        return await self.client.post(url, json=data)

grafana_client = HttpClient(base_url=f"{settings.grafana_url}:{settings.grafana_port}/api", api_key=settings.grafana_token)
