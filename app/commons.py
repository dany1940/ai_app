import enum
from typing import Literal

from pydantic import UUID4, BaseModel
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


class TitleType(enum.Enum):
    MR = "MR"
    MRS = "MRS"
    MISS = "MISS"
    DR = "DR"
    PROF = "PROF"
    REV = "REV"


class BloodGroupType(enum.Enum):
    A_POSITIVE = "A_POSITIVE"
    A_NEGATIVE = "A_NEGATIVE"
    B_POSITIVE = "B_POSITIVE"
    B_NEGATIVE = "B_NEGATIVE"
    AB_POSITIVE = "AB_POSITIVE"
    AB_NEGATIVE = "AB_NEGATIVE"
    O_POSITIVE = "O_POSITIVE"
    O_NEGATIVE = "O_NEGATIVE"


class UserAuthorisation(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


Base = declarative_base()


class Token(BaseModel):
    token_type: str
    refresh_token: str
    expires_in: int
    access_token: str
    role: UserAuthorisation


class TokenData(BaseModel):
    sub: str
    exp: int
    iat: int
    nbf: int
    jti: UUID4
    type: Literal["access", "refresh"]
    fresh: bool
