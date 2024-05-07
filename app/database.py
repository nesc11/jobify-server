from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"
# SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://jobify_server_user:fGEerwQc7tTTvCWXuT22tq3hVd2eqzqF@dpg-cosfdr21hbls73fk0d80-a.oregon-postgres.render.com/jobify_server"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
