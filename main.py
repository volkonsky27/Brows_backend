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
    settings.DOMAIN
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Чтобы позволять отправлять куки
    allow_methods=["GET", "POST"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
        "Token",
    ],
)
app.include_router(router)
app.include_router(front_router)


if __name__ == "__main__":
    uvicorn.run(app, port="8080")
