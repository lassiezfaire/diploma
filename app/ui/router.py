from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/index", include_in_schema=False, response_class=HTMLResponse)
def index():
    return "/ui/mainpage"  # RedirectResponse("/UI/index.html")


@router.get("/favicon.ico", include_in_schema=False)
def favicon():
    return "/ui/favicon"  # RedirectResponse(url="/UI/favicon.ico")
