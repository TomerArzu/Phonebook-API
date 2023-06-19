from flask_restful import Resource
from flask import request
from marshmallow import ValidationError

from domain.exceptions import PhonebookException
from logger_instance import logger

from application import ContactsHandler
from domain.entities import Contact, Address, Phone
from infrastructure.validators import PhoneSchema, AddressSchema, ContactSchema
from response_maker import create_error_response, create_success_response

phone_schema = PhoneSchema()
address_schema = AddressSchema()
contact_schema = ContactSchema()


class ContactsResource(Resource):
    def __init__(self, **kwargs):
        self._handler: ContactsHandler = kwargs['handler']

    def get(self):
        # with or without query params (search or get all)
        try:
            self._handler.get_contacts()
        except Exception as e:
            print(e)
        pass

    def post(self):
        requested_data = request.get_json()
        try:
            contact_result = contact_schema.load(requested_data)
            phone_result = phone_schema.load(requested_data['phone'])
            address_result = address_schema.load(requested_data['address'])
            new_contact, new_phone, new_address = self._handler.add_contact(
                Contact(
                    first_name=contact_result['first_name'],
                    last_name=contact_result['last_name'],
                    address=Address(**address_result),
                    phone=Phone(**phone_result)
                )
            )
            # TODO: try to arrange it so it will be one `dump` function for all entities
            created_contact = contact_schema.dump(new_contact)
            created_contact['phone'] = phone_schema.dump(new_phone)
            created_contact['address'] = address_schema.dump(new_address)
            return create_success_response(created_contact)
        except ValidationError as ve:
            return create_error_response(ve.messages, 400)
        except PhonebookException as pbe:
            return create_error_response(pbe.message, pbe.http_status_code)


class ContactResource(Resource):
    def __init__(self, **kwargs):
        # TODO: remove `ContactsHandler` hint
        self._handler: ContactsHandler = kwargs['handler']

    def put(self, contact_id):
        requested_data = request.get_json()
        try:
            result = contact_schema.load(requested_data)
            self._handler.edit_contact(contact_id, Contact(**result))
        except ValidationError as ve:
            return {'error': ve.messages}, 400

    def delete(self, contact_id):
        try:
            self._handler.delete_contact(contact_id)
        except Exception as e:
            print(e)
        pass
