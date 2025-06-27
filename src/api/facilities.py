import json

from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.init import redis_manager
from src.schemas.facility import FacilityAdd


router = APIRouter(prefix="/facilities", tags=["Услуги"])


@router.get(
    path="",
    summary="Получить все услуги",
    description="Получить список всех услуг которые есть в БД",
)
async def get_facilities(db: DBDep):
    facilities_from_cache = await redis_manager.get("facilities")
    if not facilities_from_cache:
        facilities = await db.facilities.get_all()
        facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_manager.set(key="facilities", value=facilities_json, expire=10)
        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts


@router.post(
    path="",
    summary="Добавление нового удобства",
    description="Добавление нового удобства в БД",
)
async def create_facilities(db: DBDep, data_facilities: FacilityAdd):
    result = await db.facilities.add(data_facilities)
    await db.commit()
    return {"status": "OK", "facilities": result}