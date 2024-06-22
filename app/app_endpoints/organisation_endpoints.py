from fastapi import APIRouter, HTTPException, status

import app.schemas
from app import models
from app.dependencies import Database, Organisation

router = APIRouter(
    prefix="/organistation", tags=["organisation"], responses={404: {"description": "Not Found"}}
)




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def post_organisation(
    organisation: app.schemas.OrganizationCreate,
    database: Database,
    existing_organisation: Organisation,
):
    """
    Create a new Organisation
    """

    if existing_organisation:
        raise HTTPException(
            409, detail="There is already a organisation with this credentials"
        )

    new_organisation = models.Organization(
        **organisation.model_dump(),
    )
    database.add(new_organisation)
    database.commit()


@router.post(
    "/organizations/{organization_name}",
    dependencies=[Depends(get_current_admin_rl_user)],
)
def create_organization(
    organization_name: str,
    organization_fields: OrganizationCreate,
    database: Database,
):
    """
    Create a new organization.
    """

    parent_organization_path = database.execute(
        select(models.Organization.path).where(
            models.Organization.name == organization_fields.parent
        )
    ).scalar_one_or_none()

    try:
        organization_id = database.execute(
            insert(models.Organization)
            .values(
                name=organization_name,
                created_on=func.now(),
                # The organization requires a path field which is in the form
                # "<parent_organization.path>.<organization_id>" in order to
                # achieve this, we insert the organization with a placeholder
                # path of "1", and then update it with the correct path
                path=Ltree("1"),
                **organization_fields.model_dump(exclude={"parent"}, mode="json"),
            )
            .returning(models.Organization.id)
        ).scalar_one_or_none()
    except sqlalchemy.exc.IntegrityError as error:
        # The only (famous last words) error that can occur here is a 409 (Conflict)
        # since the address, email, etc. have already been validated by pydantic
        # and the only UNIQUE field on this table is "name".
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An organization with that name already exists",
        ) from error

    database.execute(
        update(models.Organization)
        .where(models.Organization.id == organization_id)
        .values(path=Ltree(f"{parent_organization_path or '1'}.{organization_id}"))
    )
    database.commit()

