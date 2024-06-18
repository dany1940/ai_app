from sqlmodel import Field, Relationship, SQLModel, EmailStr
from pydantic import (Date, ConfigDict, BaseModel, PositiveInt, Optional)
from typing import Literal
from typing_extensions import Annotated




class GenderType(Enum):
    MALE = "Male"
    FEMALE = "Female"


class FormType(Enum):
    POWDER: "Powder"
    TABLET: "Tablet"
    CAPSULE: "Capsule"
    SYRUP: "Syrup"

class StatusType(Enum):
    ACTIVE: "Active"
    ON-HOLD: "On-Hold"
    CANCELLED: "Cancelled"
    COMPLETED: "Completed"

class Person(BaseModel):
    registration_id: int
    first_name: Annotated[str, Field(title="Person first name", min_length=2, max_length=25, pattern=r"/[a-zA-Z]+/g")]
    last_name: Annotated[str, Field(title="person last name", min_length=2, max_length=25, pattern=r"/[a-zA-Z]+/g")]

class Patient(Person):
   __pydantic_config__ = ConfigDict(use_enum_values=True, extra="forbid")
   date_of_birth: datetime
   sex: SexType = Literal[GenderType.MAN]
   @validator("date_of_birth")
    def is_date_in_range(cls, is_valid):
        if not datetime(year=1900, month=1, day=1) <= is_valid < datetime(year=2024, month=1, day=1):
            raise ValueError("Birth date must be in range")
        return is_valid


class Clinician(Person):
    pass


class Medication(BaseModel):
    __pydantic_config__ = ConfigDict(use_enum_values=True, extra="forbid")

    code: Annotated[str, title ="Medications Code" ,Field(min_length=2, max_length=25, pattern=r"/[0-9]+/g")]
    code_name: Annotated[str, title="Medication code name", Field(min_length=2, max_length=25, pattern=r"/[a-z]+/g")]
    international_code_name: Annotated[str, title="Code Name", Field(min_length=2, max_length=25, pattern=r"/[A-Z]+/g")]
    strenght_value: PositiveInt
    strenght_unit: PositiveInt
    form: Form = Literal(Form.POWDER)


class MedicationRequest(BaseModel):
  patient_refrence: int
  clinician_refrence: int
  medication_refrence: str
  reason:  str
  prescribed_date: datetime
  start_date:  datetime
  end_date: Optional[datetime] = None
  frequency: int
  status: Literal[StatusType.ACTIVE]



class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None



class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool
    items: list["Item"] = Relationship(back_populates="owner")




class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(SQLModel):
    sub: int | None = None

class NewPassword(BaseModel):
    new_password: str
    token: str

class UserCreate(UserBase):
    password: str


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

class UserUpdate(UserBase):
    email: EmailStr
    full_name: str | None = None

class UserUpdateMe(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None

class UpdatePassword(BaseModel):
    current_password: str
    new_password: str


class UserPublic(UserBase):
    id: int
class UserPublic(BaseModel):
    data: list[UserPublic]





