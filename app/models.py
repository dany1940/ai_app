from sqlalchemy.orm import relationship
from sqlalchemy.typing import Date, D
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.sql.sqltypes import TEXT
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.sql.sqltypes import Integer
from sqlalchemy.sql.sqltypes import SmallInteger
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.sql.sqltypes import DateTime
from database import Base
from typing import date





class Patient(Base):
    __tablename__ = "patient"

    patient_id: int = Column(Integer, primary_key=True, autoincrement=True)
    first_name: str = Column(String, nullable=False)
    last_name: str = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender : str = Column(String, nullable=False)

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
    form: str = Column(String, nullable=False)




class MedicationRequest(Base):
    __tablename__ = "medication_request"
    clinician_reg_id: int = Column(Integer, ForeignKey("clinician.registration_id"))
    patient_id: int = Column(Integer, ForeignKey("patient.patient_id"))
    medication_code_id: str  = Column(String, ForeignKey("medication.code_id"))
    reason_of_prescription: date | None = Column(TEXT, nullable=True)
    prescription_date: datetime = Column(DateTime, nullable=False)
    start_date: datetime = Column(DateTime, nullable=False)
    end_date: datime | None  = Column(DateTime, nullable=True)
    frequency: int = Column(SmallInteger, nullable=False)
    status: str  = Column(String, nullable=False)



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


