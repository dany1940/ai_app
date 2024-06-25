from fastapi import APIRouter, HTTPException, status

import app.schemas
from app import models
from app.dependencies import Clinician, Database, CurrentUser
from app.utils import expect
from sqlalchemy import select
from typing import cast, Annotated
from pydantic import Field
from datetime import datetime, timezone

router = APIRouter(
    prefix="/clinician",
    tags=["clinician"],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def post_clinician(
    fields: app.schemas.ClinicianCreate,
    database: Database,
    existing_clinician: Clinician,
    user: CurrentUser,
    email: str,
    first_name: Annotated[
        str,
        Field(
            title="Person first name",
            min_length=2,
            max_length=25,
            pattern=r"^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$",
            default="MARIA",
        ),
    ],
    last_name: Annotated[
        str,
        Field(
            title="person last name",
            min_length=2,
            max_length=25,
            pattern=r"^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$",
            default="DOE",
        ),
    ],
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
            database.execute(
                select(models.Institution.id)
                .where(models.Institution.name == fields.institution_name)
            ).scalar_one_or_none(),
            error_msg="No organization could be found with that name",
        )
    else:
        institution_id = cast(int, user.institution_id)
    new_clinician = models.Clinician(
        institution_id=institution_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        created_on=datetime.now(timezone.utc),
        updated_on=datetime.now(timezone.utc),
        **fields.model_dump(exclude={"institution_name"}),
    )

    database.add(new_clinician)
    database.commit()
