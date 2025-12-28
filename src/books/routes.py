from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import uuid


from src.books.service import BookService
from src.books.schemas import Book, BookUpdateModel, BookCreateModel
from src.db.main import get_session # The get_session contains the logic to create and manage database sessions.

book_router = APIRouter()

# The service layer is imported to separate business logic from route handling. The BookService class contains methods for CRUD operations on Book records.
book_service = BookService()

@book_router.get("/", response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    # The depends function is used to inject the database session into the route handler.
    books = await book_service.get_all_books(session)
    return books

@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookCreateModel) # The response_model=BookCreateModel makes so the response is validated against the Book schema.
async def create_book(book: BookCreateModel, session: AsyncSession = Depends(get_session)):
    new_book = await book_service.create_book(session=session, book_data=book)
    return new_book

@book_router.get("/{book_id}", response_model=Book)
async def get_book_by_id(book_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    book = await book_service.get_book(book_uid=book_id, session=session)
    
    if book:
        return book
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.patch("/{book_id}", response_model=Book)
async def update_book(book_id: str, book_update: BookUpdateModel, session: AsyncSession = Depends(get_session)):

    update_book = await book_service.update_book(book_uid=book_id, update_data=book_update, session=session)
    
    if update_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    else:
        return update_book

@book_router.delete("/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: str, session: AsyncSession = Depends(get_session)):
    deleted_book = await book_service.delete_book(book_uid=book_id, session=session)
    
    if deleted_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    else:
        return dict(message=f"Book with id {book_id} has been deleted.")