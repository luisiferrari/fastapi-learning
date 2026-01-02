from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta, datetime

from .schemas import UserCreateModel, UserModel,UserLoginModel
from .service import UserService
from .utils import create_access_token, decode_token, verify_password
from src.db.main import get_session


user_service = UserService()

auth_router = APIRouter()

REFRESH_TOKEN_EXPIRY_SECONDS = 3600*24*2  # 2 days

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

@auth_router.post("/login")
async def login_user(user_loggin_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = user_loggin_data.email
    password = user_loggin_data.password
    
    user = await user_service.get_user_by_email(email=email, session=session)
    
    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        
        if password_valid:
            access_token = create_access_token(
                user_data={
                    "uid": str(user.uid),
                    "username": user.username,
                    "email": user.email,
                },
                refresh=False,
                expire=timedelta(seconds=600) # 10 minutes
            )
            
            refresh_token = create_access_token(
                user_data={
                    "uid": str(user.uid),
                    "username": user.username,
                    "email": user.email,
                },
                refresh=True,
                expire=timedelta(seconds=REFRESH_TOKEN_EXPIRY_SECONDS)
            )
            return JSONResponse(
                content={
                    "message": "Login successful.",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "uid": str(user.uid),
                        "username": user.username,
                        "email": user.email
                    }
                }
            )
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password.")
    