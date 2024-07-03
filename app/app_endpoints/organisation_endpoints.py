from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import Ltree

from app import models
from app.dependencies import CurrentAdminUser, Database
from app.schemas import OrganizationCreate

router = APIRouter(
    prefix="/organization",
    tags=["organization"],
    responses={404: {"description": "Not Found"}},
)


@router.post(
    "/{organization_name}",
    status_code=status.HTTP_201_CREATED,
)
async def create_organization(
    organization_name: str,
    organization_fields: OrganizationCreate,
    db_session: Database,
):
    """
    Create a new organization.
    """

    parent_organization_path = (await db_session.scalars(
        select(models.Organization.path).where(
            models.Organization.name == organization_fields.parent
        )
    )).first()
    try:
        organization_id = (await  db_session.scalars(
            insert(models.Organization)
            .values(
                name=organization_name,
                created_on=func.now(),
                # The organization requires a path field which is in the form
                # "<parent_organization.path>.<organization_id>" in order to
                # achieve this, we insert the organization with a placeholder
                # path of "1", and then update it with the correct path
                path=Ltree("A"),
                **organization_fields.model_dump(exclude={"parent"}, mode="json"),
            )
            .returning(models.Organization.id)
        )).first()
        await db_session.commit()
    except IntegrityError as error:
        # The error that can occur here is a 409 (Conflict)
        # and the only UNIQUE field on this table is "name".
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An organization with that name already exists",
        ) from error
    print(organization_id)
    query = (
        update(models.Organization)
        .where(models.Organization.id == organization_id)
        .values(path=Ltree(f"{parent_organization_path or 'A'}.{organization_id}"))
    )
    await db_session.execute(query)
    await db_session.commit()
