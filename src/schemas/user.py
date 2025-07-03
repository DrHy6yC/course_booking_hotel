from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserBase(BaseModel):
    login: str
    name: str
    email: EmailStr
    age: Annotated[int, Field(ge=0, le=150)]


class UserRequestAdd(UserBase):
    password: str


class UserAdd(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    created_at: datetime


class UserWithHashedPass(User):
    hashed_password: str
