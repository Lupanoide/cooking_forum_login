from passlib.context import CryptContext
from src.conf.config import Config
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

conf = Config()

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, conf.get_jwt_secret_key(), algorithm=conf.get_jwt_algorithm())
    return encoded_jwt