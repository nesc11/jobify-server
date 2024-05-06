import csv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import insert, delete

from app.models import Base, User, Job
from app.database import engine, SessionLocal
from app.config import settings
from app.routers import users, jobs, accounts

# No need this since we have implemented alembic as a database migration tool
Base.metadata.create_all(bind=engine)

with open("MOCK_DATA.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    jobs_data = [row for row in reader]

with SessionLocal() as session:
    session.execute(delete(User))
    session.execute(delete(Job))

    session.execute(
        insert(User), [{"username": "demo_user", "hashed_password": "test_password"}]
    )
    session.execute(insert(Job), jobs_data)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(accounts.router)
app.include_router(users.router)
app.include_router(jobs.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Application"}
