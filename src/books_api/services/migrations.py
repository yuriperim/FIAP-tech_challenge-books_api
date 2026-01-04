from pathlib import Path
from alembic.config import Config
from alembic import command


BASE_DIR = Path(__file__).resolve().parents[3]
INI_PATH = str(BASE_DIR.joinpath("alembic.ini"))


def alembic_upgrade() -> None:
    cfg = Config(INI_PATH)
    command.upgrade(cfg, "head")


def alembic_downgrade() -> None:
    cfg = Config(INI_PATH)
    command.downgrade(cfg, "base")
