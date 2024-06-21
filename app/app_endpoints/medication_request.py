import zoneinfo
from app import models
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query
from fastapi import status
from app.commons import StatusType
from datetime import datetime
from datetime import timedelta
from app.dependencies import Database, MedicationById, ClinicianById, MedicationRequestById
import app.schemas as schemas
from sqlalchemy.sql import select, and_
from sqlalchemy.orm import load_only
from sqlalchemy import update

router = APIRouter(prefix="/medication_request", tags=["medication_request"], responses={404:{"description": "Not Found"}})


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def post_medication_request(

    medication_request: schemas.MedicationRequestCreate,
    database: Database,
    existing_patient: MedicationById,
    existing_clinician: ClinicianById,

) -> None:
    """

    # Create a medication Request
    """

    if not existing_patient:
        raise HTTPException(
            404, detail="There is no patient to prescribe"
        )

    if not existing_clinician:
        raise HTTPException(
            404, detail="There is no clinician in the system, please ask the admin to add one!"
        )
    new_medication_request= models.MedicationRequest(
        **medication_request.model_dump( ),
        clinician_refrence=existing_clinician.registration_id,
        patient_refrence=existing_patient.registration_id

    )
    database.add(new_medication_request)
    database.commit()




@router.get("/", status_code=status.HTTP_200_OK)
async def get_medication_request_for_a_patient(
    database: Database,
    status_: StatusType
    | None = Query(
        default=None,
        description="Filter a medication by it's status",
    ),
    start_date_: datetime
    | None = Query(
        default=None,
        alias="start_date",
        description="Start Date of Prescription",  # noqa: E501
    ),
    end_date_: datetime
    | None = Query(
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


    return (
        database.execute(
            select(
                    models.MedicationRequest,
                    models.Clinician,
                    models.Medication,
                    )
            .join(models.Medication, models.Medication.medication_reference == models.MedicationRequest.medication_reference)
            .join(models.Clinician, models.Clinician.registration_id == models.MedicationRequest.clinician_refrence)
            .options(load_only(
                    models.MedicationRequest.clinician_refrence,
                    models.MedicationRequest.status,
                    models.MedicationRequest.start_date,
                    models.MedicationRequest.end_date,
                    models.MedicationRequest.prescription_date,
                    ))
            .options(load_only(
                    models.Clinician.first_name,
                    models.Clinician.last_name,
                    ))
            .options(load_only(models.Medication.code_name))
            .where(
            and_(
                models.MedicationRequest.end_date <= end_date_,
                models.MedicationRequest.start_date >= start_date_,
            )
        )
            .filter(*filters)
            .group_by(models.MedicationRequest, models.Clinician, models.Medication)

        )

        .scalars()
        .all()
    )



@router.patch("/{medication_request_id}", status_code=status.HTTP_200_OK)
def modify_medication_request(
    medication_request_update: schemas.MedicationRequestUpdate,
    existing_medication_request: MedicationRequestById,
    database: Database
):
    if not existing_medication_request:
        raise HTTPException(
            404, detail="There is no medication request with that id"
        )

    database.execute(
        update(models.MedicationRequest).values(
            end_date=medication_request_update.end_date,
            frequency=medication_request_update.frequency,
            status=medication_request_update.status,

        ).where(models.MedicationRequest.medication_request_id == existing_medication_request.medication_request_id
        )
    )
    database.commit()




