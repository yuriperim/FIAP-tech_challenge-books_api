import os
from datetime import datetime, timedelta, timezone
import jwt


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_TIME_SECONDS = 5 * 60


def create_access_token(payload_in: dict) -> str:
    exp = datetime.now(tz=timezone.utc) + timedelta(seconds=ACCESS_TOKEN_EXPIRATION_TIME_SECONDS)
    payload_out = {
        **payload_in,
        "exp": exp,
    }

    return jwt.encode(payload=payload_out, key=SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
