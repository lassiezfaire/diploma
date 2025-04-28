from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routers import grafana

app = FastAPI()

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

app.include_router(grafana.router)

# uvicorn main:app --reload
