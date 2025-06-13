from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from src.database import BaseORM


class RoomsORM(BaseORM):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey(column="hotels.id"))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]

