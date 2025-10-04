from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from src.router import get_user_info
from fastapi.responses import HTMLResponse


router = APIRouter(tags="Front", prefix="/front")
templates = Jinja2Templates(directory="templates")


@router.get('{telegram_id}')
async def get_user_info_front(request: Request, user=Depends(get_user_info)):
    user.update({"request": request})
    return templates.TemplateResponse("index1.html", user)