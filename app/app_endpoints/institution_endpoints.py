from fastapi import APIRouter, HTTPException, status

from app import models
from app.dependencies import CurrentUser, Database, Institution
from app.schemas import InstitutionCreate

router = APIRouter(
    prefix="/institution",
    tags=["institution"],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def post_institution(
    clinician: InstitutionCreate,
    database: Database,
    existing_clinician: Institution,
):
    """
    Create a new Clinician in DB
    """

    if existing_clinician:
        raise HTTPException(
            409, detail="There is already a clinician with this credentials"
        )


    new_institution = models.Institution(
        **clinician.model_dump(),

    )



    database.add(models.Institution(
        name=clinician.name,
        created_on=clinician.created_on,
        contact_number=clinician.contact_number,
        id=clinician.id,
        clinician.clinician_id=clinician.id,
        organization_id=clinician.organization_id,
    ))
    database.commit()
