from fastapi.testclient import TestClient
import pytest
from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from alembic.command import downgrade
from alembic.command import upgrade
from alembic.config import Config
from app.models import Clinician
from app.dependencies import get_db
from tests.conftest import postgres_dsn
from tests.conftest import create_override
from  app.main import app



resources = [
    Clinician(
    registration_id=1 ,
    first_name="ANA",
    last_name="CARENINA",
    ),
    Clinician(
    registration_id=2 ,
    first_name="ERNEST",
    last_name="HEMINGWAY",
    ),
    Clinician(
    registration_id=3 ,
    first_name="ANA",
    last_name="CARENINA",

    ),
    Clinician(
    registration_id=4 ,
    first_name="STEPHEN",
    last_name="KING",
    )
]

clinician_to_create = [
    {
  "registration_id": 5,
  "first_name": "MARK",
  "last_name": "TWAIN",
},
{
  "registration_id": 6,
  "first_name": " CHARLES",
  "last_name": "DICKENS",
},
{
  "registration_id": 7,
  "first_name": "JANE",
  "last_name": "AUSTIN",
},
]


class Clinican:
    """
    Class containing tests for the vehicle endpoints.
    """

    @pytest.fixture(scope="class")
    def alembic_engine(self):
        return create_engine(postgres_dsn())

    @pytest.fixture(scope="class", autouse=True)
    def apply_migrations(self):
        config = Config("alembic.ini")
        config.set_main_option("sqlalchemy.url", postgres_dsn())
        upgrade(config, "head")
        yield
        downgrade(config, "base")

    @pytest.fixture(scope="class")
    def database(self, alembic_engine):
        with Session(bind=alembic_engine) as database:
            yield database

    @pytest.fixture(scope="class", autouse=True)
    def create_class_defaults(self, database):
        for resource in resources:
            database.add(resource)
            database.flush()
        database.commit()

    @pytest.fixture
    def client(self, alembic_engine):
        test_client = TestClient(app)
        app.dependency_overrides[get_db] = create_override(alembic_engine)
        return test_client



    @pytest.mark.parametrize("/", clinician_to_create)
    def test_post_patient(self, clinician: dict[Any, Any], client: TestClient) -> None:
        """
        Test that a patient can be created provided a valid input
        data.
        """
        response = client.post(
            "/clinician/",
            json=clinician,
        )
        assert response.status_code == status.HTTP_201_CREATED
