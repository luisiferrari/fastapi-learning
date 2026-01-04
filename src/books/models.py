from sqlmodel import SQLModel, Field, Column, DateTime
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date, timezone
import uuid
from typing import Optional


# '''
# This file defines the model from SQLModel that represents the "books" table in the database. It "talks" to the database layer and maps the data to Python objects.
# '''


class Book(SQLModel, table=True):
    __tablename__ = "books"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    title: str
    author: str
    publisher: str
    publush_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key='users.uid')
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
    
    
def __repr__(self):
    return f'<Book {self.title}>'