from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from sqlalchemy import select
from jose import jwt
import bcrypt

from app.models import User
from app.config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm


def get_password_hash(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        password=plain_password.encode("utf-8"),
        hashed_password=hashed_password.encode("utf-8"),
    )


def authenticate_user(session: Session, username: str, password: str):
    statement = select(User).where(User.username == username)
    results = session.scalars(statement)
    db_user = results.first()
    if db_user is None:
        return False
    if not verify_password(password, db_user.hashed_password):
        return False
    return db_user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
