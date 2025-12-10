"""create books table

Revision ID: 58caed9c6fde
Revises:
Create Date: 2025-11-20 12:36:49.333008

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "58caed9c6fde"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "books",
        sa.Column("book_id", sa.Integer, primary_key=True),
        sa.Column("titulo", sa.String(250), nullable=False),
        sa.Column("preco", sa.Numeric(10, 2), nullable=False),
        sa.Column("rating", sa.Integer, nullable=False),
        sa.Column("disponibilidade", sa.Integer, nullable=False),
        sa.Column("categoria", sa.String(25), nullable=False),
        sa.Column("url_imagem", sa.String(100), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("books")
