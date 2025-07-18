from sqlalchemy import delete, insert, select

from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import (
    FacilityDataMapper,
    RoomFacilityDataMapper,
)


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    mapper = RoomFacilityDataMapper

    async def set_room_facilities(
        self, room_id: int, facilities_ids: list[int]
    ) -> None:
        new_ids: list[int] = facilities_ids
        now_ids_query = select(self.model.facility_id).filter(
            self.model.room_id == room_id
        )
        res = await self.session.execute(now_ids_query)
        # TODO: Починить типизацию
        now_ids: list[int] = res.scalars().all()  # type: ignore
        delete_ids: list[int] = list(set(now_ids) - set(new_ids))
        create_ids: list[int] = list(set(new_ids) - set(now_ids))
        print(delete_ids)
        print(create_ids)
        if delete_ids:
            delete_m2m_facilities_stmt = delete(self.model).filter(
                self.model.room_id == room_id,
                self.model.facility_id.in_(delete_ids),
            )
            await self.session.execute(delete_m2m_facilities_stmt)
        if create_ids:
            create_m2m_facilities_stmt = insert(self.model).values(
                [
                    {"room_id": room_id, "facility_id": f_id}
                    for f_id in create_ids
                ]
            )
            await self.session.execute(create_m2m_facilities_stmt)
