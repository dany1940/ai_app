from fastapi import APIRouter, HTTPException, status
from  app.dependencies import get_db

import app.schemas
from app import models
from app.dependencies import Clinician, Database

router = APIRouter(
    prefix="/clinician",
    tags=["clinician"],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def post_clinician(
    clinician: app.schemas.ClinicianCreate,
    database: Database,
    existing_clinician: Clinician,
) -> None:
    """
    Create a new Clinician in DB
    """

    if existing_clinician:
        raise HTTPException(
            409, detail="There is already a clinician with this credentials"
        )

    new_clinician = models.Clinician(
        **clinician.model_dump(),
    )

    database.add(new_clinician)
