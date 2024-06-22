from fastapi import APIRouter, HTTPException, status

import app.schemas
from app import models
from app.dependencies import Database, Patient

router = APIRouter(
    prefix="/image", tags=["image"], responses={404: {"description": "Not Found"}}
)


def get_image(image_id: int, database: Database) -> models.Image:
    image = database.get(models.Image, image_id)
    if not image:
        raise HTTPException(404, detail="Image not found")
    return image
