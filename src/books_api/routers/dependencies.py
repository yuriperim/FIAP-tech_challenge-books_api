from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from src.books_api.models.persistent_storage.settings.db_connection_handler import DBConnectionHandler
from src.books_api.models.persistent_storage.repositories.users_repository import UsersRepository
from src.books_api.models.persistent_storage.repositories.books_repository import BooksRepository
from src.books_api.services.tokenization import decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_users_repo() -> UsersRepository:
    db_connection = DBConnectionHandler()

    return UsersRepository(db_connection)


def get_books_repo() -> BooksRepository:
    db_connection = DBConnectionHandler()

    return BooksRepository(db_connection)


def get_user(
    token: str = Depends(oauth2_scheme),
    users_repo: UsersRepository = Depends(get_users_repo)
) -> str:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Credenciais inválidas",
        headers={
            "WWW-Authenticate": "Bearer",
        }
    )

    try:
        payload = decode_token(token)
    except InvalidTokenError:
        raise credentials_exception
    else:
        username = payload.get("sub")
        if username is None:
            raise credentials_exception

        user = users_repo.select_user_by_username(username)
        if user is None:
            raise credentials_exception

    return username
