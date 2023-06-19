from dataclasses import dataclass
from typing import List


@dataclass
class Address:
    street: str
    city: str
    country: str
    id: int = None


@dataclass
class Phone:
    number: str
    type: str
    id: int = None


@dataclass
class Contact:
    first_name: str
    last_name: str
    phone: List[Phone]
    address: List[Address]
    id: int = None
