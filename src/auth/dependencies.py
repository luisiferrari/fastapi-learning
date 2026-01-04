from fastapi import Request, status, Depends
from fastapi.security import HTTPBearer
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .service import UserService
from .utils import decode_token
from .model import User
from src.db.redis import token_in_blocklist
from src.db.main import get_session

user_service = UserService()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request):
        creds = await super().__call__(request)
        
        token = creds.credentials
        
        token_data = decode_token(token)
        
        if token_data is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")
        
        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail={
                    "error":"This token is invalid or been revoked",
                    "resolution":"Plase get a new Token."
                    }
                )
        
        self.verify_token_data(token_data)
        
        # if token_data is None:
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")
        
        # if token_data.get("refresh"):
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide an access token, not a refresh token")
        
        return token_data
    
    def verify_token_data(self, token_data: dict):
        '''Override in subclasses to add custom verification logic.'''
        raise NotImplementedError("Subclasses must implement this method.")
    
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict):
        '''Verify that the token is an access token.'''
        if token_data and token_data.get("refresh"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide an access token, not a refresh token")
        

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict):
        '''Verify that the token is a refresh token.'''
        if token_data and not token_data.get("refresh"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide a refresh token, not an access token")
        
async def get_current_user(token_details: dict=Depends(AccessTokenBearer()), session: AsyncSession = Depends(get_session)):
    print(token_details)
    user_email= token_details['user']['email']
    print(user_email)
    user = await user_service.get_user_by_email(email=user_email, session=session)
    print(user)
    return user
    
class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles
        
    def __call__(self, current_user: User = Depends(get_current_user)):
        
        if current_user.role in self.allowed_roles:
            return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not aloowed to perform this action."
        )