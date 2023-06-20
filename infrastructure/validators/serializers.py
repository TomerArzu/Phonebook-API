from marshmallow import Schema, fields

from infrastructure.pagers.contacts_pager import ContactsPager


class PlainAddressSchema(Schema):
    id = fields.Int(dump_only=False, required=False)
    street = fields.Str(required=True)
    city = fields.Str(required=True)
    country = fields.Str(required=True)


class PlainPhoneSchema(Schema):
    id = fields.Int(dump_only=False, required=False)
    type = fields.Str(required=True)
    number = fields.Str(required=True)


class PlainContactSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)


class AddressSchema(PlainAddressSchema):
    contact = fields.Nested(PlainContactSchema(), dump_only=True)


class PhoneSchema(PlainPhoneSchema):
    contact = fields.Nested(PlainContactSchema(), dump_only=True)


class ContactSchema(PlainContactSchema):
    class Meta:
        ordered = True

    phone = fields.List(fields.Nested(PlainPhoneSchema()))
    address = fields.List(fields.Nested(PlainAddressSchema()))


class PagerSerializer:
    @staticmethod
    def serialize_pager(pager: ContactsPager, page_results: list = None):
        return {
            "total_pages": pager.total_pages(),
            "total_items": pager.total_items(),
            "next": pager.next_page_index(),
            "previous": pager.previous_page_index(),
            "result": page_results,
        }
