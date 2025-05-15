from fastapi import APIRouter, HTTPException
from app.agent.agent import Agent
from app.llm.yandex_gpt_client import YandexGPT5Client
from app.configs.config import settings
from app.configs.logging_config import setup_logging
import logging

setup_logging()

router = APIRouter(prefix="/grafana", tags=["grafana"])


@router.post("/dashboard")
def create_dashboard(
        user_prompt: str = "Generate sample JSON dashboard for Grafana HTTP API. Include fields like folderId and overwrite",
        system_prompt: str = "You are experienced Grafana expert. Answer using JSON only"):
    agent = Agent(llm_client=YandexGPT5Client(
        folder_id=settings.folder_id,
        auth=settings.yc_api_key,
        system_prompt=system_prompt)
    )

    response = agent.process_request(user_prompt=user_prompt)

    if response.status_code == 200:
        logging.info(f"Дашборд успешно отправлен в Grafana")
        return response.json()
    else:
        logging.error(f"Ошибка при отправке дашборда в Grafana")
        raise HTTPException(status_code=response.status_code, detail="Error creating dashboard")
