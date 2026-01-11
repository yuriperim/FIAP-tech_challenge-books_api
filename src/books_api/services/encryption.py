import bcrypt


def hash_password(password: str) -> str:
    password_bytes = password.encode(encoding="utf-8")
    hashed_password_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12))

    return hashed_password_bytes.decode(encoding="utf-8")


def check_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode(encoding="utf-8")
    hashed_password_bytes = hashed_password.encode(encoding="utf-8")

    return bcrypt.checkpw(password_bytes, hashed_password_bytes)
