from pydantic_settings import BaseSettings


class GrafanaSettings(BaseSettings):
    grafana_url: str
    grafana_port: int
    grafana_token: str

    class Config:
        env_file = "grafana.env"


settings = GrafanaSettings()
