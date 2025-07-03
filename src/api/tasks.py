import shutil

from fastapi import APIRouter, BackgroundTasks, UploadFile
from src.schemas.message import MessageReturn
from src.tasks.tasks import resize_image, resize_image_celery, sleep_task

router = APIRouter(prefix="/tasks", tags=["Задачи"])


@router.post(
    path="", summary="Создать задачу", description="Создаем задачу в Celery"
)
async def create_task() -> MessageReturn:
    # TODO: Починить типизацию
    sleep_task.delay()  # type: ignore
    return MessageReturn(status="OK")


def add_image(file: UploadFile) -> None:
    image_path = f"src/static/images/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(fsrc=file.file, fdst=new_file)


@router.post(
    path="/images",
    summary="Добавить картинку",
    description="Добавляем картинку в папку в static/images",
)
def add_image_celery(file: UploadFile) -> MessageReturn:
    image_path = f"src/static/images/{file.filename}"
    add_image(file)
    # TODO: Починить типизацию
    resize_image_celery.delay(image_path)  # type: ignore
    return MessageReturn(status="OK")


@router.post(
    path="/images_backgroundTasks",
    summary="Добавить картинку с помощью BackgroundTasks",
    description="Добавляем картинку в папку в static/images",
)
def add_image_background_tasks(
    file: UploadFile, background_tasks: BackgroundTasks
) -> MessageReturn:
    image_path = f"src/static/images/{file.filename}"
    add_image(file)
    background_tasks.add_task(resize_image, image_path)
    return MessageReturn(status="OK")
