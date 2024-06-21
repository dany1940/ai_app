from fastapi import FastAPI
from fastapi_health import health as api_health

from app.app_endpoints.health import is_database_online

from .app_endpoints import (clinician, health, medication, medication_request,
                            patient)

app = FastAPI(title="Medical Api", docs_url="/docs", version="0.0.1")

routers = [
    patient.router,
    clinician.router,
    medication.router,
    medication_request.router,
    health.router,
]
for router in routers:
    app.include_router(router)


app.add_api_route(
    "/health",
    api_health([is_database_online]),
)
