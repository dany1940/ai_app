from pydantic import Field
from pydantic import (ConfigDict, BaseModel, PositiveInt, validator)
from typing import Literal, Optional
from typing_extensions import Annotated
from app.commons import GenderType, StatusType, FormType
from datetime import date, datetime

class Person(BaseModel):
    registration_id: int
    first_name: Annotated[str, Field(title="Person first name", min_length=2, max_length=25, pattern=r"[a-zA-Z]", default="MARIA")]
    last_name: Annotated[str, Field(title="person last name", min_length=2, max_length=25, pattern=r"[a-zA-Z]", default="DOE")]



class Patient(Person):
   __pydantic_config__ = ConfigDict(use_enum_values=True, extra="forbid")
   date_of_birth: date
   gender: GenderType = Literal[GenderType.FEMALE.value]
   @validator("date_of_birth")
   def is_date_in_range(cls, is_valid):
        if not date(year=1900, month=1, day=1) <= is_valid < date(year=2024, month=1, day=1):
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

    code: Annotated[str, Field(min_length=2, max_length=25, pattern=r"[0-9]"), "Medications Code"]
    code_name: Annotated[str, Field(min_length=2, max_length=25, pattern=r"[a-z]"), "Medications Code" ]
    international_code_name: Annotated[str, Field(min_length=2, max_length=25, pattern=r"[A-Z]"), "Code Name"]
    strength_value: PositiveInt
    strenght_unit: PositiveInt
    form: FormType = Literal[FormType.POWDER.value]


class MedicationCreate(Medication):
    pass


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
  status: StatusType = Literal[StatusType.ACTIVE.value]








