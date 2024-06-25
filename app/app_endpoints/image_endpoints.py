from fastapi import APIRouter, HTTPException, status

import app.schemas as app
from app import models
from app.dependencies import Database

router = APIRouter(
    prefix="/image", tags=["image"], responses={404: {"description": "Not Found"}}
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def post_image(
    patient: app.ImageCreate,
    database: Database,
):
    """
    Create a new Image in DB
    """

    new_image = models.Image(
        **patient.model_dump(),
    )
    database.add(new_image)
    database.commit()
