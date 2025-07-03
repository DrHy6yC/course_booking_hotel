from fastapi import APIRouter
from fastapi_cache.decorator import cache
from src.api.dependencies import DBDep
from src.custom_class import KeyBuilderCustom
from src.schemas.facility import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Услуги"])


custom_key_builder = KeyBuilderCustom(my_key="all_facilities")


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
    return {"status": "OK", "facility": result}
