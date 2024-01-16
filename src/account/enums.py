from enum import Enum, auto


class UserRole(Enum):
    SUPERUSER = auto()
    MANUFACTURER = auto()
    STAFF = auto()
    VISITOR = auto()


class Gender(Enum):
    MALE = auto()
    FEMALE = auto()
    OTHER = auto()
