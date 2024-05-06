from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import Base
from app.database import engine
from app.config import settings
from app.routers import users, jobs, accounts

# No need this since we have implemented alembic as a database migration tool
Base.metadata.create_all(bind=engine)

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
