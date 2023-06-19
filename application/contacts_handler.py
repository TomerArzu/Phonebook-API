from typing import List

from domain.entities import Contact
from domain.exceptions import InvalidPageNumerException, RequestedPageNotFoundException
from domain.repositories import ContactsRepository


class ContactsHandler:
    def __init__(self, database_contacts_repository: ContactsRepository, contact_serializer, pager_serializer):
        self._database_contacts_repository = database_contacts_repository
        self.contact_serializer = contact_serializer
        self.pager_serializer = pager_serializer

    def get_contacts(self, page_number: int, first_name: str):
        if not page_number or page_number < 0:
            raise InvalidPageNumerException(f"page number is invalid, check your requested URL")
        if first_name:
            pager = self._database_contacts_repository.search_contacts_by_first_name(page_number, first_name)
        else:
            pager = self._database_contacts_repository.get_contacts(page_number)
        serialized_pager_data = list(map(dict, self.contact_serializer.dump(pager.get_page_items(), many=True)))
        serialized_pager = self.pager_serializer.serialize_pager(pager, serialized_pager_data)
        return serialized_pager

    def add_contact(self, contact_data: Contact):
        contact_model = self._database_contacts_repository.add_contact(contact_data)
        return contact_model

    def edit_contact(self, contact_id: str, contact_data: Contact):
        updated_contact = self._database_contacts_repository.edit_contact(contact_id, contact_data)
        return updated_contact

    def delete_contact(self, contact_id: str):
        self._database_contacts_repository.delete_contact(contact_id)
