from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt
import uuid
import logging

from src.config import Config

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRY_SECONDS = 3600  # 60 minutes

def generate_hashed_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)

def create_access_token(user_data: dict, expire: timedelta = None, refresh: bool = False) -> str:
    '''
    Docstring for create_access_token
    
    :param user_data: Description
    :type user_data: dict
    :param expire: Description
    :type expire: timedelta
    :param refresh: Description
    :type refresh: bool
    :return: Description
    :rtype: str
    '''
    payload = {}
    payload['user'] = user_data
    payload['exp'] = datetime.now() + expire if expire is not None else datetime.now() + timedelta(seconds=ACCESS_TOKEN_EXPIRY_SECONDS) # Default expiry time of 60 minutes
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