from datetime import date, datetime
from typing import Never

from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey, Identity
from sqlalchemy.sql.sqltypes import (TEXT, Boolean, Date, DateTime, Enum,
                                     Integer, SmallInteger, String)

from app.commons import Base

from .commons import (BloodGroupType, FormType, GenderType, StatusType,
                      TitleType)

Base = declarative_base()


class Patient(Base):
    __tablename__ = "patient_tab"
    """"Table Used to create the Patient columns"""
    registration_id: Column[int] = Column(Integer, primary_key=True, autoincrement=True)
    first_name: Column[str] = Column(String, nullable=False)
    last_name: Column[str] = Column(String, nullable=False)
    date_of_birth: Column[str] = Column(Date, nullable=False)  # type: ignore
    address: Column[str] = Column(String, nullable=False)
    is_smoker: Column[bool] = Column(Boolean, nullable=True)
    created_on: Column[datetime] = Column(DateTime, nullable=False)
    updated_on: Column[datetime] = Column(DateTime, nullable=False)
    is_active: Column[bool] = Column(Boolean, nullable=False)
    is_armed_forces: Column[bool] = Column(Boolean, nullable=False)
    is_from_emergency_services: Column[bool] = Column(Boolean, nullable=False)
    is_from_abroad: Column[bool | None] = Column(Boolean, nullable=False)
    is_from_nhs: Column[bool | None] = Column(Boolean, nullable=False)
    emergency_contact_number: Column[str] = Column(String, nullable=False)
    is_donor: Column[bool] = Column(Boolean, nullable=True)
    donor_organ: Column[str] = Column(String, nullable=True)
    is_blood_donor: Column[bool] = Column(Boolean, nullable=True)
    patient_medical_history: Column[TEXT] = Column(TEXT, nullable=True)
    blood_type: Column[Never] = Column(
        Enum(
            BloodGroupType,
            name="BloodGroupType",
            validate_strings=True,
            native_enum=True,
        ),
        nullable=False,
        server_default=BloodGroupType.A_POSITIVE.value,
        default=BloodGroupType.A_POSITIVE.value,
    )

    gender: Column[Never] = Column(
        Enum(
            GenderType,
            name="GenderType",
            validate_strings=True,
            native_enum=True,
        ),
        nullable=False,
        server_default=GenderType.FEMALE.value,
        default=GenderType.FEMALE.value,
    )
    title: Column[Never] = Column(
        Enum(
            TitleType,
            name="TytleType",
            validate_strings=True,
            native_enum=True,
        ),
        nullable=False,
        server_default=TitleType.MR.value,
        default=TitleType.MR.value,
    )
    is_alcohool_drinker: Column[bool] = Column(Boolean, nullable=False)
    institution_number: Column[str] = Column(Integer, ForeignKey("institution_tab.id"))


class Clinician(Base):
    __tablename__ = "clinician_tab"
    """Table for clinician columns"""
    registration_id: Column[int] = Column(Integer, primary_key=True, autoincrement=True)
    gmc_number: Column[str] = Column(String, nullable=False)
    first_name: Column[str] = Column(String, nullable=False)
    last_name: Column[str] = Column(String, nullable=False)

    mobile_number: Column[str] = Column(String, nullable=False)
    email: Column[str] = Column(String, nullable=False)
    password: Column[str] = Column(String, nullable=False)
    mc_number: Column[str] = Column(String, nullable=False)
    address: Column[str] = Column(String, nullable=False)
    about: Column[str] = Column(TEXT, nullable=True)
    profile_picture = relationship("Image", uselist=False)

    created_on: Column[datetime] = Column(DateTime, nullable=False)
    updated_on: Column[datetime] = Column(DateTime, nullable=False)
    rating: Column[float] = Column(DOUBLE_PRECISION, nullable=True)
    online_consultation: Column[bool] = Column(Boolean, nullable=True)
    online_consultation_fee: Column[float] = Column(DOUBLE_PRECISION, nullable=True)
    online_consultation_duration: Column[int] = Column(SmallInteger, nullable=True)


