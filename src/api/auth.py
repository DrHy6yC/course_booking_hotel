from fastapi import APIRouter, Body, HTTPException, Response, status

from src.api.dependencies import DBDep, UserIdDep
from src.openapi_examples import admin_example,admin_login_example, user_example
from src.schemas.user import User, UserAdd, UserLogin, UserRequestAdd
from src.services.auth import AuthServices


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post(
    path="/register",
    summary="Регистрация новых пользователей",
    description="Все поля обязательны"
)
async def register_user(
        db: DBDep,
        data: UserRequestAdd = Body(
            openapi_examples={
              "1": admin_example,
              "2": user_example,
            },
        )
):
    hash_password = AuthServices().hashed_password(data.password)
    data_db = UserAdd(
        login=data.login,
        name=data.name,
        email=data.email,
        age=data.age,
        hashed_password=hash_password,
    )
    try:
        await db.users.add(data_db)
        await db.commit()
        return {"status": "OK"}
    except Exception as error:
        print(error)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"status": "Error - Пользователь с такими данными уже существует"},
        )


@router.post(
    path="/login",
    summary="Залогиниться",
    description="Зайти по логину и паролю"

)
async def login_user(
        response: Response,
        db: DBDep,
        data: UserLogin = Body(
            openapi_examples={
                "1": admin_login_example,
            }
        )
):
    user = await db.users.get_user_verify_email(data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"status": "Error - Пользователь с таким email не зарегистрирован"}
        )
    if not AuthServices().verify_password(data.password, user.hashed_password):
        raise  HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"status": "Error - Пароль не верный"}
        )
    access_token = AuthServices().create_access_token({"user_id": user.id})
    response.set_cookie(key="access_token", value=access_token)
    return access_token


@router.get(
    path="/me",
    summary="Получить активного пользователя",
    description="Ищет пользователя по информации из куков"
)
async def get_me(
        user_id: UserIdDep,
        db: DBDep,
) -> User:
    return await db.users.get_one_or_none(id=user_id)


@router.post(
    path="/logout",
    summary="Выйти",
    description="Выйти из под пользователя"
)
async def logout_user(response: Response):
    response.delete_cookie(key="access_token")
    return {"status": "OK"}