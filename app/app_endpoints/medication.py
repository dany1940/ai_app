from fastapi import APIRouter




router = APIRouter(prefix="/medication", tags=["medication"], responses={404:{"description": "Not Found"}})
