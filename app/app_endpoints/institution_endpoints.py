from fastapi import APIRouter, HTTPException, status
from app import models
from app.dependencies import Database, Institution, CurrentUser
from app.schemas import InstitutionCreate
from datetime import datetime
from datetime import timezone
from app.utils import expect
from sqlalchemy import select
from typing import cast

router = APIRouter(
    prefix="/institution",
    tags=["institution"],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def post_institution(
    fields: InstitutionCreate,
    name: str,
    database: Database,
    user: CurrentUser,
    existing_institution: Institution,
):
    """
    Create a new Institution
    """



    if existing_institution:
        raise HTTPException(
            409, detail="There is already a clinician with this credentials"
        )
    if fields.institution_name:
        institution_id: int = expect(
            database.execute(
                select(models.Institution.id)
                .where(models.Institution.name == fields.institution_name)
            ).scalar_one_or_none(),
            error_msg="No organization could be found with that name",
        )
    else:
        institution_id = cast(int, user.institution_id)

    new_institution = models.Institution(
        institution_id=institution_id,
        name=name,
        created_on=datetime.now(timezone.utc),
        **fields.model_dump(exclude={"institution_name"}),

    )
    database.add(new_institution)
    database.commit()

