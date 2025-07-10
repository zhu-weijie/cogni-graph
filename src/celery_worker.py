from celery import Celery

from src.config import settings

celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BROKER_URL,
)

celery_app.conf.update(
    task_track_started=True,
)


@celery_app.task
def add(x, y):
    return x + y
