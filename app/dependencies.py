from typing import Annotated, cast


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import and_, select

from sqlalchemy.orm import Session, joinedload
from app import models
from app.conf import config
from app.security import verify_password
from app.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")







Database = Annotated[AsyncSession, Depends(get_db_session)]






def get_organization() -> models.Organization | None:
    """
    Get a  organization from database
    """
    pass



async def authenticate_user(db_session: Database, username: str, password: str):
    user = (await db_session.scalars(select(models.User).where(models.User.username == username))).first()

    if user is None:
        return None
    if not verify_password(password, cast(str, user.pword_hash)):
        return None
    return user


async def user_from_token(
    token: str,
    db_session: Database,
    credentials_exception: Exception | None = None,
) -> models.User:
    """
    Get the currently logged in user from a JWT token.

    If the token is valid, return the currently logged in user. If the token is
    invalid, raise the given exception. If no exception is given, raise an
    `HTTP 401 (Unauthorized)` exception.

    For HTTP endpoints, this function should not be called directly. Instead,
    use `Depends(get_current_user)`, or the `CurrentUser` annotated type. For
    WebSocket endpoints, this function should be called directly, with the token
    received as the first message from the WebSocket client.
    """
    if credentials_exception is None:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            token,
            config.SECRET_KEY,
            algorithms=[config.HASH_ALGORITHM],
        )
    except JWTError as error:
        raise credentials_exception from error

    if payload.get("type") != "access":
        raise credentials_exception

    username = cast(str | None, payload.get("sub"))
    if username is None:
        raise credentials_exception
    user = (await db_session.scalars(select(models.User)
        .filter(models.User.username == username)
        .join(models.User.organization)
        .options(joinedload(models.User.organization)))).first()

    return user


async def get_current_user(
    database: Database,
    token: str = Depends(oauth2_scheme),
):
    """
    Validate the user's JWT token.

    If the token is valid, return the currently logged in user.
    If the token is invalid, raise a 401 (Unauthorized) exception.
    """
    user = await user_from_token(token, database)
    return user


CurrentUser = Annotated[models.User, Depends(get_current_user)]


def get_current_super_user(user: CurrentUser):
    """
    Returns the current user if they're in the RL Automotive
    """
    if user.organization_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have insufficient rights to access this resource",
        )
    return user


def get_current_admin_user(user: CurrentUser):

    if user.organization_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have insufficient rights to access this resource",
        )
    return user


async def get_institution(
    database: Database, institution_name: str, user: CurrentUser
) -> models.Institution | None:
    """
    Get a  institution from database
    """

    institution =  (
        await database.scalars(
            select(models.Institution)
            .where(models.Institution.name == institution_name)
            )
        ).first()
    return  institution

async def get_clinician(
    database: Database,
    clinician_code: str,
) -> models.Clinician | None:
    """
    Get a  clinician from database
    """

    clinician = (
        await database.scalars(
            select(models.Clinician).where(
                and_(
                    models.Clinician.clinician_code == clinician_code,
                )
            )
        )
    ).first()

    return clinician


async def get_patient_by_code(
    database: Database,
    patient_code: str,
) -> models.Patient | None:
    """
    Get a  patient from database
    """

    patient = (
        await database.scalars(
            select(models.Patient).where(
                and_(
                    models.Patient.patient_code == patient_code,
                )
            )
        )
    ).first()
    return patient

async def get_medication(
    database: Database,
    medication_code: str,
) -> models.Medication | None:
    """
    Get a  patient from database
    """

    medication =  (
    await  database.scalars(
            select(models.Medication).where(
                and_(
                    models.Medication.code_name == medication_code,
                )
            )
        )
    ).first()
    return medication

async def get_prescription(
    database: Database,
    prescription_code: str,
    user: CurrentUser,
) -> models.Prescription | None:
    """
    Get a  prescription from database
    """
    prescription = (
        await database.scalars(
            select(models.Prescription.prescription_code).where(
                models.Prescription.prescription_code == prescription_code
            )
        )
    ).first()
    return prescription

async def get_apointment(
    database: Database,
    apointment_code: str,
    user: CurrentUser,
) -> models.Apointments | None:
    """
    Get a  prescription from database
    """
    apointment = (
        await database.scalars(
            select(models.Apointments)
            .join(
                models.Institution,
                models.Institution.id == models.Apointments.institution_refrence,
            )
            .where(models.Apointments.apointment_code == apointment_code)
        )
    ).first()
    return apointment



async def get_clinical_trial(
    database: Database,
    clinical_trial_code: str,
    institution_name: str,
    user: CurrentUser,
) -> models.ClinicalTrials | None:
    """
    Get a  prescription from database
    """
    clinical_trial = (
    await database.scalars(
            select(models.ClinicalTrials)
            .join(models.Institution, models.Institution.name == institution_name)
            .where(models.ClinicalTrials.clinical_trial_code == clinical_trial_code)
            .where(
                models.Institution.organization_id.in_(
                    select(models.Organization.id).where(
                        models.Organization.path.descendant_of(user.organization.path)
                    )
                )
            )
        )
    ).first()
    return clinical_trial

async def get_image(
    database: Database,
    image_code: str,
    user: CurrentUser,
) -> models.Image | None:
    """
    Get a  prescription from database
    """
    image = (
        await database.scalars(
            select(models.Image)
            .where(models.Image.image_code == image_code)
        )
    ).first()
    return image


Clinical_Trials = Annotated[models.ClinicalTrials, Depends(get_clinical_trial)]
Apointment = Annotated[models.Apointments, Depends(get_apointment)]
Prescription = Annotated[models.Prescription, Depends(get_prescription)]
Clinician = Annotated[models.Clinician, Depends(get_clinician)]
Patient = Annotated[models.Patient, Depends(get_patient_by_code)]
Medication = Annotated[models.Medication, Depends(get_medication)]
CurrentSuperUser = Annotated[models.User, Depends(get_current_super_user)]
Institution = Annotated[models.Institution, Depends(get_institution)]
CurrentAdminUser = Annotated[models.User, Depends(get_current_admin_user)]
Image = Annotated[models.Image, Depends(get_image)]



