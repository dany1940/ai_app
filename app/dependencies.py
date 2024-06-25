from typing import Annotated, cast, Literal
from datetime import date
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import and_, create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, joinedload
from pydantic import validator
from app import models, schemas
from app.conf import config
from app.security import verify_password
from app.commons import FormType

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


SQLALCHEMY_DATABASE_URL = f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"
load_dotenv()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
)


Base = declarative_base()


def get_db():
    """
    Acquire database connection from the pool.
    """

    with Session(bind=engine) as database:
        yield database


Database = Annotated[Session, Depends(get_db)]


def get_patient(
    database: Database,
    first_name: str,
    last_name: str,
    date_of_birth: str,
) -> models.Patient | None:
    """
    Get a  patient from database
    """
    @validator("date_of_birth")
    def is_date_in_range(is_valid):
        if (
            not date(year=1900, month=1, day=1)
            <= is_valid
            < date(year=2024, month=1, day=1)
        ):
            raise ValueError("Birth date must be in range")
        else:

           return (
            database.execute(
            select(models.Patient).where(
                and_(
                    models.Patient.first_name == first_name,
                    models.Patient.last_name == last_name,
                    models.Patient.date_of_birth == date_of_birth,
                )
            )
        )
        .unique()
        .scalar_one_or_none()
    )


def get_clinician(
    database: Database,
    first_name: str,
    last_name: str,
    email: str,
) -> models.Clinician | None:
    """
    Get a  clinician from database
    """

    return (
        database.execute(
            select(models.Clinician).where(
                and_(
                    models.Clinician.first_name == first_name,
                    models.Clinician.last_name == last_name,
                    models.Clinician.email == email,
                )
            )
        )
        .unique()
        .scalar_one_or_none()
    )


def get_medication(
    database: Database,
    brand_name: str,
    medication_name: str,
    form: object = Literal[FormType.POWDER.value],
) -> models.Medication | None:
    """
    Get a  patient from database
    """

    return (
        database.execute(
            select(models.Medication).where(
                and_(
                    models.Medication.medication_name == medication_name,
                    models.Medication.brand_name == brand_name,
                    models.Medication.form == form,
                )
            )
        )
        .unique()
        .scalar_one_or_none()
    )


def get_medication_by_id(
    database: Database,
    patient_refrence: int,
) -> models.Medication | None:
    return (
        database.execute(
            select(models.Patient).where(
                and_(models.Patient.registration_id == patient_refrence)
            )
        )
        .unique()
        .scalar_one_or_none()
    )


def get_clinician_by_id(
    database: Database,
    registration_id: int,
) -> models.Clinician | None:
    return (
        database.execute(
            select(models.Clinician).where(
                and_(models.Clinician.registration_id == registration_id)
            )
        )
        .unique()
        .scalar_one_or_none()
    )


def get_medication_request_by_id(
    database: Database,
    medication_request_id: str,
) -> models.MedicationRequest | None:
    return (
        database.execute(
            select(models.MedicationRequest).where(
                and_(
                    models.MedicationRequest.medication_request_id
                    == medication_request_id
                )
            )
        )
        .unique()
        .scalar_one_or_none()
    )


def get_contact(
    database: Database,
    contact: schemas.ContactCreate,
) -> models.Contact | None:
    """
    Get a  contact from database
    """

    return (
        database.execute(
            select(models.Contact).where(
                and_(
                    models.Contact.contact == contact.contact,
                    models.Contact.contact_name == contact.contact_name,
                    models.Contact.institution_id == contact.institution_id,
                )
            )
        )
        .unique()
        .scalar_one_or_none()
    )


def get_organization() -> models.Organization | None:
    """
    Get a  organization from database
    """
    pass


def get_image(
    database: Database,
    image: schemas.Image,
) -> models.Image | None:
    """
    Get a  image from database
    """

    return (
        database.execute(
            select(models.Image).where(
                and_(
                    models.Image.image_name == image.image_name,
                )
            )
        )
        .unique()
        .scalar_one_or_none()
    )


def authenticate_user(database: Database, username: str, password: str):
    user: models.User | None = (
        database.query(models.User).filter(models.User.username == username).first()
    )
    if user is None:
        return None
    if not verify_password(password, cast(str, user.pword_hash)):
        return None
    return user


def user_from_token(
    token: str,
    database: Database,
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
    user = (
        database.query(models.User)
        .filter(models.User.username == username)
        .join(models.User.organization)
        .options(joinedload(models.User.organization))
        .first()
    )
    if user is None:
        raise credentials_exception
    return user


def get_current_user(
    database: Database,
    token: str = Depends(oauth2_scheme),
):
    """
    Validate the user's JWT token.

    If the token is valid, return the currently logged in user.
    If the token is invalid, raise a 401 (Unauthorized) exception.
    """
    return user_from_token(token, database)


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


CurrentSuperUser = Annotated[models.User, Depends(get_current_super_user)]


def get_institution(
    database: Database, name: str, user: CurrentUser
) -> models.Institution | None:
    """
    Get a  institution from database
    """

    return (
        database.execute(
            select(models.Institution)
            .where(models.Institution.name == name)
            .where(
                Institution.organization_id.in_(
                    select(models.Organization.id).where(
                        models.Organization.path.descendant_of(user.organization.path)
                    )
                )
            )
        )
        .unique()
        .scalar_one_or_none()
    )


CurrentAdminUser = Annotated[models.User, Depends(get_current_admin_user)]
Image = Annotated[models.Image, Depends(get_image)]
Organisation = Annotated[models.Organization, Depends(get_institution)]
Contact = Annotated[models.Contact, Depends(get_contact)]
Institution = Annotated[models.Institution, Depends(get_institution)]
Medication = Annotated[models.Medication, Depends(get_medication)]
Clinician = Annotated[models.Clinician, Depends(get_clinician)]
Patient = Annotated[models.Patient, Depends(get_patient)]
MedicationById = Annotated[models.Medication, Depends(get_medication_by_id)]
ClinicianById = Annotated[models.Clinician, Depends(get_clinician_by_id)]
MedicationRequestById = Annotated[
    models.MedicationRequest, Depends(get_medication_request_by_id)
]
