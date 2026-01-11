from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from src.books_api.configs.db_config import db
from src.books_api.models.persistent_storage.interfaces.db_connection_handler_interface import IDBConnectionHandler


DATABASE_URL = f"postgresql+psycopg://{db.user}:{db.password}@{db.host}:{db.port}/{db.name}"


class DBConnectionHandler(IDBConnectionHandler):
    def __init__(self) -> None:
        self.__connection_string = DATABASE_URL
        self.__engine = None
        self.session = None

    def __enter__(self) -> "DBConnectionHandler":
        self.connect()

        session_maker = sessionmaker()
        self.session = session_maker(bind=self.__engine)

        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.session.close()
        self.disconnect()

    def connect(self) -> None:
        if self.__engine is None:
            self.__engine = create_engine(self.__connection_string)

    def disconnect(self) -> None:
        if self.__engine is not None:
            self.__engine.dispose()
            self.__engine = None
            self.session = None

    def is_connected(self) -> bool:
        with self as db:
            try:
                _ = db.session.execute(select(1))
            except OperationalError:
                is_connected = False
            except Exception:
                raise
            else:
                is_connected = True

            return is_connected
