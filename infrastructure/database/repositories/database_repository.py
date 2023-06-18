from dataclasses import asdict

from flask_restful import abort
from sqlalchemy.exc import SQLAlchemyError

from domain.services import ContactsRepository
from domain import Contact

from infrastructure.database.models import ContactModel, PhoneModel, AddressModel


class DatabaseContactsRepository(ContactsRepository):
    def __init__(self, db_instance):
        self._db_instance = db_instance

    def get_contacts(self):
        pass

    def search_contacts(self, query: str):
        pass

    def add_contact(self, contact_data: Contact):
        phone_model = PhoneModel(contact_data.phone)
        address_model = AddressModel(contact_data.address)
        contact_model = ContactModel(contact_data)
        try:
            self._db_instance.session.add(contact_model)
            self._db_instance.commit()
        except SQLAlchemyError as err:
            abort(500, message="an error occurred while inserting the contact data")
        return contact_data

    def edit_contact(self, contact_id: str, contact_data: dict):
        pass

    def delete_contact(self, contact_id: str):
        pass
