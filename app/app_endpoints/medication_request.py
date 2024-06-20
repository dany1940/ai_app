import zoneinfo
from app import models
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query, Path
from fastapi import status
from app.commons import StatusType
from datetime import datetime
from datetime import timedelta
from app.dependencies import Database
from sqlalchemy import select
from sqlalchemy import and_
import app.schemas
from app.schemas import MedicationRequest



router = APIRouter(prefix="/medication_request", tags=["medication_request"], responses={404:{"description": "Not Found"}})


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def post_medication_request(
    patient_reference: int,
    medication_request: app.schemas.MedicationRequestCreate,
    database: Database,
    registration_id: int = Query(
        default=None,
        alias="practian_id",
        description="Practician who prescribed!",  # noqa: E501
    ),

) -> None:
    """

    # Create a medication Request
    """

    existing_patient =  (database.execute(
                select(models.Patient)
                .where(
                    and_(models.Patient.registration_id == patient_reference
                         )
            )
            )
            .unique()
            .scalar_one_or_none()
    )

    if not existing_patient:
        raise HTTPException(
            404, detail="There is no patient to prescribe"
        )
    existing_clinician = (database.execute(
                select(models.Clinician)
                .where(
                    and_(models.Clinician.registration_id == registration_id
                         )
            )
            )
            .unique()
            .scalar_one_or_none()
    )

    if not existing_clinician:
        raise HTTPException(
            404, detail="There is no clinician in the system, please ask the admin to add one!"
        )
    new_medication_request= models.MedicationRequest(
        **medication_request.model_dump( ),
        patient_refrence = patient_reference,
        clinician_refrence = registration_id

    )
    database.add(new_medication_request)
    database.commit()




@router.get("/", response_model=list[MedicationRequest])
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
    filters =[]



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

    medical_requests =  (
        database.query(models.MedicationRequest)
        .filter(*filters)
    )

    return database.execute(medical_requests).unique().all()

