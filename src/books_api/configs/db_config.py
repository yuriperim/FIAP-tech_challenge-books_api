import os
from typing import NamedTuple


class DBConfig(NamedTuple):
    host: str
    port: str
    name: str
    user: str
    password: str


# em produção, variáveis homônimas do SO têm precedência
db = DBConfig(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    name=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
)
