import jwt
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv("JWT_SECRET")
algorithm = os.getenv("ALGORITHM")

def generate_token(id, expiration_minutes=15):
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=expiration_minutes)
    token = jwt.encode({"id": id, "exp": expiration_time}, secret_key, algorithm=algorithm)
    return token
