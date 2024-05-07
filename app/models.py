from typing import List, Literal
from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

    jobs: Mapped[List["Job"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username})>"


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    position: Mapped[str] = mapped_column(index=True)
    company: Mapped[str] = mapped_column(index=True)
    location: Mapped[str] = mapped_column(index=True)
    job_type: Mapped[Literal["full-time", "part-time", "internship"]]
    job_status: Mapped[Literal["pending", "interview", "declined"]]
    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="jobs")

    def __repr__(self) -> str:
        return f"<Job(id={self.id}, username={self.position})>"
