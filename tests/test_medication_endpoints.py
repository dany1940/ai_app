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
from app.models import Medication
from app.dependencies import get_db
from tests.conftest import postgres_dsn
from tests.conftest import create_override
from  app.main import app



resources = [
    Medication(
    medication_reference="ASBD",
    code_name="AA",
    international_code_name="BB",
    strength_value=3,
    strenght_unit=3,
    form="POWDER"),
    Medication(
    medication_reference="ASBDGDF",
    code_name="AAHHGS",
    international_code_name="BBJHSJ",
    strength_value=2,
    strenght_unit=3,
    form="TABLET"),
     Medication(
    medication_reference="ASBDPPPPP",
    code_name="AALLKJ",
    international_code_name="BBASD",
    strength_value=30,
    strenght_unit=3,
    form="SYRUP"),
    Medication(
    medication_reference="ASBDGHJKK",
    code_name="AAPOOU",
    international_code_name="BBLKJHH",
    strength_value=19,
    strenght_unit=2,
    form="CAPSULE"),
]

medication_to_create = [
 {
  "medication_reference": "77GSH",
  "code_name": "ddDJDK",
  "international_code_name": "KKDJHF",
  "strength_value": 2,
  "strenght_unit": 10,
  "form": "POWDER"
},
{
  "medication_reference": "SBHSJ77",
  "code_name": "ddLLKJ",
  "international_code_name": "KJJJJK",
  "strength_value": 10,
  "strenght_unit": 2,
  "form": "CAPSULE"
},
{
  "medication_reference": "778797",
  "code_name": "ddS",
  "international_code_name": "KKLLL",
  "strength_value": 6,
  "strenght_unit": 2,
  "form": "SYRUP"
},
{
  "medication_reference": "70097",
  "code_name": "dGHHd",
  "international_code_name": "KKLLL",
  "strength_value": 7,
  "strenght_unit": 2,
  "form": "TABLET"
}
]


class Medication:
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



    @pytest.mark.parametrize("/", medication_to_create)
    def test_post_medication(self, medication: dict[Any, Any], client: TestClient) -> None:
        """
        Test that a patient can be created provided a valid input
        data.
        """
        response = client.post(
            "/patient/",
            json=medication,
        )
        assert response.status_code == status.HTTP_201_CREATED
