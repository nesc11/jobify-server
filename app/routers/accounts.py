from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import User
from app.schemas import Token, UserCreate
from app.dependencies import get_session
from app.security import get_password_hash, authenticate_user, create_access_token
from app.config import settings


router = APIRouter(prefix="/accounts", tags=["accounts"])

ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


@router.post("/register")
def register(*, session: Session = Depends(get_session), user: UserCreate):
    statement = select(User).where(User.username == user.username)
    results = session.scalars(statement)
    db_user = results.first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {"message": "User created successfully"}


@router.post("/login")
def login(
    *,
    session: Session = Depends(get_session),
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    db_user = authenticate_user(
        session=session, username=form_data.username, password=form_data.password
    )
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
