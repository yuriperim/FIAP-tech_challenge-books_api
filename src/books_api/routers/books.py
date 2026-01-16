from decimal import Decimal
from typing import Annotated
from fastapi import APIRouter, Depends, Query

from src.books_api.models.persistent_storage.interfaces.books_repository_interface import IBooksRepository
from src.books_api.routers.dependencies import get_books_repo, get_user


router = APIRouter(
    prefix="/api/v1",
    tags=["Books"]
)


@router.get("/books", response_model=list[dict])
async def get_books(books_repo: IBooksRepository = Depends(get_books_repo)) -> list[dict]:
    books = books_repo.select_books()

    return [book.to_dict() for book in books]


@router.delete("/books", response_model=dict)
async def delete_books(
    username: str = Depends(get_user),
    books_repo: IBooksRepository = Depends(get_books_repo)
) -> dict:
    books_repo.delete_books()

    return {
        "message": "Registros excluídos da tabela de livros",
        "requester": username,
    }


@router.get("/books/top-rated", response_model=list[dict])
async def get_top_rated_books(books_repo: IBooksRepository = Depends(get_books_repo)) -> list[dict]:
    books = books_repo.select_books_by_rating(rating=5)

    return [book.to_dict() for book in books]


@router.get("/books/search", response_model=list[dict])
async def get_books_by_title_or_category(
    title: Annotated[str | None, Query(max_length=250)] = None,
    category: Annotated[str | None, Query(max_length=25)] = None,
    books_repo: IBooksRepository = Depends(get_books_repo)
) -> list[dict]:
    books = books_repo.select_books_by_title_or_category(title, category)

    return [book.to_dict() for book in books]


@router.get("/books/price-range", response_model=list[dict])
async def get_books_by_price_range(
    min_price: Annotated[float, Query(alias="min")],
    max_price: Annotated[float, Query(alias="max")],
    books_repo: IBooksRepository = Depends(get_books_repo)
) -> list[dict]:
    books = books_repo.select_books_by_price_range(min_price, max_price)

    return [book.to_dict() for book in books]


@router.get("/books/{book_id}", response_model=dict)
async def get_book_by_id(book_id: int, books_repo: IBooksRepository = Depends(get_books_repo)) -> dict:
    book = books_repo.select_book_by_id(book_id)

    return book.to_dict() if book is not None else {}


@router.get("/categories", response_model=dict)
async def get_categories(books_repo: IBooksRepository = Depends(get_books_repo)) -> dict:
    categories = books_repo.select_categories()

    return {"categorias": sorted(categories)}


@router.get("/stats/overview", response_model=dict)
async def get_stats_overview(books_repo: IBooksRepository = Depends(get_books_repo)) -> dict:
    distribuicao_ratings = books_repo.aggregate_by_column("rating")

    total_livros = 0
    soma_preco_livros = Decimal("0.00")
    for rating_info in distribuicao_ratings:
        rating_info["rating"] = rating_info.pop("valor")  # renomeia
        rating_info["quantidade"] = rating_info.pop("quantidade")  # ordena

        total_livros += rating_info["quantidade"]
        soma_preco_livros += rating_info["soma_preco"]

        del rating_info["soma_preco"]

    return {
        "total_livros": total_livros,
        "media_preco": round(soma_preco_livros / total_livros, 2) if total_livros > 0 else Decimal("0.00"),
        "distribuicao_ratings": sorted(distribuicao_ratings, key=lambda x: x["rating"]),
    }


@router.get("/stats/categories", response_model=list[dict])
async def get_categories_stats(books_repo: IBooksRepository = Depends(get_books_repo)) -> list[dict]:
    distribuicao_categorias = books_repo.aggregate_by_column("categoria")

    for categoria_info in distribuicao_categorias:
        categoria_info["categoria"] = categoria_info.pop("valor")  # renomeia
        categoria_info["quantidade"] = categoria_info.pop("quantidade")  # ordena
        if categoria_info["quantidade"] > 0:
            categoria_info["media_preco"] = round(categoria_info["soma_preco"] / categoria_info["quantidade"], 2)
        else:
            categoria_info["media_preco"] = Decimal("0.00")

        del categoria_info["soma_preco"]

    return sorted(distribuicao_categorias, key=lambda x: x["categoria"])
