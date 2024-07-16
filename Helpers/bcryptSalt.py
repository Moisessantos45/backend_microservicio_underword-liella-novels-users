import bcrypt


def encryptar(password: str) -> str:
    salt = bcrypt.gensalt(10)
    hassPassword = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hassPassword.decode("utf-8")


def comparePassword(password: str, hassPassword: str) -> bool:
    password_bytes = password.encode("utf-8")
    hashed_password_bytes = hassPassword.encode("utf-8")
    # Verificar la contraseña
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)
