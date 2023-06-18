from dataclasses import dataclass

@dataclass
class Address:
    street: str
    city: str
    country: str

class Phone:
    type: str
    phone_number: str


@dataclass
class Contact:
    first_name: str
    last_name: str
    phone: Phone
    address: Address
