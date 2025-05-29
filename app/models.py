from pydantic import BaseModel
from typing import Optional, List
from fastapi import UploadFile


class QuestionRequest(BaseModel):
    question: str
    model: str = "yandexgpt"  # или "gigachat" и др.


class FileUploadRequest(BaseModel):
    files: Optional[List[UploadFile]] = None


class AssistantResponse(BaseModel):
    answer: str
    model: str
    grafana_status: Optional[str] = None
