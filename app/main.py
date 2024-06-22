from fastapi import FastAPI
from fastapi_health import health as api_health

from app.app_endpoints.health_endpoints import is_database_online

from .app_endpoints import (auth_endpoints, clinician_endpoints,
                            contact_endpoints, health_endpoints,
                            image_endpoints, institution_endpoints,
                            medication_enpoints, medication_request_endpoints,
                            organisation_endpoints, patient_endpoints,
                            user_endpoints)

app = FastAPI(title="Medical Api", docs_url="/docs", version="0.0.1")

routers = [
    auth_endpoints.router,
    clinician_endpoints.router,
    health_endpoints.router,
    contact_endpoints.router,
    image_endpoints.router,
    medication_enpoints.router,
    medication_request_endpoints.router,
    organisation_endpoints.router,
    institution_endpoints.router,
    patient_endpoints.router,
    user_endpoints.router,

]
for router in routers:
    app.include_router(router)


app.add_api_route(
    "/health",
    api_health([is_database_online]),
)
