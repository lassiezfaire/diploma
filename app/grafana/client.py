from http.client import responses
from typing import Optional, Dict, Any

import httpx

from app.config.grafana_config import grafana_settings


class GrafanaClient:
    def __init__(self):
        self.grafana_url = grafana_settings.grafana_url
        self.grafana_token = grafana_settings.grafana_token
        self.grafana_db_uid = grafana_settings.dashboard_uid

        self.client = httpx.Client(
            base_url=self.grafana_url,
            headers={
                "Authorization": f"Bearer {self.grafana_token}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        )

    def get_dashboard(self, uid: str) -> dict:
        url = f'/api/dashboards/uid/{uid}'
        response = self.client.get(url)
        response.raise_for_status()
        json = response.json()
        dashboard = json['dashboard']
        return dashboard

    def update_dashboard(self, dashboard: str):
        url = '/api/dashboards/db'
        response = self.client.post(url, json=dashboard)
        response.raise_for_status()


grafana_client = GrafanaClient()
