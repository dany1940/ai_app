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
from app.models import Patient, Clinician, Medication, MedicationRequest
from app.dependencies import get_db
from tests.conftest import postgres_dsn
from tests.conftest import create_override
from  app.main import app



resources = [
Patient(
    registration_id=1 ,
    first_name="ANA",
    last_name="CARENINA",
    date_of_birth="2014-06-21",
    gender="FEMALE"
    ),
    Patient(
    registration_id=2 ,
    first_name="ERNEST",
    last_name="HEMINGWAY",
    date_of_birth="2000-09-21",
    gender="MALE"
    ),
    Patient(
    registration_id=3 ,
    first_name="ANA",
    last_name="CARENINA",
    date_of_birth="2010-06-21",
    gender="FEMALE"
    ),
    Patient(
    registration_id=4 ,
    first_name="STEPHEN",
    last_name="KING",
    date_of_birth="2000-09-21",
    gender="MALE"
    ),
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
    ),
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
    MedicationRequest(
    medication_request_id=6,
    medication_reference="ASBD",
    reason="Diabities",
    prescription_date="2024-02-21T13:04:20.032Z",
    start_date="2024-06-21T13:04:20.032Z",
    end_date=None,
    frequency=4,
    status="ACTIVE",
    patient_refrence=1,
    clinician_refrence=1),
    MedicationRequest(
    medication_request_id=7,
    medication_reference="ASBDGDF",
    reason="Diabities",
    prescription_date="2024-01-21T13:04:20.032Z",
    start_date="2024-02-21T13:04:20.032Z",
    end_date=None,
    frequency=6,
    status="ON_HOLD",
    patient_refrence=2,
    clinician_refrence=2),
]
medication_requests_to_create = [
    {
  "patient_refrence": 1,
  "registration_id":1,
  "medication_request_id": 11,
  "medication_reference": "ASBDGHJKK",
  "reason": "Diabites",
  "prescription_date": "2023-06-21T13:04:20.032Z",
  "start_date": "2023-07-21T13:04:20.032Z",
  "end_date": "2024-06-21T13:04:20.032Z",
  "frequency": 2,
  "status": "ACTIVE",
    },
   {
  "patient_refrence": 2,
  "registration_id":2,
  "medication_request_id": 10,
  "medication_reference": "BBASD",
  "reason": "Cancer",
  "prescription_date": "2024-03-21T13:04:20.032Z",
  "start_date": "2024-02-21T13:04:20.032Z",
  "end_date": "2024-06-21T13:04:20.032Z",
  "frequency": 2,
  "status": "ON_HOLD",
    },
]


class MedicationRequests:
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



    @pytest.mark.parametrize("/", medication_requests_to_create)
    def test_post_medication(self, medication_requests: dict[Any, Any], client: TestClient) -> None:
        """
        Test that a medication request for a given patient can be created
        data.
        """
        response = client.post(
            "/medication_request/",
            json=medication_requests,
        )

    def test_get_medication_request_no_filters(
        self, client: TestClient
    ) -> None:
        """
        Test the get medication request endpoint with no filters.
        """
        response = client.get(
            "/medication_request/",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [{}]

    @pytest.mark.parametrize(
        ("status", "start_date", "end_date"),
        [("ON_HOLD"), ("2024-02-21T13:04:20.032Z"), ("2024-06-21T13:04:20.032Z")],
        [("ACTIVE"), ("2023-07-21T13:04:20.032Z"), ("2024-06-21T13:04:20.032Z")],

    )
    def test_get_medication_request_no_filters(
        self, client: TestClient
    ) -> None:
        """
        Test the get medication request endpoint.
        """
        response = client.get(
            "/medication_request/",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [{}]

