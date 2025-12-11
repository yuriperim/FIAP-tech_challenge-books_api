from pathlib import Path
from alembic.config import Config
from alembic import command


BASE_DIR = Path(__file__).resolve().parents[3]


def alembic_upgrade():
    ini_path = str(BASE_DIR.joinpath("alembic.ini"))
    cfg = Config(ini_path)
    command.upgrade(cfg, "head")
