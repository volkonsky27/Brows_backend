import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.router import router
from src.front import router as front_router


app = FastAPI(title="Brows", version="1.0")
app.include_router(router)
app.include_router(front_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
uvicorn.run(app, port="8080")
