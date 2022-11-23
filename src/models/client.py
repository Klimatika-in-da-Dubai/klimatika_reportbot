from dataclasses import dataclass
from enum import Enum


@dataclass
class Client:
    class Type(str, Enum):
        UNKNOWN = ""
        OWNER = "OWNER"
        TENANT = "TENANT"

    name: str = ""
    phone: str = ""
    type: Type = Type.UNKNOWN
    address: str = ""
