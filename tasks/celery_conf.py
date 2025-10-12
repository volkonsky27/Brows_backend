from celery import Celery
from src.config import settings


celery_app = Celery(
    "tasks",
    broker=settings.REDIS,
    include=["tasks.tasks"]
)
