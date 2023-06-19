from dataclasses import asdict

from flask_restful import abort
from sqlalchemy.exc import SQLAlchemyError

from logger_instance import logger
from domain.services import ContactsRepository
from domain.entities import Contact
from domain.exceptions import ContactNotFoundException, ContactCouldNotSaveException

from infrastructure.database.models import ContactModel, PhoneModel, AddressModel


class DatabaseContactsRepository(ContactsRepository):
    def __init__(self, db_instance):
        self._db_instance = db_instance

    def get_contacts(self):
        pass

    def search_contacts(self, query: str):
        pass

    def add_contact(self, contact_data: Contact):
        try:
            contact_model = self._save_contact_details(contact_data.first_name, contact_data.last_name)
            self._db_instance.session.flush()

            phone_model = self._save_phone_details(contact_data.phone.type, contact_data.phone.number, contact_model.id)
            address_model = self._save_address_details(contact_data.address.street, contact_data.address.city,
                                       contact_data.address.country, contact_model.id)

            self._db_instance.session.commit()
        except SQLAlchemyError as err:
            self._db_instance.session.rollback()
            logger.error("an error occurred during saving the contact data - error message: %s".format(err))
            raise ContactCouldNotSaveException(
                message="an error occurred during saving the contact data - error message: %s".format(err),
                source_error=err
            ) from err
        return contact_model, phone_model, address_model

    def edit_contact(self, contact_id: str, contact_data: dict):
        pass

    def delete_contact(self, contact_id: str):
        pass

    def _save_contact_details(self, first_name, last_name) -> ContactModel:
        contact_model = ContactModel(
            first_name=first_name,
            last_name=last_name,
        )
        self._db_instance.session.add(contact_model)
        return contact_model

    def _save_phone_details(self, type, number, contact_id):
        phone_model = PhoneModel(
            type=type,
            number=number,
            contact_id=contact_id
        )
        self._db_instance.session.add(phone_model)
        return phone_model

    def _save_address_details(self, street, city, country, contact_id):
        address_model = AddressModel(
            street=street,
            city=city,
            country=country,
            contact_id=contact_id
        )
        self._db_instance.session.add(address_model)
        return address_model