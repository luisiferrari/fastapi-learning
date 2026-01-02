from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserCreateModel, UserModel
from .service import UserService
from src.db.main import get_session

user_service = UserService()

auth_router = APIRouter()

@auth_router.get("/all_users", response_model=list[UserModel])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    users = await user_service.get_all_users(session=session)
    return users

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email    
    print(email)
    user_exists = await user_service.user_exists(email=email, session=session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with this email already exists.")
    new_user = await user_service.create_user(user_data=user_data, session=session)
    return {"message": "User created successfully.", "user_id": str(new_user.uid)}