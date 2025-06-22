import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from agent.router import router as agent_router
from voice.router import router as voice_router

app = FastAPI()
app.mount("/ui", StaticFiles(directory="ui"), name="static")

app.include_router(agent_router)
app.include_router(voice_router)


@app.get("/", include_in_schema=False, response_class=HTMLResponse)
def index():
    return RedirectResponse("/ui/index.html")


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return RedirectResponse(url="/ui/favicon.ico")


if __name__ == "__main__":
    uvicorn.run('app.main:app', host='127.0.0.1', port=80, reload=True)
