from datetime import datetime, timezone
from typing import Annotated, List, cast

from fastapi import APIRouter, HTTPException, status
from pydantic import Field
from sqlalchemy import and_, select

import app.schemas
from app import models
from app.dependencies import (Apointment, Clinician, CurrentUser, Database,
                              Institution, Patient)
from app.utils import expect

router = APIRouter(
    prefix="/apointments",
    tags=["apointments"],
    responses={404: {"description": "Not Found"}},
)


@router.post(
    "/{apointment_code}", status_code=status.HTTP_201_CREATED, response_model=None
)
def post_apointments(
    fields: app.schemas.ApointmentsCreate,
    apointment_code: str,
    database: Database,
    existing_patient: Patient,
    existing_clinician: Clinician,
    existing_institution: Institution,
    existing_apointment: Apointment,
    user: CurrentUser,
):
    """
    Create a new Apointments in DB
    """

    if existing_apointment:
        raise HTTPException(409, detail="There is already an apointment with this code")

    if not existing_patient:
        raise HTTPException(409, detail="There is no patient with this credentials")
    if not existing_clinician:
        raise HTTPException(409, detail="There is no clinician with this credentials")
    if not existing_institution:
        raise HTTPException(409, detail="There is no institution with this credentials")

    new_apointment = models.Apointments(
        institution_refrence=existing_institution.id,
        clinician_refrence=existing_clinician.registration_id,
        patient_refrence=existing_patient.registration_id,
        apointment_code=apointment_code,
        updated_on=datetime.now(timezone.utc),
        creted_on=datetime.now(timezone.utc),
        **fields.model_dump(exclude={"apointment_code"}),
    )
    database.add(new_apointment)
    database.commit()
