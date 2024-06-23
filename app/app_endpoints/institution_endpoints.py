from fastapi import APIRouter, HTTPException, status

from app import models
from app.dependencies import Database, Institution
from app.schemas import InstitutionCreate

router = APIRouter(
    prefix="/institution",
    tags=["institution"],
    responses={404: {"description": "Not Found"}},
)
