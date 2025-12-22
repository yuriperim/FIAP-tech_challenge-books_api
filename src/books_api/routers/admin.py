from fastapi import APIRouter, Depends, BackgroundTasks

from src.books_api.models.persistent_storage.settings.db_connection_handler import DBConnectionHandler
from src.books_api.models.persistent_storage.repositories.books_repository import BooksRepository
from src.books_api.services.migrations import alembic_upgrade
from src.books_api.services.books_etl import run_etl


router = APIRouter(
    prefix="/api/v1",
    tags=["Admin"]
)


def get_books_repo() -> BooksRepository:
    db_connection = DBConnectionHandler()

    return BooksRepository(db_connection)


@router.post("/migrations")
async def run_migrations(background_tasks: BackgroundTasks) -> dict:
    background_tasks.add_task(alembic_upgrade)

    return {"message": "Atualização BD iniciada"}


# @router.post("/scraping/trigger")
async def run_books_etl(
    background_tasks: BackgroundTasks,
    books_repo: BooksRepository = Depends(get_books_repo)
) -> dict:
    background_tasks.add_task(run_etl, books_repo)

    return {"message": "Scraping iniciado"}


@router.get("/health")
async def run_health_check(books_repo: BooksRepository = Depends(get_books_repo)) -> dict:
    conn = books_repo.get_db_connection()
    if conn.is_connected():
        message = "Conexão com BD estabelecida."
    else:
        message = "Conexão com BD não estabelecida."

    return {"message": message}
