from sqlalchemy.orm.exc import NoResultFound

from src.books_api.models.persistent_storage.interfaces.db_connection_handler_interface import IDBConnectionHandler
from src.books_api.models.persistent_storage.interfaces.users_repository_interface import IUsersRepository
from src.books_api.models.persistent_storage.entities.users import UsersTable


class UsersRepository(IUsersRepository):
    def __init__(self, db_connection: IDBConnectionHandler) -> None:
        self.__db_connection = db_connection

    def get_db_connection(self) -> IDBConnectionHandler:
        return self.__db_connection

    def insert_user(self, username: str, hashed_password: str) -> None:
        user = UsersTable(
            username=username,
            hashed_password=hashed_password,
        )

        with self.__db_connection as db:
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

    def select_user_by_username(self, username: str) -> UsersTable | None:
        with self.__db_connection as db:
            try:
                user = db.session.query(UsersTable).filter(UsersTable.username == username).one()
            except NoResultFound:
                user = None

            return user
