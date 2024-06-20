from fastapi import FastAPI
from app.app_endpoints.health import is_database_online
from fastapi_health import health  as api_health
from .app_endpoints import clinician, medication, medication_request, patient, health
import uvicorn


app = FastAPI(
    title="Medical Api",
    docs_url="/docs",
    version="0.0.1"
)

routers = [patient.router, clinician.router, medication.router, medication_request.router, health.router]
for router in routers:
    app.include_router(router)


app.add_api_route(
    "/health",
    api_health([is_database_online]),
)








