from pydantic_settings import BaseSettings
from pydantic import Field


class GrafanaSettings(BaseSettings):
    grafana_url: str = Field(..., env="GRAFANA_URL")
    grafana_token: str = Field(..., env="GRAFANA_TOKEN")
    dashboard_uid: str = Field(..., env="DASHBOARD_UID")

    class Config:
        env_file = "..\\.env"
        extra = "allow"


grafana_settings = GrafanaSettings()
