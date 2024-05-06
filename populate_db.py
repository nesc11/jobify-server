import csv

from sqlalchemy import delete, insert
from sqlalchemy.orm import sessionmaker

from app.models import User, Job
from app.database import SessionLocal


def main():

    with open("MOCK_DATA.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        jobs_data = [row for row in reader]

    with SessionLocal() as session:
        session.execute(delete(User))
        session.execute(delete(Job))

        session.execute(
            insert(User), [{"username": "demo_user", "hashed_password": "password"}]
        )
        session.execute(insert(Job), jobs_data)


if __name__ == "__main__":
    main()
