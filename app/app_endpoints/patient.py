from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from app.dependencies import Database
import app.schemas
from app.crud.patient import patient as crud_patient
from app import models

router = APIRouter(prefix="/patient", tags=["patient"], responses={404:{"description": "Not Found"}})

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def post_patient(
    patient: app.schemas.PatientCreate,
    database: Database,
) -> None:
    """
    Create a new Patient in DB
    """

    existing_patient = crud_patient.get(database, patient.first_name, patient.last_name, patient.date_of_birth)

    if existing_patient:
        raise HTTPException(
            409, detail="There is already a patient with this credentials"
        )

    new_patient = models.Patient(
        **patient.model_dump(),

    )
    database.add(new_patient)
    database.commit()
