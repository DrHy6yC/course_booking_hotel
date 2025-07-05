class CourseError(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundError(CourseError):
    detail = "Объект не найден"


class AllRoomsBusyError(CourseError):
    detail = "Все номера заняты"


class ObjectAlreadyExistsError(CourseError):
    detail = "Объект уже существует"
