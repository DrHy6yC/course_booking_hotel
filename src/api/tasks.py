from fastapi import APIRouter

from src.tasks.tasks import sleep_task

router = APIRouter(prefix="/tasks", tags=["Задачи"])


@router.post(
    path="",
    summary="Создать задачу",
    description="Создаем задачу в Celery"
)
async def create_task():
    sleep_task.delay()
    return {"status": "OK"}
