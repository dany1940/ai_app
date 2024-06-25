from os import getenv

from sqlalchemy.orm import Session


def create_override(engine):
    def override_get_db():
        with Session(bind=engine) as database:
            yield database

    return override_get_db


def postgres_dsn() -> str:
    postgres_password = getenv("POSTGRES_PASSWORD")
    return f"postgresql://postgres:{postgres_password}@localhost:5432/postgres"


""""""
