from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .conf import config
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from fastapi import Depends
from app import models
from app import schemas
from sqlalchemy import and_, select, or_


SQLALCHEMY_DATABASE_URL = f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"
load_dotenv()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
)



Base = declarative_base()


def get_db():
    """
    Acquire database connection from the pool.
    """

    with Session(bind=engine) as database:
        yield database




Database = Annotated[Session, Depends(get_db)]

def get_patient(
    database: Database,
    patient: schemas.PatientCreate,
    )->models.Patient:
        """
        Get a  patient from database
        """

        return (
            database.execute(
                select(models.Patient)
                .where(
                    and_(models.Patient.first_name == patient.first_name,
                         models.Patient.last_name == patient.last_name,
                         models.Patient.date_of_birth == patient.date_of_birth
                         )
            )
            )
            .unique()
            .scalar_one_or_none()
        )

def get_clinician(
        database: Database,
        clinician: schemas.ClinicianCreate,
    ):
        """
        Get a  patient from database
        """

        return (
            database.execute(
                select(models.Clinician)
                .where(
                    and_(models.Clinician.first_name == clinician.first_name,
                         models.Clinician.last_name == clinician.last_name,
                         models.Clinician.registration_id == clinician.registration_id,
                         )
            )
            )
            .unique()
            .scalar_one_or_none()
        )
def get_medication(
        database: Database,
        medication: schemas.MedicationCreate
    ):
        """
        Get a  patient from database
        """

        return (
            database.execute(
                select(models.Medication)
                .where(
                    or_(models.Medication.medication_reference == medication.medication_reference,
                         models.Medication.code_name == medication.code_name,
             )
            )
            )
            .unique()
            .scalar_one_or_none()
        )
Medication = Annotated[None, Depends(get_medication)]
Clinician  = Annotated[None, Depends(get_clinician)]
Patient  = Annotated[None, Depends(get_patient)]







