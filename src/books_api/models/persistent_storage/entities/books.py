from sqlalchemy import Column, Integer, Numeric, String

from src.books_api.models.persistent_storage.entities import Base  # Base definido em __init__.py


class BooksTable(Base):
    __tablename__ = "books"

    book_id = Column("book_id", Integer, primary_key=True)
    titulo = Column("titulo", String(250), nullable=False)
    preco = Column("preco", Numeric(10, 2), nullable=False)
    rating = Column("rating", Integer, nullable=False)
    disponibilidade = Column("disponibilidade", Integer, nullable=False)
    categoria = Column("categoria", String(25), nullable=False)
    url_imagem = Column("url_imagem", String(100), nullable=False)

    def __repr__(self) -> str:
        return f"Book(book_id={self.book_id}, titulo={self.titulo}, categoria={self.categoria})"

    def to_dict(self) -> dict:
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
