from enum import Enum, auto


class UserRole(Enum):
    SUPERUSER = auto()
    OWNER = auto()
    STAFF = auto()
    MEMBER = auto()


class Gender(Enum):
    MALE = auto()
    FEMALE = auto()
    OTHER = auto()
