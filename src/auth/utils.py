from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
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
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM],
        )
        return token_data
    
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None