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
            contact = Contact(
                first_name=contact_result['first_name'],
                last_name=contact_result['last_name'],
                address=[Address(**address) for address in contact_result['address']],
                phone=[Phone(**phone) for phone in contact_result['phone']]
            )
            new_contact = self._handler.add_contact(contact)
            created_contact = contact_schema.dump(new_contact)
            response = create_success_response(created_contact)
        except ValidationError as ve:
            response = create_error_response(ve.messages, 400)
        except PhonebookException as pbe:
            response = create_error_response(pbe.message, pbe.http_status_code)
        return response


class ContactResource(Resource):
    def __init__(self, **kwargs):
        # TODO: remove `ContactsHandler` hint
        self._handler: ContactsHandler = kwargs['handler']

    def put(self, contact_id):
        requested_data = request.get_json()
        try:
            contact_result = contact_schema.load(requested_data)
            contact = Contact(
                first_name=contact_result['first_name'],
                last_name=contact_result['last_name'],
                address=[Address(**address) for address in contact_result['address']],
                phone=[Phone(**phone) for phone in contact_result['phone']]
            )
            response = contact_schema.dump(self._handler.edit_contact(contact_id, contact))
        except ValidationError as ve:
            response = create_error_response(ve.messages, 400)
        except PhonebookException as pbe:
            response = create_error_response(pbe.message, pbe.http_status_code)
        return response

    def delete(self, contact_id):
        try:
            self._handler.delete_contact(contact_id)
        except Exception as e:
            print(e)
        pass
