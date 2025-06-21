from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.facility import FacilityAdd


router = APIRouter(prefix="/facilities", tags=["Услуги"])


@router.get(
    path="",
    summary="Получить все услуги",
    description="Получить список всех услуг которые есть в БД",
)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post(
    path="",
    summary="",
    description="",
)
async def create_facilities(db: DBDep, data_facilities: FacilityAdd):
    result = await db.facilities.add(data_facilities)
    await db.commit()
    return {"status": "OK", "facilities": result}