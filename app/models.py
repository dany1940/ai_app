from datetime import datetime
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.schema import Column
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.sql.sqltypes import TEXT
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.sql.sqltypes import Integer
from sqlalchemy.sql.sqltypes import SmallInteger
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.sqltypes import Enum
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from app.dependencies import Base
from datetime import date
from .commons import StatusType, FormType, GenderType


Base = declarative_base()

class Patient(Base):
    __tablename__ = "patient"

    patient_id: int = Column(Integer, primary_key=True, autoincrement=True)
    first_name: str = Column(String, nullable=False)
    last_name: str = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender : str = Column(
        Enum(
            GenderType,
            name="gender",
            validate_strings=True,
            native_enum=True,
        ),
        nullable=False,
        default=GenderType.FEMALE.value,
        server_default=GenderType.FEMALE.value,
    )


class Clinician(Base):
    __tablename__ = "clinician"

    registration_id: int = Column(Integer, primary_key=True, autoincrement=True)
    first_name: str = Column(String, nullable=False)
    last_name: str = Column(String, nullable=False)



class Medication(Base):
    __tablename__ = "medication"
    code_id: str = Column(String,  primary_key=True)
    code_name: str = Column(String, nullable=False)
    code_iso_name: str | None = Column(String, nullable=True)
    strength_value: int | None = Column(SmallInteger, nullable=True)
    strenght_unit: float | None = Column(DOUBLE_PRECISION, nullable=True)
    form: str = Column(
        Enum(
            FormType,
            name="form",
            validate_strings=True,
            native_enum=True,
        ),
        nullable=False,
        default=FormType.TABLET.value,
        server_default=FormType.TABLET.value,
    )





class MedicationRequest(Base):
    __tablename__ = "medication_request"
    medication_request_id: str = Column(String,  primary_key=True)
    clinician_reg_id: int = Column(Integer, ForeignKey("clinician.registration_id"))
    patient_id: int = Column(Integer, ForeignKey("patient.patient_id"))
    medication_code_id: str  = Column(String, ForeignKey("medication.code_id"))
    reason_of_prescription: date | None = Column(TEXT, nullable=True)
    prescription_date: datetime = Column(DateTime, nullable=False)
    start_date: datetime = Column(DateTime, nullable=False)
    end_date: datetime | None  = Column(DateTime, nullable=True)
    frequency: int = Column(SmallInteger, nullable=False)
    status: str = Column(
        Enum(
            StatusType,
            name="status",
            validate_strings=True,
            native_enum=True,
        ),
        nullable=False,
        default=StatusType.ACTIVE.value,
        server_default=StatusType.ACTIVE.value,
    )

