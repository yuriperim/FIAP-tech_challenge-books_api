from typing import Annotated
from fastapi import APIRouter, Depends, Query

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


@router.get("/books/search", response_model=list[dict])
async def get_books_by_title_or_category(
    title: Annotated[str | None, Query(max_length=250)] = None,
    category: Annotated[str | None, Query(max_length=25)] = None,
    books_repo: BooksRepository = Depends(get_books_repo)
) -> list[dict]:
    books = books_repo.select_books_by_title_or_category(title, category)

    return [book.to_dict() for book in books]


@router.get("/books/price-range", response_model=list[dict])
async def get_books_by_price_range(
    min_price: Annotated[float, Query(alias="min")],
    max_price: Annotated[float, Query(alias="max")],
    books_repo: BooksRepository = Depends(get_books_repo)
) -> list[dict]:
    books = books_repo.select_books_by_price_range(min_price, max_price)

    return [book.to_dict() for book in books]


@router.get("/books/{book_id}", response_model=dict)
async def get_book_by_id(book_id: int, books_repo: BooksRepository = Depends(get_books_repo)) -> dict:
    book = books_repo.select_book_by_id(book_id)

    return book.to_dict() if book is not None else {}


@router.get("/categories", response_model=dict)
async def get_categories(books_repo: BooksRepository = Depends(get_books_repo)) -> dict:
    categories = books_repo.select_categories()

    return {"categorias": categories}
