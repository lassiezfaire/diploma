from typing import List
from fastapi import UploadFile
from fastapi import APIRouter, HTTPException, Response

from app.models import QuestionRequest, AssistantResponse
from app.agent.agent import Agent

router = APIRouter()


@router.post("/upload", response_model=dict)
async def upload_files(
        files: List[UploadFile],
        agent: Agent
):
    """Эндпоинт для предварительной загрузки файлов"""
    try:
        # Создаем временную сессию для загрузки файлов
        session_id = agent.ai_assistant.create_session(files=files)
        agent.ai_assistant.close_session(session_id)

        return {"status": "files_uploaded", "count": len(files)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask", response_model=AssistantResponse)
async def ask_question(
        request: QuestionRequest,
        agent: Agent,
        files: List[UploadFile]
):
    """Основной эндпоинт для вопросов к AI"""
    try:
        result = agent.process_request(
            user_prompt=request.question,
            files=files
        )

        return {
            "answer": result["llm_response"]["answer"],
            "model": result["llm_response"].get("model", "unknown"),
            "grafana_status": result["grafana_response"]["status"] if result["grafana_response"] else None
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/sessions/{session_id}", status_code=204)
async def close_session(
        session_id: str,
        agent: Agent
):
    """Закрывает сессию и освобождает ресурсы"""
    try:
        agent.ai_assistant.close_session(session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session cleanup error: {str(e)}")

    return Response(status_code=204)
