from enum import Enum


class GenderType(str, Enum):
    MALE = "Male"
    FEMALE = "Female"


class FormType(str, Enum):
    POWDER: str = "Powder"
    TABLET: str = "Tablet"
    CAPSULE: str = "Capsule"
    SYRUP: str = "Syrup"

class StatusType(str, Enum):
    ACTIVE: str = "Active"
    ON_HOLD: str =  "On_Hold"
    CANCELLED: str = "Cancelled"
    COMPLETED: str = "Completed"
