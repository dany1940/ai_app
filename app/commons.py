import enum

from sqlalchemy.ext.declarative import declarative_base


class GenderType(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

    PSI = "PSI"
    BAR = "BAR"
    KPA = "KPA"


class FormType(enum.Enum):
    POWDER = "POWDER"
    TABLET = "TABLET"
    CAPSULE = "CAPSULE"
    SYRUP = "SYRUP"


class StatusType(enum.Enum):
    ACTIVE = "ACTIVE"
    ON_HOLD = "ON_HOLD"
    CANCELLED = "CANCCELED"
    COMPLETED = "COMPLETED"


Base = declarative_base()
