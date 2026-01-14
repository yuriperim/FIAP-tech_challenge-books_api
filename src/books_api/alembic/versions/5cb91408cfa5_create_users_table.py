"""create users table

Revision ID: 5cb91408cfa5
Revises: 58caed9c6fde
Create Date: 2026-01-10 16:21:30.387163

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from src.books_api.configs.user_config import admin_user
from src.books_api.services.encryption import hash_password


# revision identifiers, used by Alembic.
revision: str = "5cb91408cfa5"
down_revision: Union[str, Sequence[str], None] = "58caed9c6fde"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    users_table = op.create_table(
        "users",
        sa.Column("user_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(25), unique=True, nullable=False),
        sa.Column("hashed_password", sa.CHAR(60), unique=False, nullable=False),
    )

    # em produção, variáveis homônimas do SO têm precedência
    username = admin_user.username
    password = admin_user.password

    hashed_password = hash_password(password)

    op.execute(
        users_table
        .insert()
        .values(username=username, hashed_password=hashed_password)
    )


def downgrade() -> None:
    """Downgrade schema."""
    raise RuntimeError("Migração irreversível")
