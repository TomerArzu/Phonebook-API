from typing import List

from domain.entities import Contact
from domain.services import ContactsRepository


class ContactsHandler:
    def __init__(self, database_contacts_repository: ContactsRepository):
        self._database_contacts_repository = database_contacts_repository

    def get_contacts(self) -> List[Contact]:
        pass

    def add_contact(self, contact_data: Contact):
        contact_model = self._database_contacts_repository.add_contact(contact_data)
        return contact_model

    def edit_contact(self, contact_id: str, contact_data: Contact):
        updated_contact = self._database_contacts_repository.edit_contact(contact_id, contact_data)
        return updated_contact

    def delete_contact(self, contact_id: str):
        self._database_contacts_repository.delete_contact(contact_id)
