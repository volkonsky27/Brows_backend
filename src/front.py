from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from src.router import get_user_info
from fastapi.responses import HTMLResponse


router = APIRouter(prefix="/front")
templates = Jinja2Templates(directory="templates")


@router.get("/{telegram_id}/", response_class=HTMLResponse)
async def get_user_info_front(telegram_id: int, request: Request):
    user = await get_user_info(telegram_id)
    user.update({"request": request})
    return templates.TemplateResponse("index1.html", user)
