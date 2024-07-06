from datetime import datetime, timezone
from typing import Annotated, cast

from fastapi import APIRouter, HTTPException, status
from pydantic import Field
from sqlalchemy import select

import app.schemas
from app import models
from app.dependencies import Clinician, CurrentUser, Database
from app.utils import expect

router = APIRouter(
    prefix="/clinician",
    tags=["clinician"],
    responses={404: {"description": "Not Found"}},
)


@router.post(
    "/{clinician_code}", status_code=status.HTTP_201_CREATED, response_model=None
)
async def post_clinician(
    fields: app.schemas.ClinicianCreate,
    database: Database,
    clinician_code: str,
    existing_clinician: Clinician,
    user: CurrentUser,
) -> None:
    """
    Create a new Clinician in DB
    """

    if existing_clinician:
        raise HTTPException(
            409, detail="There is already a clinician with this credentials"
        )
    if fields.institution_name:
        institution_id: int = expect(
           ( await database.scalars(
                select(models.Institution.id).where(
                    models.Institution.name == fields.institution_name
                )
            )).first(),
            error_msg="No institution could be found with that name",
        )
    else:
        institution_id = cast(int, user.institution_id)
    new_clinician = models.Clinician(
        institution_id=institution_id,
        clinician_code=clinician_code,
        created_on=datetime.now(),
        updated_on=datetime.now(),
        **fields.model_dump(exclude={"institution_name"}),
    )

    database.add(new_clinician)
    await database.commit()
