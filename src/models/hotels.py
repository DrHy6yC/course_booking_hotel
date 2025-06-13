from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.database import BaseORM


class HotelsORM(BaseORM):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(length=100))
    location: Mapped[str]
