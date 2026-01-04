from sys import version
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.books.routes import book_router
from src.auth.routers import auth_router
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
    version=version
    # lifespan=life_span # -> Removed because I'm using alembic for database migrations. I was only using .create_all() from Lifespan, so now its not necessary anymore
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])
