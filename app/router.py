from fastapi import APIRouter, HTTPException
from app.agent.agent import Agent
from app.llm.yandex_gpt_client import YandexGPT5Client
from app.config import settings

router = APIRouter(prefix="/grafana", tags=["grafana"])

@router.post("/dashboard")
def create_dashboard(user_text: str = "Generate sample JSON dashboard for Grafana HTTP API",
                     system_prompt: str = "You are experienced Grafana expert. Answer using JSON only"):
    agent = Agent(llm_client=YandexGPT5Client(
        folder_id=settings.folder_id,
        auth=settings.yc_api_key,
        system_prompt=system_prompt)
    )

    response = agent.process_request(message=user_text)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error creating dashboard")
