from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.database import SessionLocal
from app.security import SECRET_KEY, ALGORITHM
from app.schemas import TokenData, UserPublic
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="accounts/login")


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    statement = select(User).where(User.username == token_data.username)
    results = session.scalars(statement)
    db_user = results.first()
    if db_user is None:
        raise credentials_exception
    return db_user


def get_current_active_user(
    current_user: Annotated[UserPublic, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="inactive user"
        )
    return current_user


def authenticate_admin_user(
    current_user: Annotated[UserPublic, Depends(get_current_active_user)]
):
    if current_user.username != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
