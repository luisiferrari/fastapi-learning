from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException, status
import jwt
import uuid
import logging

from src.config import Config

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRY_SECONDS = 3600*24  # 24 hours

def generate_hashed_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)

def create_access_token(user_data: dict, expire: timedelta = None, refresh: bool = False) -> str:
    
    now = datetime.now(timezone.utc)

    payload = {}
    payload['user'] = user_data
    payload['exp'] = now + expire if expire is not None else now + timedelta(seconds=ACCESS_TOKEN_EXPIRY_SECONDS) # Default expiry time of 60 minutes
    payload['jti'] = str(uuid.uuid4()) #needs to be string for jwt encoding
    payload['refresh'] = refresh
    
    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM,
    )
    
    return token

def decode_token(token: str) -> dict:
    
    ## Added robust JWT decoding and validation logic to the authentication utilities, including explicit handling for expired tokens and invalid token formats. Improved error handling by sanitizing Bearer tokens, validating JWT structure before decoding, and returning proper HTTP errors for expired or malformed tokens, ensuring a more reliable and predictable authentication flow across protected routes
    
    
    try:
        if not token:
            raise ValueError("Token vazio")

        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")

        if token.count(".") != 2:
            raise ValueError("Formato de token inválido")

        return jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM],
        )
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None