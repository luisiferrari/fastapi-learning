from .model import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select


class UserService:
    async def get_user(email: str, session: AsyncSession):
        statement = select().where(User.email == email)
        result = await session.exec(statement)
        return result.first()