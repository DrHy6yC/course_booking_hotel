from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request, status
from pydantic import BaseModel

from src.connectors.database_init import async_session_maker
from src.services.auth import AuthServices
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[
        int | None, Query(default=1, description="Номер страницы", ge=1)
    ]
    per_page: Annotated[
        int | None,
        Query(
            default=None,
            description="Количество отелей на странице",
            ge=1,
            le=10,
        ),
    ]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    access_token = request.cookies.get("access_token", None)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": "Error - нет активного пользователя, залогиньтесь"
            },
        )
    return access_token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    payload = AuthServices().decoded_access_token(token)
    user_id = payload["user_id"]
    return user_id


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factories=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
