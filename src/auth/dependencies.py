from fastapi import Request, status
from fastapi.security import HTTPBearer
from fastapi.exceptions import HTTPException

from .utils import decode_token

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request):
        creds = await super().__call__(request)
        
        token = creds.credentials
        
        token_data = decode_token(token)
        
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
        

