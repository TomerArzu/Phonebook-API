from typing import List

from sqlalchemy.exc import SQLAlchemyError

from logger_instance import logger
from domain.repositories import ContactsPersistentRepository
from domain.entities import Contact, Phone, Address
from domain.exceptions import ContactNotFoundException, ContactCouldNotSaveException

from infrastructure.database.models import ContactModel, PhoneModel, AddressModel
from infrastructure.infra_utils.contacts_pager import ContactsPager


class DatabaseContactsPersistentRepository(ContactsPersistentRepository):
    def __init__(self, db_instance):
        self._db_instance = db_instance

    def get_contacts(self, page: int):
        pager = ContactsPager(ContactModel, page)
        return pager

    def search_contacts_by_first_name(self, page: int, first_name):
        pager = ContactsPager(ContactModel, page, first_name_filter=first_name)
        return pager

    def add_contact(self, contact_data: Contact):
        try:
            contact_model = self._save_or_update_contact_details(contact_data.first_name, contact_data.last_name)
            self._db_instance.session.flush()

            self._save_phone_details(contact_data.phone, contact_model.id)
            self._save_address_details(contact_data.address, contact_model.id)

            self._db_instance.session.commit()

        except SQLAlchemyError as err:
            self._db_instance.session.rollback()
            logger.error("an error occurred during saving the contact data - error message: %s".format(err))
            raise ContactCouldNotSaveException(
                message="an error occurred during saving the contact data - error message: %s".format(err),
            ) from err
        return contact_model

    def edit_contact(self, contact_id: str, updated_contact_data: Contact):
        try:
            exists_contact_model: ContactModel = ContactModel.query.get(contact_id)
            if not exists_contact_model:
                raise ContactNotFoundException(f"contact {contact_id} not found!")
            self._save_or_update_contact_details(
                first_name=updated_contact_data.first_name,
                last_name=updated_contact_data.last_name,
                contact_model=exists_contact_model,
            )
            self._put_contact_phones(exists_contact_model, updated_contact_data)
            self._put_contact_addresses(exists_contact_model, updated_contact_data)
            self._db_instance.session.commit()
        except SQLAlchemyError as err:
            self._db_instance.session.rollback()
            logger.error("an error occurred during saving the contact data - error message: %s".format(err))
            raise ContactCouldNotSaveException(
                message="an error occurred during saving the contact data - error message: %s".format(err),
            ) from err

        return exists_contact_model

    def delete_contact(self, contact_id: str):
        exists_contact_model: ContactModel = ContactModel.query.get(contact_id)
        if not exists_contact_model:
            raise ContactNotFoundException(f"contact {contact_id} not found!")
        self._db_instance.session.delete(exists_contact_model)
        self._db_instance.session.commit()

    def _save_or_update_contact_details(self, first_name, last_name,
                                        contact_model: ContactModel = None) -> ContactModel:
        new_or_updated_contact_model = contact_model
        if not new_or_updated_contact_model:
            new_or_updated_contact_model = ContactModel()
        new_or_updated_contact_model.first_name = first_name
        new_or_updated_contact_model.last_name = last_name
        self._db_instance.session.add(new_or_updated_contact_model)
        return new_or_updated_contact_model

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

    def _put_contact_phones(self, exists_contact_model, updated_contact_data):
        for phone in updated_contact_data.phone:
            updated_or_new_phone_model: PhoneModel = exists_contact_model.phone.filter_by(id=phone.id).first()
            if updated_or_new_phone_model:
                updated_or_new_phone_model.type = phone.type
                updated_or_new_phone_model.number = phone.number
            else:
                updated_or_new_phone_model = PhoneModel(
                    type=phone.type,
                    number=phone.number,
                    contact_id=exists_contact_model.id
                )
            self._db_instance.session.add(updated_or_new_phone_model)

    def _put_contact_addresses(self, exists_contact_model, updated_contact_data):
        for address in updated_contact_data.address:
            updated_or_new_address_model: AddressModel = exists_contact_model.address.filter_by(id=address.id).first()
            if updated_or_new_address_model:
                updated_or_new_address_model.street = address.street
                updated_or_new_address_model.city = address.city
                updated_or_new_address_model.country = address.country
            else:
                updated_or_new_address_model = AddressModel(
                    street=address.street,
                    city=address.city,
                    country=address.country,
                    contact_id=exists_contact_model.id
                )
            self._db_instance.session.add(updated_or_new_address_model)
