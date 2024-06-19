from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from dependencies import Database
import schemas

router = APIRouter(prefix="/medication_request")

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def post_patient(
    patient: schemas.PatientCreate,
    database: Database,
) -> None:
    """
    Create a new Patient in DB
    """

    patient = []
    if patient:
        raise HTTPException(
            409, detail="There is aalready a patient with this credentials"
        )




