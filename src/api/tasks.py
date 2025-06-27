import shutil

from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.tasks.tasks import sleep_task, resize_image, resize_image_celery

router = APIRouter(prefix="/tasks", tags=["Задачи"])


@router.post(
    path="",
    summary="Создать задачу",
    description="Создаем задачу в Celery"
)
async def create_task():
    sleep_task.delay()
    return {"status": "OK"}


def add_image(file: UploadFile):
    image_path = f"src/static/images/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(fsrc=file.file, fdst=new_file)


@router.post(
    path="/images",
    summary="Добавить картинку",
    description="Добавляем картинку в папку в static/images"
)
def add_image_celery(file: UploadFile):
    image_path = f"src/static/images/{file.filename}"
    add_image(file)
    resize_image_celery.delay(image_path)
    return {"status": "OK"}

@router.post(
    path="/images_backgroundTasks",
    summary="Добавить картинку с помощью BackgroundTasks",
    description="Добавляем картинку в папку в static/images"
)
def add_image_BackgroundTasks(file: UploadFile, background_tasks: BackgroundTasks):
    image_path = f"src/static/images/{file.filename}"
    add_image(file)
    background_tasks.add_task(resize_image, image_path)
    return {"status": "OK"}