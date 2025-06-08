from typing import List

from fastapi import APIRouter

from app.agent.agent import AIAssistant

router = APIRouter()

ai_assistant = AIAssistant()


@router.post("/assistant", response_model=dict)
def create_assistant():
    """Создает нового ассистента"""
    pass


@router.post("/assistant/{assistant_id}/ask", response_model=dict)
def ask_assistant():
    """Задаёт вопрос ассистенту"""
    pass


@router.delete("/assistant/{assistant_id}", response_model=dict)
def delete_assistant():
    """Удаляет ассистента"""
    pass


@router.get("/assistants", response_model=List[dict])
def list_assistants():
    """Выводит список всех ассистентов"""
    pass
