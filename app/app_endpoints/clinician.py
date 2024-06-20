from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from app.dependencies import Database
import app.schemas
from app.crud.clinician import clinician as crud_clinician
from app import models


router = APIRouter(prefix="/clinician", tags=["clinician"], responses={404:{"description": "Not Found"}})

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def post_clinician(
    clinician: app.schemas.ClinicianCreate,
    database: Database,
) -> None:
    """
    Create a new Clinician in DB
    """

    existing_patient = crud_clinician.get(database, clinician.first_name, clinician.last_name, clinician.registration_id)

    if existing_patient:
        raise HTTPException(
            409, detail="There is already a clinician with this credentials"
        )
    new_clinician = models.Clinician(
        **clinician.model_dump(),

    )
    database.add(new_clinician)
    database.commit()
