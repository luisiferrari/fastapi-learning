from sys import version
from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"Server is starting...")
    await init_db()
    yield
    print(f"Server has been stoped.")

version = "v1"

app = FastAPI(
    title="Book Management API",
    description="An API to manage a collection of books.",
    version=version,
    lifespan=life_span
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])



# @app.get("/")
# async def read_root(name: str = "World"):
#     '''Simple endpoint that returns a greeting message.
#     Parameters:
#         name (str): The name to greet.
#     '''
#     return {"Hello": "World"}

# @app.get("/greet")
# async def greet_name(name: Optional[str] = "User", age: int = 0):
    
#     return {"message": f"hello {name}", "age": age}

# class BookCreateModel(BaseModel):
#     title: str
#     author: str

# @app.post('/create_book')
# async def create_book(book_data: BookCreateModel):
#     return {
#         "title": book_data.title,
#         "author": book_data.author
#     }
    
# @app.get("/get_headers", status_code=200)
# async def get_headers(
#     accept:str = Header(None),
#     content_type: str = Header(None),
#     user_agent:str = Header(None),
#     host: str = Header(None)
# ):
#     request_headers = {}
#     request_headers["Accept"] = accept
#     request_headers["Content-Type"] = content_type
#     request_headers["User-Agent"] = user_agent
#     request_headers["Host"] = host
#     return request_headers