from dataclasses import dataclass


@dataclass
class Address:
    street: str
    city: str
    country: str


@dataclass
class Phone:
    number: str
    type: str


@dataclass
class Contact:
    first_name: str
    last_name: str
    phone: Phone
    address: Address
