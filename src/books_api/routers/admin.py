from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.books_api.models.persistent_storage.interfaces.users_repository_interface import IUsersRepository
from src.books_api.models.persistent_storage.interfaces.books_repository_interface import IBooksRepository
from src.books_api.routers.dependencies import get_users_repo, get_books_repo, get_user
from src.books_api.services.encryption import check_password
from src.books_api.services.tokenization import create_access_token
from src.books_api.services.migrations import alembic_upgrade, alembic_downgrade
from src.books_api.services.books_etl import run_etl


router = APIRouter(
    prefix="/api/v1",
    tags=["Admin"]
)


@router.post("/auth/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    users_repo: IUsersRepository = Depends(get_users_repo)
) -> dict:
    user = users_repo.select_user_by_username(form_data.username)
    if (user is None) or (not check_password(form_data.password, user.hashed_password)):
        raise HTTPException(status_code=400, detail="Nome de usuário ou senha incorretos")

    payload = {
        "sub": user.username,
    }

    return {
        "access_token": create_access_token(payload),
        "token_type": "bearer",
    }


@router.post("/migrations/up")
async def run_migrations_up(username: str = Depends(get_user)) -> dict:
    alembic_upgrade()

    return {
        "message": "Atualização BD concluída",
        "requester": username,
    }


@router.post("/migrations/down")
async def run_migrations_down(username: str = Depends(get_user)) -> dict:
    try:
        alembic_downgrade()
    except RuntimeError:
        message = "Regressão BD interrompida"
    else:
        message = "Regressão BD concluída"

    return {
        "message": message,
        "requester": username,
    }


@router.post("/scraping/trigger")
async def run_books_etl(
    background_tasks: BackgroundTasks,
    username: str = Depends(get_user),
    books_repo: IBooksRepository = Depends(get_books_repo)
) -> dict:
    background_tasks.add_task(run_etl, books_repo)

    return {
        "message": "Scraping iniciado",
        "requester": username,
    }


@router.get("/health")
async def run_health_check(users_repo: IUsersRepository = Depends(get_users_repo)) -> dict:
    conn = users_repo.get_db_connection()
    if conn.is_connected():
        message = "Conexão com BD estabelecida"
    else:
        message = "Conexão com BD não estabelecida"

    return {"message": message}
