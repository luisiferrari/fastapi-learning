from pydantic import BaseModel
import uuid
from datetime import datetime, date

class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    publush_date: date
    page_count: int
    language: str
    create_at: datetime
    update_at: datetime
    
class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    publush_date: date
    page_count: int
    language: str
    
class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str