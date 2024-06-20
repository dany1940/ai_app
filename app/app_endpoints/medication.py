from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from app.dependencies import Database
from app.crud.medication import medication as crud_medication
import app.schemas
from app import models



router = APIRouter(prefix="/medication", tags=["medication"], responses={404:{"description": "Not Found"}})



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def post_medication(
    medication: app.schemas.MedicationCreate,
    database: Database,
) -> None:
    """
    Create a new Medication
    """
    existing_medication = crud_medication.get(database, medication.code, medication.code_name)

    if existing_medication:
        raise HTTPException(
            409, detail="There is medication, there is no need to add it in the system"
        )


    new_medication = models.Medication(
        **medication.model_dump(),

    )
    database.add(new_medication)
    database.commit()

