import shutil

from fastapi import APIRouter, UploadFile

from src.tasks.tasks import sleep_task, resize_image

router = APIRouter(prefix="/tasks", tags=["Задачи"])


@router.post(
    path="",
    summary="Создать задачу",
    description="Создаем задачу в Celery"
)
async def create_task():
    sleep_task.delay()
    return {"status": "OK"}


@router.post(
    path="/images",
    summary="Добавить картинку",
    description="Добавляем картинку в папку в static/images"
)
def add_image(file: UploadFile):
    image_path = f"src/static/images/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(fsrc=file.file, fdst=new_file)
    resize_image.delay(image_path)
    return {"status": "OK"}