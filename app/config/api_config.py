from pydantic_settings import BaseSettings
from pydantic import Field


class YandexSettings(BaseSettings):
    yc_api_key: str = Field(..., env="YC_API_KEY")
    folder_id: str = Field(..., env="YC_FOLDER_ID")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


class GrafanaSettings(BaseSettings):
    grafana_url: str = Field(..., env="GRAFANA_URL")
    grafana_port: str = Field(..., env="GRAFANA_PORT")
    grafana_token: str = Field(..., env="GRAFANA_TOKEN")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


yandex_settings = YandexSettings()
grafana_settings = GrafanaSettings()
