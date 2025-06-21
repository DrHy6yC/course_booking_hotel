from datetime import datetime


from sqlalchemy import CheckConstraint, Integer, String

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.database import BaseORM


class UsersORM(BaseORM):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint('age >= 0 AND age <= 150', name='age_range_check'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(length=100), unique=True)
    email: Mapped[str] = mapped_column(String(length=100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(length=100))
    name: Mapped[str] = mapped_column(String(length=100))
    age: Mapped[int] = mapped_column(Integer())
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp(),
        nullable = False
    )
