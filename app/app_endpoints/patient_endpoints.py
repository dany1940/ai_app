from datetime import datetime, timezone
from typing import cast

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import and_, select

import app.schemas
from app import models
from app.dependencies import CurrentUser, Database, Patient
from app.utils import expect

router = APIRouter(
    prefix="/patient", tags=["patient"], responses={404: {"description": "Not Found"}}
)


@router.post(
    "/{patient_code}", status_code=status.HTTP_201_CREATED, response_model=None
)
async def post_patient(
    fields: app.schemas.PatientCreate,
    patient_code: str,
    patient: Patient,
    db_session: Database,
    user: CurrentUser,
):
    """
    Create a new Patient in DB
    """

    if patient:
        raise HTTPException(
            409, detail="There is already a patient with this credentials"
        )
    if fields.institution_name:
        institution_id: int = expect(
           (await db_session.scalars(
                select(models.Institution.id).where(
                    models.Institution.name == fields.institution_name
                )
            )
        ).first(),
            error_msg="No institution could be found with that name",
        )
    else:
        institution_id = cast(int, user.institution_id)

    if fields.clinician_code:
        clinician_id: int = expect(
            (await db_session.scalars(
                select(models.Clinician.registration_id).where(
                    and_(
                        models.Clinician.clinician_code == fields.clinician_code,
                        models.Clinician.institution_id == institution_id,
                    )
                )
            )).first(),
            error_msg="No clinician could be found with that name",
        )
    else:
        clinician_id = cast(int, user.institution_id)

    new_patient = models.Patient(
        institution_id=institution_id,
        patient_code=patient_code,
        clinician_id=clinician_id,
        updated_on=datetime.now(timezone.utc),
        created_on=datetime.now(timezone.utc),
        **fields.model_dump(
            exclude={"institution_name", "clinician_code", "patient_code"}
        ),
    )

    db_session.add(new_patient)
    await db_session.commit()
