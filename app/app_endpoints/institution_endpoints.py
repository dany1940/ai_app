from fastapi import APIRouter, HTTPException, status

import app.schemas
from app import models
from app.dependencies import Database, Institution, Patient

router = APIRouter(
    prefix="/institution", tags=["institution"], responses={404: {"description": "Not Found"}}
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def post_institution(
    institution: app.schemas.InstitutionCreate,
    database: Database,
    existing_institution: Institution,
):
    """
    Create a new Institution
    """

    if existing_institution:
        raise HTTPException(
            409, detail="There is already a institution with this credentials"
        )

    new_institution = models.Patient(
        **institution.model_dump(),
    )
    database.add(new_institution)
    database.commit()


