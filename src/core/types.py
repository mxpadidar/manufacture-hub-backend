from datetime import timedelta
from enum import Enum, auto
from typing import NamedTuple


class Role(Enum):
    SUPERUSER = auto()
    MANUFACTURER = auto()
    STAFF = auto()
    VISITOR = auto()


class Gender(Enum):
    MALE = auto()
    FEMALE = auto()
    OTHER = auto()


class JwtConfigs(NamedTuple):
    secret: str
    algorithm: str
    expires_in: timedelta


class Token(NamedTuple):
    value: str
    type: str


class TokenPayload(NamedTuple):
    id: int
    role: int
