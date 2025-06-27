from fastapi import APIRouter
from fastapi_cache import KeyBuilder
from fastapi_cache.decorator import cache
from typing import Optional, Any, Dict, Tuple, Union, Awaitable
from fastapi import Request, Response

from src.api.dependencies import DBDep
from src.schemas.facility import FacilityAdd


router = APIRouter(prefix="/facilities", tags=["Услуги"])


class CustomKeyBuilder(KeyBuilder):
    async def __call__(
            self,
            function: Any,
            namespace: str = "",
            request: Optional[Request] = None,
            response: Optional[Response] = None,
            *args,
            **kwargs,
    ) -> str:
        return ":all_facilities"


custom_key_builder = CustomKeyBuilder()

@router.get(
    path="",
    summary="Получить все услуги",
    description="Получить список всех услуг которые есть в БД",
)
@cache(expire=10, key_builder=custom_key_builder)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post(
    path="",
    summary="Добавление нового удобства",
    description="Добавление нового удобства в БД",
)
async def create_facilities(db: DBDep, data_facilities: FacilityAdd):
    result = await db.facilities.add(data_facilities)
    await db.commit()
    return {"status": "OK", "facilities": result}