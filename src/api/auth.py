from datetime import datetime, timedelta, timezone


from fastapi import APIRouter, Body, HTTPException, status


import jwt
from passlib.context import CryptContext


from src.database import async_session_maker
from src.config import settings
from src.openapi_examples import admin_example,admin_login_example, user_example
from src.repositories.users import UsersRepository
from src.schemas.user import UserRequestAdd, UserAdd, UserLogin


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификайия"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTE)
    to_encode |= {"exp": expire}
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt



@router.post(
    path="/register",
    summary="Регистрация новых пользователей",
    description="Все поля обязательны"
)
async def register_user(
      data: UserRequestAdd = Body(
          openapi_examples={
              "1": admin_example,
              "2": user_example,
          },
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
        try:
            await UsersRepository(session).add(data_db)
            await session.commit()
            return {"status": "OK"}
        except Exception as error:
            print(error)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"status": "Error - Пользователь с такими данными уже сущестует"},
            )


@router.post(
    path="/login",
    summary="Залогиниться",
    description="Зайти по логину и паролю"

)
async def login_user(
        data: UserLogin = Body(
            openapi_examples={
                "1": admin_login_example,
            }
        )
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_verify_email(data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"status": "Error - Пользователь с таким email не зарегистрирован"}
            )
        if not verify_password(data.password, user.hashed_password):
            raise  HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"status": "Error - Пароль не верный"}
            )
        access_token = create_access_token({"user_id": user.id})
        return access_token
