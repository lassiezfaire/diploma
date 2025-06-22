from fastapi import APIRouter, HTTPException, UploadFile, File, Form

from app.agent.agent import AIAgent
from app.llm_clients.YandexGPT5rc import YandexGPT5rc
from app.config.logging_config import logger
from app.llm_clients.vseGPT import VseGPT



from pydantic import BaseModel
class Prompt(BaseModel):
    prompt: str


router = APIRouter()
assistant = VseGPT()
#assistant = YandexGPT5rc()

agent = AIAgent(assistant)


# Получает команду пользователя от frontend, спрашивает LLM, обрабатывает ответ и отдаёт команду в Grafana
@router.post("/command/")
def process_command(data: Prompt):
    try:
        response = agent.process_command(data.prompt)
    except Exception as e:
        print(e)
    return response


