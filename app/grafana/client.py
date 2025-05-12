import httpx


class GrafanaClient:
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