class Medication(Base):
    __tablename__ = "medication_tab"
    """"table holding the Medication Columns"""
    medication_reference: Column[str] = Column(String, primary_key=True)
    code_name: Column[str] = Column(String, nullable=False)
    international_code_name: Column[str | None] = Column(String, nullable=True)  # type: ignore
    strength_value: Column[int | None] = Column(SmallInteger, nullable=True)  # type: ignore
    strenght_unit: Column[float | None] = Column(DOUBLE_PRECISION, nullable=True)  # type: ignore
    form: Never = Column(
        Enum(
            FormType,
            validate_strings=True,
            native_enum=True,
        ),
        nullable=False,
        default=FormType.CAPSULE.value,
        server_default=FormType.CAPSULE.value,
    )  # type: ignore
    brand_name: Column[str] = Column(String, nullable=False)
    active_ingredient_name: Column[str] = Column(String, nullable=False)
    excipient_name: Column[str] = Column(String, nullable=False)
    other_name_of_active_ingredient: Column[str] = Column(String, nullable=False)
    abbreviated_name_of_active_ingredient: Column[str] = Column(String, nullable=False)
    abbreviated_name_of_active_ingredient: Column[str] = Column(String, nullable=False)
    chemical_formula: Column[str] = Column(String, nullable=False)
    peculiar_part_of_drug: Column[str] = Column(String, nullable=False)
    color: Column[str] = Column(String, nullable=False)
    smell: Column[str] = Column(String, nullable=False)
    taste: Column[str] = Column(String, nullable=False)
    usage_of_excipient: Column[str] = Column(String, nullable=False)
    indications: Column[str] = Column(String, nullable=False)
    contraindications: Column[str] = Column(String, nullable=False)
    is_allowed_for_children: Column[bool] = Column(Boolean, nullable=False)
    medication_category: Column[str] = Column(String, nullable=False)
    medication_sub_category: Column[str] = Column(String, nullable=False)
    medication_type: Column[str] = Column(String, nullable=False)
    frequency: Column[int] = Column(SmallInteger, nullable=False)
    dosage: Column[str] = Column(String, nullable=False)
    side_effects: Column[str] = Column(String, nullable=False)
    storage: Column[str] = Column(String, nullable=False)
    medication_image: Column[int] = Column(Integer, ForeignKey("image_tab.image_id"))
    image = relationship("Image", uselist=False)
    is_fda_approved: Column[bool] = Column(Boolean, nullable=False)
    is_nhs_approved: Column[bool] = Column(Boolean, nullable=False)
    is_emergency_medicine: Column[bool] = Column(Boolean, nullable=False)
    is_controlled_drug: Column[bool] = Column(Boolean, nullable=False)
    is_generic: Column[bool] = Column(Boolean, nullable=False)
    is_over_the_counter: Column[bool] = Column(Boolean, nullable=False)
    is_herbal: Column[bool] = Column(Boolean, nullable=False)
    is_homeopathic: Column[bool] = Column(Boolean, nullable=False)
    is_banned: Column[bool] = Column(Boolean, nullable=False)
    is_restricted: Column[bool] = Column(Boolean, nullable=False)
    is_unlicensed: Column[bool] = Column(Boolean, nullable=False)
    is_orphan_drug: Column[bool] = Column(Boolean, nullable=False)
    is_biological: Column[bool] = Column(Boolean, nullable=False)
    is_trial_drug: Column[bool] = Column(Boolean, nullable=False)
    is_medical_gas: Column[bool] = Column(Boolean, nullable=False)
    is_medical_radioisotope: Column[bool] = Column(Boolean, nullable=False)
    is_medical_radioactive: Column[bool] = Column(Boolean, nullable=False)


class MedicationRequest(Base):
    __tablename__ = "medication_request_tab"
    """table holding the medication request columns"""
    medication_request_id: Column[str] = Column(String, primary_key=True)
    clinician_refrence: Column[int] = Column(
        Integer, ForeignKey("clinician_tab.registration_id")
    )
    patient_refrence: Column[int] = Column(
        Integer, ForeignKey("patient_tab.registration_id")
    )
    reason: Column[date | None] = Column(TEXT, nullable=True)  # type: ignore
    prescription_date: Column[datetime] = Column(DateTime, nullable=False)
    start_date: Column[datetime] = Column(DateTime, nullable=False)
    end_date: Column[datetime | None] = Column(DateTime, nullable=True)  # type: ignore
    frequency: Column[int] = Column(SmallInteger, nullable=False)
    status: Never = Column(
        Enum(
            StatusType,
            name="status",
            validate_strings=True,
            native_enum=True,
        ),
        nullable=False,
        default=StatusType.ACTIVE.value,
        server_default=StatusType.ACTIVE.value,
    )  # type: ignore


class Image(Base):
    __tablename__ = "image_tab"

    image_id = Column(Integer, Identity(always=True), primary_key=True)
    link = Column(String, nullable=False)
    created_on = Column(DateTime(timezone=False), nullable=False)


class Organization(Base):
    __tablename__ = "organization_tab"

    id = Column(Integer, Identity(always=True), primary_key=True)
    name = Column(String, nullable=False, unique=True)
    created_on = Column(DateTime(timezone=False), nullable=False, unique=False)
    address = Column(String, nullable=True)
    email = Column(String, nullable=True)
    telephone = Column(String, nullable=True)
    institution_id = Column(Integer, ForeignKey("institution_tab.id"), nullable=True)
    profile_picture_id = Column(
        Integer,
        ForeignKey("image_tab.image_id"),
        nullable=True,
    )
    url = Column(String, nullable=True)

    def __repr__(self) -> str:
        return f"Organization(name={self.name})"


class Institution(Base):
    __tablename__ = "institution_tab"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    created_on = Column(DateTime, nullable=False)
    contact_number: Column[String] = Column(String(255), nullable=True)

    notes: Column[TEXT] = Column(TEXT, nullable=True)
    clinician_id: Column[Integer] = Column(
        Integer, ForeignKey("clinician_tab.registration_id"), nullable=True
    )

    def __repr__(self) -> str:
        return f"Institution(id={self.id}, name={self.name})"


class User(Base):
    __tablename__ = "user_tab"

    id: int = Column(Integer, Identity(always=True), primary_key=True)
    username: str = Column(String, nullable=False, unique=True)
    email: str = Column(String, nullable=False, unique=True)
    pword_hash: str = Column(String, nullable=False)
    firstname: str | None = Column(String, nullable=True)
    lastname: str | None = Column(String, nullable=True)
    can_edit: bool = Column(
        Boolean, default=False, server_default="false", nullable=False
    )
    organization_id = Column(Integer, ForeignKey("organization_tab.id"), nullable=True)

    def __repr__(self) -> str:
        return f"User(email={self.email}, organization={self.organization_id})"


class Contact(Base):
    """
    Table representing an email contact for an institution.
    """

    __tablename__ = "contact_tab"
    contact = Column(TEXT, primary_key=True)
    contact_name = Column(TEXT, nullable=False)

    institution_id = Column(Integer, ForeignKey("institution_tab.id"), primary_key=True)
