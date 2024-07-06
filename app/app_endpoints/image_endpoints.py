from fastapi import APIRouter, HTTPException, status

import app.schemas as app
from app import models
from app.dependencies import Database, Image
from datetime import datetime

router = APIRouter(
    prefix="/image", tags=["image"], responses={404: {"description": "Not Found"}}
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def post_image(
    image: app.ImageCreate,
    existing_image: Image,
    database: Database,
):
    """
    Create a new Image in DB
    """
    if existing_image:
        raise HTTPException(
            409, detail="There is already an image with this credentials"
        )
    new_image = models.Image(
        **image.model_dump(),
        created_on=datetime.now(),
    )
    database.add(new_image)
    await database.commit()
