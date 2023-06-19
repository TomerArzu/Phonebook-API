from typing import List

from flask_restful import abort
from sqlalchemy.exc import SQLAlchemyError

from logger_instance import logger
from domain.services import ContactsRepository
from domain.entities import Contact, Phone, Address
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

            self._save_phone_details(contact_data.phone, contact_model.id)
            self._save_address_details(contact_data.address, contact_model.id)

            self._db_instance.session.commit()
        except SQLAlchemyError as err:
            self._db_instance.session.rollback()
            logger.error("an error occurred during saving the contact data - error message: %s".format(err))
            raise ContactCouldNotSaveException(
                message="an error occurred during saving the contact data - error message: %s".format(err),
                source_error=err
            ) from err
        return contact_model

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

    def _save_phone_details(self, phones: List[Phone], contact_id: str):
        phone_models = []
        for phone in phones:
            phone_model = PhoneModel(
                type=phone.type,
                number=phone.number,
                contact_id=contact_id
            )
            self._db_instance.session.add(phone_model)
            phone_models.append(phone)
        return phone_models

    def _save_address_details(self, addresses: List[Address], contact_id: str):
        address_models = []
        for address in addresses:
            address_model = AddressModel(
                street=address.street,
                city=address.city,
                country=address.country,
                contact_id=contact_id
            )
            self._db_instance.session.add(address_model)
            address_models.append(address_model)
        return address_models
