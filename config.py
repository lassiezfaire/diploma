from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    grafana_url: str
    grafana_port: int
    grafana_token: str

    class Config:
        env_file = ".env"

settings = Settings()