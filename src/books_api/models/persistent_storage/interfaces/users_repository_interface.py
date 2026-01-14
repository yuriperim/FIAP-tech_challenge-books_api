from abc import ABC, abstractmethod

from src.books_api.models.persistent_storage.interfaces.db_connection_handler_interface import IDBConnectionHandler
from src.books_api.models.persistent_storage.entities.users import UsersTable


class IUsersRepository(ABC):
    @abstractmethod
    def get_db_connection(self) -> IDBConnectionHandler:
        pass

    @abstractmethod
    def insert_user(self, username: str, hashed_password: str) -> None:
        pass

    @abstractmethod
    def select_user_by_username(self, username: str) -> UsersTable | None:
        pass
