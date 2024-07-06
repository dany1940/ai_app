import zoneinfo
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import orm, select
from sqlalchemy.orm import load_only

import app.schemas
from app import models
from app.commons import PrescriptionStatusType
from app.dependencies import Clinician, Database, Patient, Prescription

router = APIRouter(
    prefix="/prescription",
    tags=["prescription"],
    responses={404: {"description": "Not Found"}},
)


@router.post(
    "/{prescription_id}", status_code=status.HTTP_201_CREATED, response_model=None
)
async def post_prescription(
    fields: app.schemas.PrescriptionCreate,
    prescription_code: str,
    existing_prescription: Prescription,
    patient: Patient,
    clinician: Clinician,
    medication_code: list[str],
    database: Database,
):
    """
    Create a new OPrescription in DB
    """
    if not patient:
        raise HTTPException(404, detail="Patient not found")
    if not clinician:
        raise HTTPException(404, detail="Clinician not found")

    if existing_prescription:
        raise HTTPException(
            409, detail="There is already a prescription with this credentials"
        )
    medication_json = {}

    for code in medication_code:
        medication = ( await database.scalars(
            select(models.Medication)
            .where(models.Medication.code_name == code)
            .options(load_only(models.Medication.indications, models.Medication.dosage))
        )).first()
        if not medication:
            raise HTTPException(404, detail=f"Medication code not found{code}")
        medication_json[code] = {
            "indications": medication.indications,
            "dossage": medication.dosage,
        }

    new_prescription = models.Prescription(
        clinician_refrence=clinician.registration_id,
        patient_refrence=patient.registration_id,
        prescription_code=prescription_code,
        updated_on=datetime.now(),
        created_on=datetime.now(),
        medication_json=medication_json,
        **fields.model_dump(exclude={"patient_name", "clinician_name"}),
    )

    database.add(new_prescription)
    await database.commit()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[app.schemas.GetPrescription],
)
async def get_medication_prescription_for_a_patient(
    database: Database,
    status_: PrescriptionStatusType | None = Query(
        default=None,
        description="Filter a medication by it's status",
    ),
    start_date_: datetime | None = Query(
        default=None,
        alias="start_date",
        description="Start Date of Prescription",  # noqa: E501
    ),
    end_date_: datetime | None = Query(
        default=None,
        alias="end_date",
        description="End Date of Prescription",  # noqa: E501
    ),
):
    """
    # Return a list of medication requests, inlcuding medication code and the clinician first and last name
    """
    # construct WHERE clause
    filters = []

    timezone_utc = zoneinfo.ZoneInfo("UTC")
    now = datetime.now(tz=timezone_utc)

    if end_date_ is None:
        end_date_ = now
    if start_date_ is None:
        start_date_ = now - timedelta(days=365)

    if end_date_.tzinfo is None:
        end_date_ = end_date_.replace(tzinfo=timezone_utc)
    if start_date_.tzinfo is None:
        start_date_ = start_date_.replace(tzinfo=timezone_utc)

    if start_date_ > end_date_:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "start time cannot be greater than end time",
        )
    if end_date_ < now - timedelta(days=365):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "end time cannot be more than 365 days in the past",
        )
    if end_date_ > now:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "end time cannot be in the future",
        )

    if status_ is not None:
        filters.append(models.Prescription.prescription_status == status_)

    return ( await database.execute(
        select(
            models.Prescription.reason,
            models.Prescription.created_on.label("prescription_date"),
            models.Prescription.start_date,
            models.Prescription.end_date,
            models.Prescription.frequency,
            models.Prescription.prescription_status,
            models.Prescription.medication_json,
            models.Prescription.prescription_code,
            models.Prescription.patient_refrence,
            models.Clinician.first_name.label("clinician_first_name"),
            models.Clinician.last_name.label("clinician_last_name"),
            models.Clinician.email.label("clinician_email"),
        )
        .join(
            models.Clinician,
            models.Prescription.clinician_refrence == models.Clinician.registration_id,
        )
        .join(
            models.Patient,
            models.Prescription.patient_refrence == models.Patient.registration_id,
        )
        .filter(*filters)
    )
    ).all()

