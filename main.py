import uvicorn
from fastapi import FastAPI
from src.router import router
from src.front import router as front_router
from src.config import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="Brows", version="1.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
origins = [
    settings.DOMAIN, "http://localhost:8080", "http://127.0.0.1:8080"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Чтобы позволять отправлять куки
    allow_methods=["GET", "POST"],
    allow_headers="*"
)
app.include_router(router)
app.include_router(front_router)


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
