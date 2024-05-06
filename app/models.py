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
    type: Mapped[Literal["full-time", "part-time", "internship"]]
    status: Mapped[Literal["pending", "interview", "declined"]]
    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="jobs")

    def __repr__(self) -> str:
        return f"<Job(id={self.id}, username={self.position})>"


# # USERS
# class UserBase(SQLModel):
#     username: str = Field(index=True, unique=True)


# class User(UserBase, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     is_active: bool = Field(default=True)
#     hashed_password: str

#     jobs: list["Job"] = Relationship(back_populates="user")


# class UserCreate(UserBase):
#     password: str


# class UserPublic(UserBase):
#     id: int
#     is_active: bool


# class UserUpdate(SQLModel):
#     username: str | None = None
#     password: str | None = None


# # JOBS
# class JobBase(SQLModel):
#     position: str = Field(index=True)
#     company: str
#     job_type: Literal["full-time", "part-time", "internship"] = Field(
#         default="full-time"
#     )
#     job_status: Literal["pending", "interview", "declined"] = Field(default="pending")


# class Job(JobBase, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     user_id: int = Field(foreign_key="user.id")

#     user: User = Relationship(back_populates="jobs")


# class JobCreate(JobBase):
#     pass


# class JobPublic(JobBase):
#     id: int


# class JobUpdate(SQLModel):
#     position: str | None = None
#     comapny: str | None = None
