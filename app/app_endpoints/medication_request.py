import zoneinfo
from app import models
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query
from fastapi import status
from app.commons import StatusType
from datetime import datetime
from datetime import timedelta
from app.dependencies import Database
from sqlalchemy.sql import and_
from sqlalchemy.sql import select



router = APIRouter(prefix="/medication_request", tags=["medication_request"], responses={404:{"description": "Not Found"}})



@router.get("/")
async def get_medication_request_for_a_patient(
    database: Database,
    patient_name: str,
    patient_surname: str,
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
    patient =  (database.execute(
    select(models.Patient)
    .where(
    and_(
    models.Patient.first_name == patient_name,
    models.Patient.last_name == patient_surname,
    )
    )
    )
    ).scalar_one_or_none()

    if patient is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="There is no patient with that name and surname",
        )

    timezone_utc = zoneinfo.ZoneInfo("UTC")
    now = datetime.now(tz=timezone_utc)

    if end_date_ is None:
        end_date_ = now
    if start_date_ is None:
        start_date_ = now - timedelta(days=10)

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




@router.get("/")
async def get_medication_request(
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
        start_date_ = now - timedelta(days=10)

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
