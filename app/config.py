from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    grafana_url: str
    grafana_port: int
    grafana_token: str
    yc_api_key: str
    folder_id: str

    class Config:
        env_file = "app\\.env"

settings = Settings()