from typing import List
from fastapi import UploadFile
from fastapi import APIRouter, HTTPException, Response, Depends

from app.models import QuestionRequest, AssistantResponse
from app.agent.agent import Agent
from app.llm.yc_ai_assistant import YandexAIAssistant

router = APIRouter()


def get_agent() -> Agent:
    yandex_assistant = YandexAIAssistant()
    return Agent(ai_assistant=yandex_assistant)


@router.post("/sessions", response_model=dict)
async def create_session(
        files: List[UploadFile],
        agent: Agent = Depends(get_agent)
):
    """Создает новую сессию с загруженными файлами"""
    try:
        session_id = agent.create_session(files=files)
        return {"session_id": session_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/sessions/{session_id}", status_code=204)
async def close_session(
        session_id: str,
        agent: Agent = Depends(get_agent)
):
    """Закрывает сессию и освобождает ресурсы"""
    try:
        agent.ai_assistant.close_session(session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session cleanup error: {str(e)}")

    return Response(status_code=204)
