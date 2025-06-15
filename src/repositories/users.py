from src.models.users import UsersORM
from src.repositories.base import BaseRepository
from src.schemas.user import User


class UsersRepository(BaseRepository):
    model = UsersORM
    schema = User
