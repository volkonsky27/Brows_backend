from celery import Celery


celery_app = Celery(
    "tasks",
    broker="redis://192.168.58.138:6379",
    include=["tasks.tasks"]
)
