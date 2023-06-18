from typing import List

from domain import Contact
from domain.services import ContactsRepository


class ContactsHandler:
    def __init__(self, database_contacts_repository: ContactsRepository):
        self._database_contacts_repository = database_contacts_repository

    def get_contacts(self) -> List[Contact]:
        pass

    def add_contact(self, contact_data: Contact):
        try:
            self._database_contacts_repository.add_contact(contact_data)
        except Exception as e:
            print(e)

    def edit_contact(self, contact_id: str, contact_data: Contact):
        pass

    def delete_contact(self, contact_id: str):
        pass
