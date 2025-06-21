from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import BaseORM


class FacilitiesORM(BaseORM):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(length=100))


class RoomsFacilitiesORM(BaseORM):
    __tablename__ = "rooms_facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey(column="rooms.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey(column="facilities.id"))
