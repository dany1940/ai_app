import logging
import sys
from contextlib import asynccontextmanager

from app.app_endpoints import (user_endpoints, auth_endpoints, organisation_endpoints, institution_endpoints, patient_endpoints,
clinician_endpoints, image_endpoints)
from app.database import sessionmanager
from fastapi import FastAPI

logging.basicConfig(stream=sys.stdout)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, docs_url="/api/docs")


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Routers
routers = [
    auth_endpoints.router,
    organisation_endpoints.router,
    user_endpoints.router,
    institution_endpoints.router,
    patient_endpoints.router,
    clinician_endpoints.router,
    image_endpoints.router,

]
for router in routers:
    app.include_router(router)

