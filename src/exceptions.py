class CourseError(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundError(CourseError):
    detail = "ERROR - Объект не найден"


class AllRoomsBusyError(CourseError):
    detail = "ERROR - Все номера заняты"


class ObjectAlreadyExistsError(CourseError):
    detail = "ERROR - Объект уже существует"

class InvalidTimeRangeError(CourseError):
    detail = "ERROR - Начальное время не может быть позже конечного."
