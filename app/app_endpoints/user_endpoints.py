from typing import cast

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import delete, insert, or_, update
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import select

from app import models
from app.dependencies import CurrentAdminUser, CurrentUser, Database
from app.schemas import UserCreate, UserPasswordUpdate, UserUpdate
from app.security import get_password_hash, verify_password

router = APIRouter(
    prefix="/api/user", tags=["user"], responses={404: {"description": "Not Found"}}
)

from typing import cast

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import delete, insert, or_, update
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import select

from app import models
from app.dependencies import CurrentAdminUser, CurrentUser, Database
from app.schemas import UserCreate, UserPasswordUpdate, UserUpdate
from app.security import get_password_hash, verify_password

router = APIRouter(
    prefix="/user", tags=["user"], responses={404: {"description": "Not Found"}}
)


@router.get("/me", response_model=None)
async def get_current_user(
    user: CurrentUser,
):
    """
    Get the currently logged in user.
    """

    return user


@router.put("/me/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(
    password_fields: UserPasswordUpdate,
    user: CurrentUser,
    db_session: Database,
):
    """
    Update the password of the currently logged in user.
    """

    existing_password_hash = cast(str, user.pword_hash)

    if password_fields.new_password != password_fields.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirm password do not match.",
        )

    if verify_password(password_fields.new_password, existing_password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from old password.",
        )

    if not verify_password(password_fields.old_password, existing_password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password."
        )

    query = (
        update(models.User)
        .where(models.User.id == user.id)
        .values(pword_hash=get_password_hash(password_fields.new_password))
    )
    await db_session.execute(query)
    await db_session.commit()


@router.put("/me")
async def update_current_user(
    new_user: UserUpdate,
    database: Database,
    user: CurrentUser,
):
    """
    Update the currently logged in user.
    """
    existing_user =(await
        database.scalars(
            select(models.User)
            .where(models.User.id != user.id)
            .where(
                or_(
                    models.User.username == new_user.username,
                    models.User.email == new_user.email,
                )
            )
        )
    ).all()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with that username or email already exists",
        )

    query = (
        update(models.User)
        .where(models.User.id == user.id)
        .values(
            firstname=new_user.firstname,
            email=new_user.email,
            lastname=new_user.lastname,
            username=new_user.username,
        )
    )
    await database.execute(query)
    await database.commit()


@router.get("/users/{username}", response_model=None)
async def get_user(
    username: str,
    user: CurrentAdminUser,
    db_session: Database,
):
    user = await(
        select(models.User)
        .where(models.User.username == username)
        .options(joinedload(models.User.organization))
        .where(
            models.User.organization_id.in_(
                select(models.Organization.id).where(
                    models.Organization.path.descendant_of(user.organization.path)
                )
            )
        )
    )
    return user

@router.post("/{username}")
async def create_user(
    username: str,
    user: UserCreate,
    db_session: Database,
    current_user: CurrentAdminUser,
):
    """
    Create a new user in your organization.
    """
    existing_user =  (await db_session.scalars(select(models.User).where(models.User.username == username))).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with that username or email already exists",
        )
    if not user.organization_name:
        organization_id = current_user.organization_id
    else:
        organization_id =  (await db_session.scalars(
            select(models.Organization.id)
            .where(models.Organization.name == user.organization_name)
            .where(
                models.Organization.path.descendant_of(current_user.organization.path)
            )
        )).first()

        if organization_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No organization could be found with that name",
            )
    query = insert(models.User).values(
            username=username,
            email=user.email,
            firstname=user.firstname,
            lastname=user.lastname,
            pword_hash=get_password_hash(user.password),
            organization_id=organization_id,
            can_edit=user.is_admin,
        )
    user = await db_session.execute(query)
    await db_session.commit()




@router.delete(
    "/user/{username}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    username: str,
    db_session: Database,
    current_user: CurrentAdminUser,
):
    if username == current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot delete your own account",
        )

    user_to_delete  = ( await db_session.scalars(
        select(models.User.id)
        .where(
            models.User.username == username,
        )
        .where(
            models.User.organization_id.in_(
                select(models.Organization.id).where(
                    models.Organization.path.descendant_of(
                        current_user.organization.path
                    )
                )
            )
        )
    )
    ).first()


    if user_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user could be found with that username",
        )

    query = (delete(models.User).where(models.User.username == username))
    await db_session.execute(query)
    await db_session.commit()
