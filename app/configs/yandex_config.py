from pydantic_settings import BaseSettings


class YandexGPTSettings(BaseSettings):
    yc_api_key: str
    folder_id: str

    class Config:
        env_file = "yandex.env"


settings = YandexGPTSettings()
