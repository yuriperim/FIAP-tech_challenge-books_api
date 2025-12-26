from abc import ABC, abstractmethod

from src.books_api.models.persistent_storage.interfaces.db_connection_handler_interface import IDBConnectionHandler
from src.books_api.models.persistent_storage.entities.books import BooksTable


class IBooksRepository(ABC):
    @abstractmethod
    def get_db_connection(self) -> IDBConnectionHandler:
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def insert_books(self, books_raw: list[dict]) -> None:
        pass

    @abstractmethod
    def select_book_by_id(self, book_id: int) -> BooksTable | None:
        pass

    @abstractmethod
    def select_books_by_title_or_category(self, titulo: str | None, categoria: str | None) -> list[BooksTable]:
        pass

    @abstractmethod
    def select_books_by_rating(self, rating: int) -> list[BooksTable]:
        pass

    @abstractmethod
    def select_books_by_price_range(self, min_price: float, max_price: float) -> list[BooksTable]:
        pass

    @abstractmethod
    def select_books(self) -> list[BooksTable]:
        pass

    @abstractmethod
    def select_categories(self) -> list[str]:
        pass

    @abstractmethod
    def aggregate_by_column(self, column_name: str) -> list[dict]:
        pass
