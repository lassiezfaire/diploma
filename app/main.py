from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.router import router

app = FastAPI()

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

app.include_router(router)

# uvicorn app.main:app --host 127.0.0.1 --port 80 --reload
