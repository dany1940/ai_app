from pydantic import Field
from pydantic import (ConfigDict, BaseModel, PositiveInt, validator)
from typing import Literal, Optional
from typing_extensions import Annotated
from app.commons import GenderType, StatusType, FormType
from datetime import datetime

class Person(BaseModel):
    registration_id: int
    first_name: Annotated[str, Field(title="Person first name", min_length=2, max_length=25, pattern=r"/[a-zA-Z]+/g")]
    last_name: Annotated[str, Field(title="person last name", min_length=2, max_length=25, pattern=r"/[a-zA-Z]+/g")]

class Patient(Person):
   __pydantic_config__ = ConfigDict(use_enum_values=True, extra="forbid")
   date_of_birth: datetime
   gender: Literal[GenderType.MALE]
   @validator("date_of_birth")
   def is_date_in_range(cls, is_valid):
        if not datetime(year=1900, month=1, day=1) <= is_valid < datetime(year=2024, month=1, day=1):
            raise ValueError("Birth date must be in range")
        return is_valid


class Clinician(Person):
    pass

class PatientCreate(BaseModel):
    pass

class Medication(BaseModel):
    __pydantic_config__ = ConfigDict(use_enum_values=True, extra="forbid")

    code: Annotated[str, Field(min_length=2, max_length=25, pattern=r"/[0-9]+/g"), "Medications Code"]
    code_name: Annotated[str, Field(min_length=2, max_length=25, pattern=r"/[a-z]+/g"), "Medications Code" ]
    international_code_name: Annotated[str, Field(min_length=2, max_length=25, pattern=r"/[A-Z]+/g"), "Code Name"]
    strenght_value: PositiveInt
    strenght_unit: PositiveInt
    form: Literal[FormType.POWDER]


class MedicationRequest(BaseModel):
  meddication_request_id: int
  patient_refrence: int
  clinician_refrence: int
  medication_refrence: str
  reason:  str
  prescribed_date: datetime
  start_date:  datetime
  end_date: Optional[datetime] = None
  frequency: int
  status: Literal[StatusType.ACTIVE]








