from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

from src.books_api.models.persistent_storage.interfaces.db_connection_handler_interface import IDBConnectionHandler
from src.books_api.models.persistent_storage.interfaces.books_repository_interface import IBooksRepository
from src.books_api.models.persistent_storage.entities.books import BooksTable


class BooksRepository(IBooksRepository):
    def __init__(self, db_connection: IDBConnectionHandler) -> None:
        self.__db_connection = db_connection

    def get_db_connection(self) -> IDBConnectionHandler:
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
        books = [BooksTable(
            book_id=book["book_id"],
            titulo=book["titulo"],
            preco=book["preco"],
            rating=book["rating"],
            disponibilidade=book["disponibilidade"],
            categoria=book["categoria"],
            url_imagem=book["url_imagem"],
        ) for book in books_raw]

        with self.__db_connection as db:
            try:
                db.session.add_all(books)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

    def select_book_by_id(self, book_id: int) -> BooksTable | None:
        with self.__db_connection as db:
            try:
                book = db.session.query(BooksTable).filter(BooksTable.book_id == book_id).one()
            except NoResultFound:
                book = None

            return book

    def select_books_by_title_or_category(self, titulo: str | None, categoria: str | None) -> list[BooksTable]:
        conditions = []
        if titulo is not None:
            conditions.append(BooksTable.titulo.ilike(f"%{titulo}%"))
        if categoria is not None:
            conditions.append(BooksTable.categoria == categoria)

        with self.__db_connection as db:
            try:
                books = db.session.query(BooksTable).filter(*conditions).all()
            except NoResultFound:
                books = []

            return books

    def select_books_by_rating(self, rating: int) -> list[BooksTable]:
        condition = BooksTable.rating == rating

        with self.__db_connection as db:
            try:
                books = db.session.query(BooksTable).filter(condition).all()
            except NoResultFound:
                books = []

            return books

    def select_books_by_price_range(self, min_price: float, max_price: float) -> list[BooksTable]:
        condition = BooksTable.preco.between(min_price, max_price)

        with self.__db_connection as db:
            try:
                books = db.session.query(BooksTable).filter(condition).all()
            except NoResultFound:
                books = []

            return books

    def select_books(self) -> list[BooksTable]:
        with self.__db_connection as db:
            try:
                books = db.session.query(BooksTable).all()
            except NoResultFound:
                books = []

            return books

    def select_categories(self) -> list[str]:
        with self.__db_connection as db:
            try:
                categories_tuples = db.session.query(BooksTable.categoria).distinct().all()
            except NoResultFound:
                categories_tuples = []

            return [category_tuple[0] for category_tuple in categories_tuples]

    def aggregate_by_column(self, column_name: str) -> list[dict]:
        column = getattr(BooksTable, column_name)

        with self.__db_connection as db:
            try:
                aggregation_tuples = (
                    db.session
                    .query(
                        column,
                        func.count(BooksTable.book_id),
                        func.sum(BooksTable.preco),
                    )
                    .group_by(column)
                    .all()
                )
            except NoResultFound:
                aggregation_tuples = []

            return [{
                "valor": aggregation_tuple[0],
                "quantidade": aggregation_tuple[1],
                "soma_preco": aggregation_tuple[2],
            } for aggregation_tuple in aggregation_tuples]
