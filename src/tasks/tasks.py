from time import sleep

from src.tasks.celery_app import celery_instance


@celery_instance.task
def sleep_task():
    sleep(5)
    print("Задача выполнена")
