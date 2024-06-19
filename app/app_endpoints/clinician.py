from fastapi import APIRouter




router = APIRouter(prefix="/clinician", tags=["clinician"], responses={404:{"description": "Not Found"}})
