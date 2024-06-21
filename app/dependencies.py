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
    ) -> models.Clinician:
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
    ) -> models.Medication:
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

def get_medication_by_id(
            database: Database,
            patient_refrence: int,
    ) -> models.Medication:
     return(database.execute(
                select(models.Patient)
                .where(
                    and_(models.Patient.registration_id == patient_refrence
                         )
            )
            )
            .unique()
            .scalar_one_or_none()
    )

def get_clinician_by_id(
            database: Database,
            registration_id: int,
    ) -> models.Clinician:
      return (database.execute(
                select(models.Clinician)
                .where(
                    and_(models.Clinician.registration_id == registration_id
                         )
            )
            )
            .unique()
            .scalar_one_or_none()
    )

def get_medication_request_by_id(
            database: Database,
            medication_request_id: str,
    ) -> models.MedicationRequest:
      return (database.execute(
                select(models.MedicationRequest)
                .where(
                    and_(models.MedicationRequest.medication_request_id == medication_request_id
                         )
            )
            )
            .unique()
            .scalar_one_or_none()
    )



Medication = Annotated[models.Medication, Depends(get_medication)]
Clinician  = Annotated[models.Clinician, Depends(get_clinician)]
Patient  = Annotated[models.Patient, Depends(get_patient)]
MedicationById = Annotated[models.Medication, Depends(get_medication_by_id)]
ClinicianById =  Annotated[models.Clinician, Depends(get_clinician_by_id)]
MedicationRequestById= Annotated[models.MedicationRequest, Depends(get_medication_request_by_id)]







