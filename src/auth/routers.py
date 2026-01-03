from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta, datetime

from sqlmodel import true

from .schemas import UserCreateModel, UserModel,UserLoginModel
from .service import UserService
from .utils import create_access_token, verify_password
from src.db.main import get_session
from .dependencies import RefreshTokenBearer, AccessTokenBearer
from src.db.redis import add_jti_to_blocklist


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
    
@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    
    # O RefreshTokenBearer me retorna um dict no formato abaixo:
    # {
    #     "user": {
    #         "uid": "40c07a54-74ba-461b-aa58-f203bdc9e0d0",
    #         "username": "teste1",
    #         "email": "auth@mail.com"
    #     },
    #     "exp": 1767563103,
    #     "jti": "7b1f8c05-42f1-471c-9c9b-f7a23d455699",
    #     "refresh": true
    # }
    
    # Isso porque essa classe herda do TokenBearer e no seu método __call__ ela decodifica o token
    # e retorna o payload (que é esse dict acima).
    # Luis, 02/01/2026.
    
    if token_details is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid refresh token.")
    
    expire_refresh_toke = datetime.fromtimestamp(token_details.get("exp"))
    print(expire_refresh_toke)
    
    if expire_refresh_toke < datetime.now():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Refresh token has expired.")

    user_data = token_details.get("user") # user contains {"uid", "username", "email"}
    
    access_token = create_access_token(
        user_data=user_data,
        refresh=False,
        expire=timedelta(seconds=600) # 10 minutes
    )
            
    refresh_token = create_access_token(
        user_data=user_data,
        refresh=True,
        expire=timedelta(seconds=REFRESH_TOKEN_EXPIRY_SECONDS)
    )

    return JSONResponse(
                content={
                    "message": "Login successful.",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": user_data
                }
            )


@auth_router.get('/logout')
async def revoke_token(token_detais: dict=Depends(AccessTokenBearer())):
    jti = token_detais['jti']
    await add_jti_to_blocklist(jti)
    
    return JSONResponse(
        content={
            "message":"Logged out Successfully"
        },
        status_code=status.HTTP_200_OK
    )
    