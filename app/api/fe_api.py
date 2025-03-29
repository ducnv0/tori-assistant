from fastapi import APIRouter
from fastapi.responses import RedirectResponse

fe_router = APIRouter()


@fe_router.get('/')
async def redirect_to_fe():
    return RedirectResponse(url='/static/index.html')
