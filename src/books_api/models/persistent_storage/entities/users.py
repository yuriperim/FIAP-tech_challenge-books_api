from sqlalchemy import Column, Integer, String, CHAR

from src.books_api.models.persistent_storage.entities import Base  # Base definido em __init__.py


class UsersTable(Base):
    __tablename__ = "users"

    user_id = Column("user_id", Integer, primary_key=True, autoincrement=True)
    username = Column("username", String(25), unique=True, nullable=False)
    hashed_password = Column("hashed_password", CHAR(60), unique=False, nullable=False)

    def __repr__(self) -> str:
        return f"User(user_id={self.user_id}, username={self.username})"
