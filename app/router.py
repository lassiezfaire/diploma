from fastapi import APIRouter, HTTPException
from utils.http_client import grafana_client
from pydantic import BaseModel

router = APIRouter(prefix="/grafana", tags=["grafana"])

class DashboardCreateRequest(BaseModel):
    dashboard: dict
    overwrite: bool = False

@router.get("/dashboard/{dashboard_id}")
async def get_dashboard(dashboard_id: str):
    response = await grafana_client.get(f"/dashboards/uid/{dashboard_id}")
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching dashboard")

@router.post("/dashboard")
async def create_dashboard(request: DashboardCreateRequest):
    response = await grafana_client.post("/dashboards/db", data=request.model_dump())
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error creating dashboard")
