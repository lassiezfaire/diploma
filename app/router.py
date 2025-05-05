from fastapi import APIRouter, HTTPException
from app.utils.http_client import grafana_client
from app.controller.controller import process_request
from pydantic import BaseModel

router = APIRouter(prefix="/grafana", tags=["grafana"])

class DashboardCreateRequest(BaseModel):
    dashboard: dict
    overwrite: bool = False

@router.get("/dashboard/{dashboard_id}")
def get_dashboard(dashboard_id: str):
    response = grafana_client.get(f"/dashboards/uid/{dashboard_id}")
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching dashboard")

@router.post("/dashboard")
def create_dashboard(system_text: str, user_test: str):

    messages = [
        {
            "role": "system",
            "text": system_text,
        },
        {
            "role": "user",
            "text": user_test,
        },
    ]

    response = process_request(messages=messages)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error creating dashboard")
