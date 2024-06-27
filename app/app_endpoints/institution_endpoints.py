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


@router.post("/{institution_name}", status_code=status.HTTP_201_CREATED, response_model=None)
def post_institution(
    fields: InstitutionCreate,
    institution_name: str,
    database: Database,
    user: CurrentUser,
    existing_institution: Institution,
):
    """
    Create a new Institution
    """



    if existing_institution:
        raise HTTPException(
            409, detail="There is already an institution with this credentials"
        )
    if fields.organization_name:
        organization_id: int = expect(
            database.execute(
                select(models.Organization.id)
                .where(models.Organization.name == fields.organization_name)
            ).scalar_one_or_none(),
            error_msg="No organization could be found with that name",
        )
    else:
        organization_id = cast(int, user.organization_id)

    new_institution = models.Institution(
        organization_id=organization_id,
        name=institution_name,
        created_on=datetime.now(timezone.utc),
        **fields.model_dump(exclude={"institution_name", "organization_name"}),

    )
    database.add(new_institution)
    database.commit()

