from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, validator
from typing_extensions import Annotated
from app.commons import FormType, GenderType, StatusType


class Person(BaseModel):
    registration_id: int
    first_name: Annotated[
        str,
        Field(
            title="Person first name",
            min_length=2,
            max_length=25,
            pattern=r"^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$",
            default="MARIA",
        ),
    ]
    last_name: Annotated[
        str,
        Field(
            title="person last name",
            min_length=2,
            max_length=25,
            pattern=r"^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$",
            default="DOE",
        ),
    ]


class Patient(Person):
    """ "class patien validates birthday"""

    __pydantic_config__ = ConfigDict(use_enum_values=True, extra="forbid")
    date_of_birth: date
    gender: object = Literal[GenderType.FEMALE.value]

    @validator("date_of_birth")
    def is_date_in_range(cls, is_valid):
        if (
            not date(year=1900, month=1, day=1)
            <= is_valid
            < date(year=2024, month=1, day=1)
        ):
            raise ValueError("Birth date must be in range")
        return is_valid


class Clinician(Person):
    pass


class ClinicianCreate(Clinician):
    pass


class PatientCreate(Patient):
    pass


class Medication(BaseModel):
    __pydantic_config__ = ConfigDict(use_enum_values=True, extra="forbid")

    medication_reference: Annotated[
        str, Field(min_length=2, max_length=25, pattern=r"[0-9]"), "Medications Code"
    ]
    code_name: Annotated[
        str, Field(min_length=2, max_length=25, pattern=r"[a-z]"), "Medications Code"
    ]
    international_code_name: Annotated[
        str, Field(min_length=2, max_length=25, pattern=r"[A-Z]"), "Code Name"
    ]
    strength_value: PositiveInt
    strenght_unit: PositiveInt
    form: object = Literal[FormType.POWDER.value]


class MedicationCreate(Medication):
    pass


class MedicationRequestBase(BaseModel):
    """class base for medication"""

    medication_request_id: int
    medication_reference: str
    reason: str
    prescription_date: datetime
    start_date: datetime
    end_date: Optional[datetime] = None
    frequency: int
    status: object= Literal[StatusType.ACTIVE.value]


class MedicationRequest(MedicationRequestBase):
    """Pydantic class used for a  medication response"""

    patient_refrence: int
    clinician_refrence: int


class MedicationRequestCreate(MedicationRequestBase):
    pass


class MedicationRequestUpdate(BaseModel):
    end_date: datetime
    frequency: int
    status: StatusType
