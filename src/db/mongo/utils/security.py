import bcrypt


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def is_password_correct(password_orig: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password_orig.encode(), password_hash.encode())
