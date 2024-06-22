from datetime import date, datetime
from typing import Literal, Optional

from pydantic import (BaseModel, ConfigDict, EmailStr, Field, PositiveInt,
                      validator)
from typing_extensions import Annotated

from app.commons import (BloodGroupType, FormType, GenderType, StatusType,
                         TitleType)


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
    address: Annotated[
        str,
        Field(
            title="person address",
            min_length=2,
            max_length=25,
            pattern=r"^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$",
            default="1234 Main St",
        ),
    ]
    created_on: datetime
    updated_on: datetime
    mobile_number: str
    email: EmailStr


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

    is_smoker: bool
    is_active: bool
    is_armed_forces: bool
    is_from_emergency_services: bool
    is_from_abroad: bool
    is_from_nhs: bool
    emergency_contact_number: bool
    is_donor: bool
    donor_organ: str
    is_blood_donor: bool
    patient_medical_history: str
    blood_type: BloodGroupType = Literal[BloodGroupType.A_POSITIVE.value]
    title: TitleType
    Is_alcohool_drinker: bool
    institution_number: str


class PatientCreate(Patient):
    pass


class Image(BaseModel):

    image_id: int
    link: str
    created_on: datetime


class Clinician(Person):
    gmc_number: str
    mc_number: str
    password: str
    about: str
    profile_picture: Image
    rating: float
    online_consultation: bool
    online_consultation_fee: float
    online_consultation_duration: int


class ClinicianCreate(Clinician):
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
    brand_name: str
    active_ingredient_name: str
    excipient_name: str
    other_name_of_active_ingredient: str
    abbreviated_name_of_active_ingredient: str
    abbreviated_name_of_active_ingredient: str
    chemical_formula: str
    peculiar_part_of_drug: str
    color: str
    smell: str
    taste: str
    usage_of_excipient: str
    indications: str
    contraindications: str
    is_allowed_for_children: str
    medication_category: str
    medication_sub_category: str
    medication_type: str
    frequency: int
    dosage: str
    side_effects: str
    storage: str
    medication_image: int
    image: Image
    is_fda_approved: bool
    is_nhs_approved: bool
    is_emergency_medicine: bool
    is_controlled_drug: bool
    is_generic: bool
    is_over_the_counter: bool
    is_herbal: bool
    is_homeopathic: bool
    is_banned: bool
    is_restricted: bool
    is_unlicensed: bool
    is_orphan_drug: bool
    is_biological: bool
    is_trial_drug: bool
    is_medical_gas: bool
    is_medical_radioisotope: bool
    is_medical_radioactive: bool


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
    status: object = Literal[StatusType.ACTIVE.value]


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


class Institution(BaseModel):
    id: int
    name: str
    created_on: datetime
    contact_number: str
    organization_id: int
    notes: str
    clinician_id: int


class InstitutionCreate(Institution):
    pass


class Organization(BaseModel):

    id: int
    name: str
    created_on: datetime
    institution_id: int
    address: str
    email: str
    telephone: str
    profile_picture_id: int
    url: str


class OrganizationCreate(Organization):
    pass


class UserBase(BaseModel):
    # Shared properties
    email: EmailStr
    firstname: str | None = None
    lastname: str | None = None


class User(BaseModel):
    # Additional properties to return

    model_config = ConfigDict(from_attributes=True)
    username: str
    email: EmailStr
    firstname: str | None
    lastname: str | None


class UserUpdate(UserBase):
    # Properties to receive via API on update
    username: str


class UserInDB(User):
    # Additional properties stored in database
    username: str
    organization_id: int
    hashed_password: str
    can_edit: bool


class Contact(BaseModel):
    contact: str
    contact_name: str
    institution_id: int


class ContactCreate(Contact):
    pass


class UserCreate(BaseModel):
    """
    Properties to receive on user creation.
    """

    password: str
    email: EmailStr
    firstname: str | None = None
    lastname: str | None = None
    is_admin: bool = False
    organization_name: str | None = None


class UserPasswordUpdate(BaseModel):
    """
    Properties to receive on user password update.
    """

    old_password: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str
