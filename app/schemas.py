from datetime import date, datetime
from typing import List, Literal, Optional

from pydantic import (BaseModel, ConfigDict, EmailStr, Field, PositiveInt,
                      validator)
from typing_extensions import Annotated

from app.commons import (BloodGroupType, FormType, GenderType, StatusType,
                         TitleType, PrescriptionStatusType)


class Person(BaseModel):
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




class PatientCreate(BaseModel):
    """ "class patien validates birthday"""

    __pydantic_config__ = ConfigDict(use_enum_values=True)

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
    date_of_birth: Annotated[
        datetime,
        Field(
            title="Date of birth",
            description="The date of birth of the patient",
            example="2021-08-31",
            default_factory=datetime.now,
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
    ] | None = None


    gender: object = Literal[GenderType.FEMALE.value]
    is_smoker: bool | None = None
    is_active: bool | None = None
    is_armed_forces: bool | None = None
    is_from_emergency_services: bool | None = None
    is_from_abroad: bool | None = None
    is_from_nhs: bool | None = None
    emergency_contact_number: bool | None = None
    is_donor: bool  | None = None
    donor_organ: str | None = None
    is_blood_donor: bool | None = None
    patient_medical_history: str  | None = None
    blood_type: BloodGroupType = Literal[BloodGroupType.A_POSITIVE.value]
    title: TitleType | None = None
    is_alcohool_drinker: bool | None = None
    institution_name: str
    clinician_code: str


class Image(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    link: str
    created_on: datetime
    clinician_id: int


class ImageCreate(Image):
    pass


class Clinician(Person):

    model_config = ConfigDict(from_attributes=True)

    gmc_number: str
    mc_number: str
    password: str
    about: str
    rating: float
    online_consultation: bool
    online_consultation_fee: float
    online_consultation_duration: int


class UserOverview(BaseModel):
    """
    Properties containing the overview of a user without returning all fields.
    """

    model_config = ConfigDict(from_attributes=True)

    username: str
    firstname: str | None = None
    lastname: str | None = None
    organization_name: str
    is_admin: bool
    email: str


class ClinicianCreate(BaseModel):
    address: Annotated[
        str,
        Field(
            title="person address",
            min_length=2,
            max_length=25,
            pattern=r"^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$",
            default="1234 Main St",
        ),
    ] | None = None
    email: str
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
    gmc_number: str | None = None
    mc_number: str | None = None
    password: str  | None = None
    about: str      | None = None
    rating: float   | None = None
    mobile_number: str | None = None
    online_consultation: bool   | None = None
    online_consultation_fee: float  | None = None
    online_consultation_duration: int  | None = None
    institution_name: str


class Medication(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    medication_reference: Annotated[
        str, Field(min_length=2, max_length=25, pattern=r"[0-9]"), "Medications Code"
    ]
    code_name: Annotated[
        str, Field(min_length=2, max_length=25, pattern=r"[a-z]"), "Medications Code"
    ]
    international_code_name: Annotated[
        str, Field(min_length=2, max_length=25, pattern=r"[A-Z]"), "Code Name"
    ]
    strength_value: PositiveInt | None = None
    strenght_unit: PositiveInt  |   None = None
    form: object = Literal[FormType.POWDER.value]
    brand_name: str | None = None
    active_ingredient_name: str | None = None
    excipient_name: str | None = None
    other_name_of_active_ingredient: str | None = None
    abbreviated_name_of_active_ingredient: str | None = None
    abbreviated_name_of_active_ingredient: str | None = None
    chemical_formula: str | None = None
    peculiar_part_of_drug: str | None = None
    color: str | None = None
    smell: str | None = None
    taste: str | None = None
    usage_of_excipient: str | None = None
    indications: str | None = None
    contraindications: str | None = None
    is_allowed_for_children: str | None = None
    medication_category: str | None = None
    medication_sub_category: str | None = None
    medication_type: str | None = None
    frequency: int | None = None
    dosage: str  | None = None
    side_effects: str | None = None
    storage: str | None = None
    medication_image: int | None = None
    image: Image | None = None
    is_fda_approved: bool | None = None
    is_nhs_approved: bool | None = None
    is_emergency_medicine: bool | None = None
    is_controlled_drug: bool | None = None
    is_generic: bool | None = None
    is_over_the_counter: bool | None = None
    is_herbal: bool | None = None
    is_homeopathic: bool | None = None
    is_banned: bool | None = None
    is_restricted: bool | None = None
    is_unlicensed: bool | None = None
    is_orphan_drug: bool | None = None
    is_biological: bool  | None = None
    is_trial_drug: bool  | None = None
    is_medical_gas: bool  | None = None
    is_medical_radioisotope: bool  | None = None
    is_medical_radioactive: bool   | None = None


class MedicationCreate(BaseModel):

    medication_reference: Annotated[
        str, Field(min_length=2, max_length=25, pattern=r"[0-9]"), "Medications Code"
    ]
    code_name: Annotated[
        str, Field(min_length=2, max_length=25, pattern=r"[a-z]"), "Medications Code"
    ]
    international_code_name: Annotated[
        str, Field(min_length=2, max_length=25, pattern=r"[A-Z]"), "Code Name"
    ]



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


class InstitutionBase(BaseModel):
    id: int
    name: str


class Institution(InstitutionBase):
    created_on: datetime
    contact_number: str
    organization_id: int
    notes: str
    clinician: List[Clinician]

class InstitutionCreate(BaseModel):
    contact_number: str | None = None
    organization_name: str | None = None
    notes: str | None = None


class Organization(BaseModel):
    name: str
    created_on: datetime
    address: str
    email: str
    telephone: str
    profile_picture_id: int
    url: str
    path: str


class OrganizationCreate(BaseModel):
    parent: str | None
    email: str | None = None
    url: str   | None = None


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


class Prescription(BaseModel):
    prescription_id: str
    reason: str
    prescription_date: datetime
    start_date: datetime
    end_date: Optional[datetime] = None
    frequency: int
    prescription_status: object = Literal[PrescriptionStatusType.ACTIVE.value]



class PrescriptionCreate(BaseModel):
    reason: str
    start_date: datetime
    end_date: Optional[datetime] = None
    frequency: int
    prescription_status: object = Literal[PrescriptionStatusType.ACTIVE.value]


class Apointments(BaseModel):
    reason: str
    apointment_date: datetime




class ApointmentsCreate(BaseModel):
    reason: str
    apointment_date: datetime



class ClinicalTrial(BaseModel):
    reason: str




class ClinicalTrialCreate(BaseModel):
    reason: str

class GetClinician(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
    email: str
class GetMedication(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code_name: str
    form: object = Literal[FormType.POWDER.value]
    indications: str
    dosage: str

class GetPrescription(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reason: str
    prescription_date: datetime
    start_date: datetime
    end_date: Optional[datetime] = None
    frequency: int
    prescription_status: object = Literal[PrescriptionStatusType.ACTIVE.value]
    clinician: GetClinician
    medication: GetMedication
