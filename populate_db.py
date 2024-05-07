import csv

from sqlalchemy import delete, insert

from app.models import User, Job
from app.database import SessionLocal
from app.security import get_password_hash


def main():
    with open("MOCK_DATA.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        jobs_data = [row for row in reader]

    with SessionLocal() as session:
        session.execute(delete(User))
        session.execute(delete(Job))

        demo_user = User(
            id=1,
            username="demo_username",
            hashed_password=get_password_hash("demo_password"),
        )
        session.add(demo_user)
        session.commit()

        session.execute(insert(Job), jobs_data)
        session.commit()


if __name__ == "__main__":
    main()
