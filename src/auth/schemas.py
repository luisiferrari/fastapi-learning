from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class UserCreateModel(BaseModel):
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
    role: str
    
class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    first_name: str | None = None
    last_name: str | None = None
    email: str
    password_hash: str = Field(exclude=True)
    create_at: datetime
    update_at: datetime
    
class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
