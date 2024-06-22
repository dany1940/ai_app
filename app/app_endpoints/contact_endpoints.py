from fastapi import APIRouter, HTTPException, status

import app.schemas
from app import models
from app.dependencies import Contact, Database

router = APIRouter(
    prefix="/contact", tags=["contact"], responses={404: {"description": "Not Found"}}
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def post_contact(
    contact: app.schemas.ContactCreate,
    database: Database,
    existing_contact: Contact
):
    """
    Create a new Organisation
    """

    if existing_contact:
        raise HTTPException(
            409, detail="There is already a contact with this credentials"
        )

    new_contact = models.Contact(
        **contact.model_dump(),
    )
    database.add(new_contact)
    database.commit()
