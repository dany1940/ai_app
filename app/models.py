from datetime import date, datetime

from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import (TEXT, Date, DateTime, Enum, Integer,
                                     SmallInteger, String)

from app.commons import Base

from .commons import FormType, GenderType, StatusType
from typing import Never
Base = declarative_base()


class Patient(Base):
    __tablename__ = "patient_tab"
    """"Table Used to create the Patient columns"""
    registration_id: Column[int] = Column(Integer, primary_key=True, autoincrement=True)
    first_name: Column[str] = Column(String, nullable=False)
    last_name: Column[str] = Column(String, nullable=False)
    date_of_birth: Column[str] = Column(Date, nullable=False) # type: ignore
    gender:Column[Never] =  Column(
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


class Clinician(Base):
    __tablename__ = "clinician_tab"
    """Table for clinician columns"""
    registration_id: Column[int ]= Column(Integer, primary_key=True, autoincrement=True)
    first_name: Column[str] = Column(String, nullable=False)
    last_name: Column[str] = Column(String, nullable=False)


class Medication(Base):
    __tablename__ = "medication_tab"
    """"table holding the Medication Columns"""
    medication_reference: Column[str] = Column(String, primary_key=True)
    code_name: Column[str] = Column(String, nullable=False)
    international_code_name: Column[str | None] = Column(String, nullable=True) # type: ignore
    strength_value: Column[int | None] = Column(SmallInteger, nullable=True) # type: ignore
    strenght_unit: Column[float | None] = Column(DOUBLE_PRECISION, nullable=True)# type: ignore
    form: Never = Column(
        Enum(
            FormType,
            validate_strings=True,
            native_enum=True,
        ),
        nullable=False,
        default=FormType.CAPSULE.value,
        server_default=FormType.CAPSULE.value,
    )# type: ignore


class MedicationRequest(Base):
    __tablename__ = "medication_request_tab"
    """table holding the medication request columns"""
    medication_request_id: Column[str] = Column(String, primary_key=True)
    clinician_refrence: Column[int] = Column(
        Integer, ForeignKey("clinician_tab.registration_id")
    )
    patient_refrence: Column[int] = Column(Integer, ForeignKey("patient_tab.registration_id"))
    medication_reference: Column[str] = Column(
        String, ForeignKey("medication_tab.medication_reference")
    )
    reason: Column[date | None] = Column(TEXT, nullable=True)# type: ignore
    prescription_date: Column[datetime] = Column(DateTime, nullable=False)
    start_date: Column[datetime] = Column(DateTime, nullable=False)
    end_date: Column[datetime | None] = Column(DateTime, nullable=True)# type: ignore
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
    )# type: ignore
