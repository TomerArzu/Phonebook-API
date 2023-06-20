from flask_restful import Resource
from flask import request
from marshmallow import ValidationError

from domain.exceptions import PhonebookException
from infrastructure.validators.serializers import PagerSerializer
from utils.logger_instance import logger

from domain.entities import Contact, Address, Phone
from infrastructure.validators import PhoneSchema, AddressSchema, ContactSchema
from utils.response_maker import create_error_response, create_success_response

phone_schema = PhoneSchema()
address_schema = AddressSchema()
contact_schema = ContactSchema()


class ContactsResource(Resource):
    def __init__(self, **kwargs):
        self._contact_handler = kwargs['contact_handler']
        self._cached_requests_handler = kwargs['cached_requests_handler']

    def get(self):
        try:
            response = self._cached_requests_handler.get_cached_response(request.method, request.url)
            if not response:
                page_number = request.args.get('page')
                first_name = request.args.get('first_name')
                pager = self._contact_handler.get_contacts(int(page_number), first_name)
                serialized_pager_data = list(map(dict, contact_schema.dump(pager.get_page_items(), many=True)))
                serialized_pager = PagerSerializer.serialize_pager(pager, serialized_pager_data)
                response = create_success_response(serialized_pager)
                self._cached_requests_handler.set_cache_request(request.method, request.url, response)
        except TypeError as te:
            response = create_error_response("you must supply page number as numeric value", 400)
            logger.debug("error while getting contact - you must supply page number as numeric value")
        except PhonebookException as pbe:
            response = create_error_response(pbe.message, pbe.http_status_code)
            logger.debug(f"error while getting contact - {pbe.message}")
        return response

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
            new_contact = self._contact_handler.add_contact(contact)
            created_contact = contact_schema.dump(new_contact)
            logger.debug(f"new contact created! {created_contact}")
            response = create_success_response(created_contact)
            self._cached_requests_handler.invalidate_cache()
        except ValidationError as ve:
            response = create_error_response(ve.messages, 400)
            logger.debug(f"request body error - {ve.messages}")
        except PhonebookException as pbe:
            response = create_error_response(pbe.message, pbe.http_status_code)
            logger.debug(f"error while saving contact - {pbe.message}")
        return response


class ContactResource(Resource):
    def __init__(self, **kwargs):
        self._contact_handler = kwargs['contact_handler']
        self._cached_requests_handler = kwargs['cached_requests_handler']

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
            updated_contact = contact_schema.dump(self._contact_handler.edit_contact(contact_id, contact))
            response = create_success_response(updated_contact)
            self._cached_requests_handler.invalidate_cache()
        except ValidationError as ve:
            response = create_error_response(ve.messages, 400)
            logger.debug(f"request body error - {ve.messages}")
        except PhonebookException as pbe:
            response = create_error_response(pbe.message, pbe.http_status_code)
            logger.debug(f"error while updating contact - {pbe.message}")
        return response

    def delete(self, contact_id):
        try:
            self._contact_handler.delete_contact(contact_id)
            response = create_success_response("Contact deleted!")
            logger.debug(f"Contact deleted - {contact_id=}")
            self._cached_requests_handler.invalidate_cache()
        except PhonebookException as pbe:
            response = create_error_response(pbe.message, pbe.http_status_code)
            logger.debug(f"error while deleting contact - {pbe.message}")
        return response
