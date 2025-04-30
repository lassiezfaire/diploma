from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from router import router

app = FastAPI()

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

app.include_router(router)

# uvicorn main:app --reload
