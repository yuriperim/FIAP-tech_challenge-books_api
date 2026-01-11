import os
from typing import NamedTuple


class UserConfig(NamedTuple):
    username: str
    password: str


# em produção, variáveis homônimas do SO têm precedência
admin_user = UserConfig(
    username=os.getenv("ADMIN_USER"),
    password=os.getenv("ADMIN_PASSWORD"),
)
