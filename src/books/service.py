from sqlalchemy.ext.asyncio import AsyncSession
from src.books.schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc
from .models import Book
import uuid

# """
# This file contains the service layer for the Book entity. It handles the business logic and interacts with the database layer to perform CRUD operations on Book records.

# The Session (from SQLModel) object is used to manage database transactions asynchronously.
# """

class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.create_at))
        
        result = await session.execute(statement=statement)
        
        return result.scalars().all()
    
    async def get_book(self, book_uid: uuid.UUID, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        
        result = await session.execute(statement=statement)
        
        return result.scalars().first()
    
    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        
        new_book = Book(
            **book_data_dict
        )
        # '''
        # The ** syntax is used to unpack the dictionary and pass its key-value pairs as keyword arguments to the Book constructor. The named arguments correspond to the fields defined in the Book model.
        # '''
        
        session.add(new_book)
        
        await session.commit()
        await session.refresh(new_book)  
        
        return new_book
          
    async def update_book(self,update_data: BookUpdateModel,  book_uid: str, session: AsyncSession):
       
       book_to_update = await self.get_book(book_uid=book_uid, session=session)
       
    #    '''
    #    The self.get_book method is because it is an instance method of the BookService class.
    #    '''
       
       if book_to_update is not None:
            update_data_dict = update_data.model_dump()

            for k,v in update_data_dict.items():
                setattr(book_to_update, k, v)

            await session.commit()

            return book_to_update
        
       else:
            return None
       
    
    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid=book_uid, session=session)

        if book_to_delete is not None:
            await session.delete(book_to_delete)
            
            await session.commit()
            
        else:
            return None