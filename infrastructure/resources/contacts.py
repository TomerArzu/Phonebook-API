from flask_restful import Resource
from flask import request
from marshmallow import ValidationError

from logger_instance import logger

from application import ContactsHandler
from domain import Contact
from infrastructure.validators import PhoneSchema, AddressSchema, ContactSchema

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
            result = contact_schema.load(requested_data)
            self._handler.add_contact(Contact(**result))
        except ValidationError as ve:
            return {'error': ve.messages}, 400


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
