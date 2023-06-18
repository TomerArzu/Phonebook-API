from marshmallow import Schema, fields


class AddressSchema(Schema):
    id = fields.Str(dump_only=True)
    street = fields.Str(required=True)
    city = fields.Str(required=True)
    country = fields.Str(required=True)


class PhoneSchema(Schema):
    id = fields.Str(dump_only=True)
    type = fields.Str(required=True)
    number = fields.Str(required=True)


class ContactSchema(Schema):
    id = fields.Str(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    address = fields.Nested(AddressSchema(), required=True)
    phone = fields.Nested(PhoneSchema(), required=True)
