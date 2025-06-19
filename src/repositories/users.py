from pydantic import EmailStr
from sqlalchemy import select


from src.models.users import UsersORM
from src.repositories.base import BaseRepository
from src.schemas.user import User, UserWithHashedPass


class UsersRepository(BaseRepository):
    model = UsersORM
    schema = User

    async def get_user_verify_email(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPass.model_validate(obj=model, from_attributes=True)

