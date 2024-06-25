from fastapi import APIRouter, HTTPException, status
import app.schemas
from app import models
from app.dependencies import Database, Patient, CurrentUser
from datetime import datetime
from datetime import timezone
from app.utils import expect
from sqlalchemy import select
from typing import cast, Annotated
from pydantic import Field
from sqlalchemy import and_


router = APIRouter(
    prefix="/patient", tags=["patient"], responses={404: {"description": "Not Found"}}
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def post_patient(
    fields: app.schemas.PatientCreate,
    database: Database,
    existing_patient: Patient,
    user: CurrentUser,
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
    date_of_birth: Annotated[
        datetime,
        Field(
            title="Date of birth",
            description="The date of birth of the patient",
            example="2021-08-31",
            default_factory=datetime.now,
        ),
    ],
):
    """
    Create a new Patient in DB
    """

    if existing_patient:
        raise HTTPException(
            409, detail="There is already a patient with this credentials"
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

    if fields.clinician_name:
        clinician_id: int = expect(
            database.execute(
                select(models.Clinician.registration_id)
                .where(and_(models.Clinician.first_name == fields.clinician_first_name,
                             models.Clinician.last_name == fields.clinician_last_name,
                            models.Clinician.institution_id == institution_id)
                )
            ).scalar_one_or_none(),
            error_msg="No organization could be found with that name",
        )
    else:
        clinician_id = cast(int, user.institution_id)

    new_patient = models.Patient(
        institution_id=institution_id,
        clinician_id=clinician_id,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        updated_on=datetime.now(timezone.utc),
        created_on=datetime.now(timezone.utc),
        **fields.model_dump(exclude={"institution_name"}),

    )

    database.add(new_patient)
    database.commit()
