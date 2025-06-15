from fastapi import APIRouter, Body
from passlib.context import CryptContext


from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.user import UserRequestAdd, UserAdd


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификайия"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post(
    path="/register",
    summary="Регистрация новых пользователей",
    description="Все поля обязательны"
)
async def register_user(
      data: UserRequestAdd = Body(
          openapi_examples={
              "1": {
                  "summary": "Админ",
                  "value":{
                      "login":"di",
                      "name": "admin",
                      "email": "admin@h.ru",
                      "age": "12",
                      "password": "111",
                  }
              },
              "2": {
                  "summary": "Пользователь",
                  "value":{
                      "login":"Zurab",
                      "name": "Ashot",
                      "email": "za@h.ru",
                      "age": "12",
                      "password": "000",
                  }
              }
          }
      )
):
    hash_password = pwd_context.hash(data.password)
    data_db = UserAdd(
        login=data.login,
        name=data.name,
        email=data.email,
        age=data.age,
        hashed_password=hash_password,
    )
    async with async_session_maker() as session:
        await UsersRepository(session).add(data_db)
        await session.commit()

    return {"status": "OK"}
