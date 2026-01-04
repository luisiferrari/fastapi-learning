from sqlmodel import SQLModel, Field, Column, DateTime
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime, timezone
from typing import Optional



class User(SQLModel, table=True):
    __tablename__ = "users"
    
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username: str
    email: str
    first_name: Optional[str] = Field(default=None, nullable=True)
    last_name: Optional[str] = Field(default=None, nullable=True)
    role: str = Field(
        sa_column=Column(
            pg.VARCHAR,
            nullable=False,
            server_default='user'
        )
    )
    is_verified: Optional[bool] = Field(default=None, nullable=True)
    create_at: datetime = Field(
            sa_column=Column(
                DateTime(timezone=True),
                nullable=False,
                default=lambda: datetime.now(timezone.utc)
            )
        )
    update_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc)
        )
    )
    password_hash: str = Field(exclude=True)  # Exclude password from default representations. Example: when converting to dict or JSON, it won't include the password field.
    
    # The below method is used to represent the object as a string for easier debugging and logging. Exemple: When you print a User object, it will show the username.
    def __repr__(self):
        return f'<User {self.username}>'