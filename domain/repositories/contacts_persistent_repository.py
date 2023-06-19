from abc import ABC, abstractmethod
from typing import TypeVar

from domain.entities import Contact

T = TypeVar("T")


class ContactsPersistentRepository(ABC):
    @abstractmethod
    def get_contacts(self, page: int):
        """Retrieve a list of contacts with pagination."""
        ...

    @abstractmethod
    def search_contacts_by_first_name(self, page: int, first_name):
        """Search for contact based on the query string with pagination."""
        ...

    @abstractmethod
    def add_contact(self, contact_data: Contact):
        """Add a new contact to the phonebook."""
        ...

    @abstractmethod
    def edit_contact(self, contact_id: str, contact_data: Contact):
        """Edit an existing contact in the phonebook."""
        ...

    @abstractmethod
    def delete_contact(self, contact_id: str):
        """Delete a contact from the phonebook."""
        pass
