from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from src.database import BaseORM


class BookingsORM(BaseORM):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey(column="rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey(column="users.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]

    @hybrid_property
    def total_coast(self) -> int:
        return self.price * (self.date_to - self.date_from).days
