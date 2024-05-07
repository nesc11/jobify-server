import math

from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import User
from app.schemas import UserCreate, UserPublic, UserList
from app.dependencies import get_session, check_admin_user
from app.security import get_password_hash


router = APIRouter(
    prefix="/users", tags=["users"], dependencies=[Depends(check_admin_user)]
)


@router.get("/", response_model=UserList)
def read_users(
    session: Session = Depends(get_session),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, le=10),
):
    users = session.scalars(
        select(User).offset((page - 1) * per_page).limit(per_page)
    ).all()
    total = len(users)
    return {
        "users": users,
        "page": page,
        "pages": math.ceil(total / per_page),
        "total": total,
    }


@router.post("/", response_model=UserPublic)
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    db_user = session.scalars(
        select(User).where(User.username == user.username)
    ).first()
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
    return db_user


@router.get("/{user_id}", response_model=UserPublic)
def read_user(*, session: Session = Depends(get_session), user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.delete("/{user_id}")
def delete_user(*, session: Session = Depends(get_session), user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    session.delete(user)
    session.commit()
    return {"ok": True}
