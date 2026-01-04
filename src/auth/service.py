from .model import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc

from src.auth.schemas import UserCreateModel
from src.auth.utils import generate_hashed_password
from .model import User


class UserService:
    
    async def get_all_users(self, session: AsyncSession): # -> I personally addede this method so I dont have to keep checking the database manually
        statement = select(User).order_by(desc(User.create_at))
        result = await session.execute(statement)
        return result.scalars().all()
    
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.scalars(statement)
        return result.first()
    
    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email=email, session=session)
        return user is not None
    
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        
        """
        In this method, we receive the Schema UserCreateModel containing the data necessary to create a new user. We convert this schema into a dictionary using the model_dump() method. Then, we create a new instance of the User model by unpacking the dictionary using the ** syntax. This allows us to pass the key-value pairs of the dictionary as keyword arguments to the User constructor."""
        
        user_data_dict = user_data.model_dump()
        password = user_data_dict['password']
        user_data_dict.pop('password')
        new_user = User(
            **user_data_dict
        )
        
        new_user.password_hash = generate_hashed_password(password)
        new_user.role = 'user'
        
        session.add(new_user)
        
        await session.commit()
        await session.refresh(new_user)
        
        return new_user