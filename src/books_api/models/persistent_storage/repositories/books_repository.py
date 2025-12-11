from sqlalchemy.orm.exc import NoResultFound

from src.books_api.models.persistent_storage.interfaces.db_connection_handler_interface import IDBConnectionHandler
from src.books_api.models.persistent_storage.interfaces.books_repository_interface import IBooksRepository
from src.books_api.models.persistent_storage.entities.books import BooksTable


class BooksRepository(IBooksRepository):
    def __init__(self, db_connection: IDBConnectionHandler) -> None:
        self.__db_connection = db_connection

    def get_connection(self) -> IDBConnectionHandler:
        return self.__db_connection

    def insert_book(
        self,
        book_id: int,
        titulo: str,
        preco: float,
        rating: int,
        disponibilidade: int,
        categoria: str,
        url_imagem: str
    ) -> None:
        book = BooksTable(
            book_id=book_id,
            titulo=titulo,
            preco=preco,
            rating=rating,
            disponibilidade=disponibilidade,
            categoria=categoria,
            url_imagem=url_imagem,
        )

        with self.__db_connection as db:
            try:
                db.session.add(book)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

    def insert_books(self, books_raw: list[dict]) -> None:
        books = [
            BooksTable(
                book_id=book["book_id"],
                titulo=book["titulo"],
                preco=book["preco"],
                rating=book["rating"],
                disponibilidade=book["disponibilidade"],
                categoria=book["categoria"],
                url_imagem=book["url_imagem"],
            ) for book in books_raw
        ]

        with self.__db_connection as db:
            try:
                db.session.add_all(books)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

    def select_book(self, book_id: int) -> BooksTable | None:
        with self.__db_connection as db:
            try:
                book = db.session.query(BooksTable).filter(BooksTable.book_id == book_id).one()
            except NoResultFound:
                book = None

            return book

    def select_books(self) -> list[BooksTable]:
        with self.__db_connection as db:
            try:
                books = db.session.query(BooksTable).all()
            except NoResultFound:
                books = []

            return books
