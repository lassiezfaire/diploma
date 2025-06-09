import logging
import os
import tempfile
from typing import Annotated, Any, Dict, List

from fastapi import APIRouter, HTTPException, UploadFile, File, Form

from app.agent.agent import AIAgent
from app.llm_clients.yandex_client import YandexClient

router = APIRouter()

yandex_assistant = YandexClient()
agent = AIAgent(yandex_assistant)

system_prompt = """
    You're professional Grafana user. You will generate Grafana HTTP API dashboards. Answer in JSON format only.
"""


@router.post("/assistant", response_model=Dict[str, Any])
def create_assistant(
        system_prompt: str = Form(default=system_prompt),
        file: Annotated[UploadFile, File(description="JSON файл для ассистента")] = None,
) -> Dict[str, Any]:
    """Создает новую сессию с ассистентом (синхронная версия)"""
    if not file:
        raise HTTPException(status_code=400, detail="Необходимо загрузить файл")

    try:
        if not file.filename.lower().endswith(".json"):
            raise HTTPException(400, "Поддерживаются только JSON файлы")

        with tempfile.NamedTemporaryFile(mode="wb", suffix=".json", delete=False) as tmp:
            content = file.file.read()  # Синхронное чтение
            tmp.write(content)
            file_path = tmp.name

        session_id = agent.create_agent(
            system_prompt=system_prompt,
            file_path=file_path,
        )

        try:
            os.unlink(file_path)
        except Exception as e:
            logging.warning(f"Failed to delete temp file: {str(e)}")

        return {"session_id": session_id, "status": "created"}

    except HTTPException:
        raise
    except Exception as e:
        if "file_path" in locals():
            try:
                os.unlink(file_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/assistant/{assistant_id}/ask", response_model=Dict[str, Any])
def ask_assistant(
        session_id: str,
        user_prompt: str
):
    """Задает вопрос ассистенту в указанной сессии"""
    try:
        response = agent.request(
            session_id=session_id,
            question=user_prompt
        )
        return {
            "response": response,
            "session_id": session_id
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/assistant/{assistant_id}")
def delete_assistant(session_id: str):
    """Закрывает сессию и освобождает ресурсы"""
    try:
        agent.delete_agent(session_id)
        return {"status": "deleted", "session_id": session_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/assistants", response_model=List[dict])
def list_assistants() -> List[dict]:
    """Выводит список всех ассистентов"""
    pass
