from marshmallow import Schema, fields


class PlainAddressSchema(Schema):
    id = fields.Str(dump_only=True)
    street = fields.Str(required=True)
    city = fields.Str(required=True)
    country = fields.Str(required=True)


class PlainPhoneSchema(Schema):
    id = fields.Str(dump_only=True)
    type = fields.Str(required=True)
    number = fields.Str(required=True)


class PlainContactSchema(Schema):
    id = fields.Str(dump_only=True)
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
