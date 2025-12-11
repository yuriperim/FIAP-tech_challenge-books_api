from fastapi import APIRouter, Depends

from src.books_api.models.persistent_storage.settings.db_connection_handler import DBConnectionHandler
from src.books_api.models.persistent_storage.repositories.books_repository import BooksRepository


router = APIRouter(
    prefix="/api/v1",
    tags=["Books"]
)


def get_books_repo() -> BooksRepository:
    db_connection = DBConnectionHandler()

    return BooksRepository(db_connection)


@router.get("/books", response_model=list[dict])
async def get_books(books_repo: BooksRepository = Depends(get_books_repo)) -> list[dict]:
    books = books_repo.select_books()

    return [book.to_dict() for book in books]
