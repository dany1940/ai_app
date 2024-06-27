from fastapi import APIRouter, HTTPException, status
import app.schemas
import zoneinfo
from app import models
from app.dependencies import Database, Prescription,  Patient, Clinician
from datetime import datetime
from datetime import timezone, timedelta
from sqlalchemy import select
from sqlalchemy.orm import load_only
from app.commons import StatusType
from fastapi import Query
from sqlalchemy import orm


router = APIRouter(
    prefix="/prescription", tags=["prescription"], responses={404: {"description": "Not Found"}}
)


@router.post("/{prescription_id}", status_code=status.HTTP_201_CREATED, response_model=None)
def post_prescription(
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
        raise HTTPException(
            404, detail="Patient not found"
        )
    if not clinician:
        raise HTTPException(
            404, detail="Clinician not found"
        )

    if existing_prescription:
        raise HTTPException(
            409, detail="There is already a prescription with this credentials"
        )
    medication_json = {}

    for code in medication_code:
        medication = database.execute(
            select(models.Medication)
            .where(models.Medication.code_name == code)
            .options(load_only(models.Medication.indications, models.Medication.dosage))
        ).scalar_one_or_none()
        print(medication)
        if not medication:
            raise HTTPException(
                404, detail=f"Medication code not found{code}"
            )
        medication_json[code] = {
            "indications": medication.indications,
            "dossage": medication.dosage,
        }

    new_prescription = models.Prescription(
        clinician_refrence=clinician.registration_id,
        patient_refrence=patient.registration_id,
        prescription_code=prescription_code,
        updated_on=datetime.now(timezone.utc),
        created_on=datetime.now(timezone.utc),
        medication_json=medication_json,
        **fields.model_dump(exclude={"patient_name", "clinician_name"}),

    )

    database.add(new_prescription)
    database.commit()


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[app.schemas.GetPrescription])
async def get_medication_prescription_for_a_patient(
    database: Database,
    status_: StatusType | None = Query(
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
        filters.append(models.MedicationRequest.status == status_)

    return(
        database.execute(
            select(
                models.Prescription,
            )
            .options(orm.joinedload(models.Prescription.clinician))
            .options(orm.joinedload(models.Prescription.patient))
        )

        .scalars()
        .all()
    )


@router.patch("/{medication_request_id}", status_code=status.HTTP_200_OK)
def modify_medication_request(
    medication_request_update: str,
    existing_medication_request:str,
    database: Database,
):
  pass
