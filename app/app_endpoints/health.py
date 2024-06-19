import logging
from app.dependencies import Database
from fastapi import APIRouter




router = APIRouter(prefix="/health", tags=["health"], responses={404:{"description": "Not Found"}})


def is_database_online(database=Database):
    try:
        database.execute("SELECT 1")
        return True
    except Exception:
        logging.exception("An unexpected error occurred when connecting to DB")
        return False
