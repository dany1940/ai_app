from typing import Annotated, cast, Literal
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import and_, create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, joinedload
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


def get_patient_by_code(
    database: Database,
    patient_code: str,
) -> models.Patient | None:
    """
    Get a  patient from database
    """

    return (
        database.execute(
            select(models.Patient).where(
                and_(
                    models.Patient.patient_code == patient_code,
                )
            )
        )
        .unique()
        .scalar_one_or_none()
    )


def get_clinician(
    database: Database,
    clinician_code: str,
) -> models.Clinician | None:
    """
    Get a  clinician from database
    """

    return (
        database.execute(
            select(models.Clinician).where(
                and_(
                    models.Clinician.clinician_code == clinician_code,
                )
            )
        )
        .unique()
        .scalar_one_or_none()
    )


def get_medication(
    database: Database,
    medication_code: str,
) -> models.Medication | None:
    """
    Get a  patient from database
    """

    return (
        database.execute(
            select(models.Medication).where(
                and_(
                    models.Medication.code_name == medication_code,
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
    database: Database, institution_name: str,  user: CurrentUser
) -> models.Institution | None:
    """
    Get a  institution from database
    """

    return (
        database.execute(
            select(models.Institution)
            .where(models.Institution.name == institution_name)
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
Patient = Annotated[models.Patient, Depends(get_patient_by_code)]
Clinician = Annotated[models.Clinician, Depends(get_clinician)]

def get_prescription(
  database: Database,
  prescription_code: str,
  user: CurrentUser,

) -> models.Prescription | None:
    """
    Get a  prescription from database
    """
    return (
            database.execute(
            select(models.Prescription.prescription_code)

        .where(
            models.Prescription.prescription_code == prescription_code
        )
            )
        .unique()
        .scalar_one_or_none()

    )

Institution = Annotated[models.Institution, Depends(get_institution)]

def get_apointment(
  database: Database,
  apointment_code: str,
  user: CurrentUser,

) -> models.Apointments | None:
    """
    Get a  prescription from database
    """
    return (
            database.execute(
            select(models.Apointments)
            .join(models.Institution, models.Institution.id == models.Apointments.institution_refrence)
            .where(models.Apointments.apointment_code == apointment_code)
            .where(
                models.Institution.organization_id.in_(
                    select(models.Organization.id).where(
                        models.Organization.path.descendant_of(user.organization.path)
                    )
                )
        )

    ) .unique()
        .scalar_one_or_none()
    )
def get_clinical_trial(
  database: Database,
  clinical_trial_code: str,
  institution_name: str,
  user: CurrentUser,

) -> models.ClinicalTrials | None:
    """
    Get a  prescription from database
    """
    return (
            database.execute(
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

    ) .unique()
        .scalar_one_or_none()
    )


ClinicalTrial = Annotated[models.ClinicalTrials, Depends(get_clinical_trial)]
Apointment = Annotated[models.Apointments, Depends(get_apointment)]
Prescription = Annotated[models.Prescription, Depends(get_prescription)]
CurrentAdminUser = Annotated[models.User, Depends(get_current_admin_user)]
Image = Annotated[models.Image, Depends(get_image)]
Organisation = Annotated[models.Organization, Depends(get_institution)]
Contact = Annotated[models.Contact, Depends(get_contact)]

Medication = Annotated[models.Medication, Depends(get_medication)]
MedicationById = Annotated[models.Medication, Depends(get_medication_by_id)]
ClinicianById = Annotated[models.Clinician, Depends(get_clinician_by_id)]
