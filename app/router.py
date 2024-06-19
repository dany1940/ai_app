import importlib
from typing import Final

from fastapi import APIRouter
from fastapi import status


routers: Final = (
    {"path": "app.patient", "tags": []},
    {"path": "app.clinician", "tags": []},
    {"path": "app.medication", "tags": []},
    {"path": "app.medication_request", "tags": []}

)

router = APIRouter(
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unable to authenticte."
        },
    }
)

for router_ in routers:
    module = importlib.import_module(router_["path"])  # type: ignore
    router.include_router(
        module.router,
        tags=router_["tags"],  # type: ignore
        include_in_schema=True,
    )
