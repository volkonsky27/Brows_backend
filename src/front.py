from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.router import get_services

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_user_info_front(request: Request):
    req = {"request": request}
    return templates.TemplateResponse("index.html", req)


@router.get("/front/services", response_class=HTMLResponse)
async def get_user_info_front(request: Request, services=Depends(get_services)):
    for i in services:
        print(i)
    req = {"request": request}
    req.update({"services": services})
    return templates.TemplateResponse("services.html", req)
