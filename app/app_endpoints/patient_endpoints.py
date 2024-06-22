from fastapi import APIRouter, HTTPException, status

import app.schemas
from app import models
from app.dependencies import Database, Patient

router = APIRouter(
    prefix="/patient", tags=["patient"], responses={404: {"description": "Not Found"}}
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def post_patient(
    patient: app.schemas.PatientCreate,
    database: Database,
    existing_patient: Patient,
):
    """
    Create a new Patient in DB
    """

    if existing_patient:
        raise HTTPException(
            409, detail="There is already a patient with this credentials"
        )

    new_patient = models.Patient(
        **patient.model_dump(),
    )
    database.add(new_patient)
    database.commit()
