from pydantic_settings import BaseSettings
from pydantic import Field


class YandexSettings(BaseSettings):
    yc_api_key: str = Field(..., env="YC_API_KEY")
    yc_folder_id: str = Field(..., env="YC_FOLDER_ID")

    class Config:
        env_file = "../.env"
        extra = "allow"


yandex_settings = YandexSettings()
