from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from typing import List
from src.books.schemas import Book, BookUpdate
from src.books.book_data import books

book_router = APIRouter()

@book_router.get("/", response_model=List[Book])
async def get_all_books():
    return books

@book_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    new_book = book.model_dump()
    books.append(new_book)
    return new_book

@book_router.get("/{book_id}", response_model=Book)
async def get_book_by_id(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.patch("/{book_id}", response_model=Book)
async def update_book(book_id: int, book_update: BookUpdate):
    for book in books:
        if book["id"] == book_id:
            book['title'] = book_update.title
            book['author'] = book_update.author
            book['publisher'] = book_update.publisher
            book['page_count'] = book_update.page_count
            book['language'] = book_update.language
            
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.delete("/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return dict(message=f"Book with id {book_id} has been deleted.")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")