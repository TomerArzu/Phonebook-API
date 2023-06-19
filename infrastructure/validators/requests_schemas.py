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
    address = fields.Nested(AddressSchema())
    phone = fields.Nested(PhoneSchema())


# class AddressSchema(PlainAddressSchema):
#     # contact_id = fields.Int(required=True, load_only=True)
#     contact = fields.Nested(PlainContactSchema(), dump_only=True)
#
#
# class PhoneSchema(PlainPhoneSchema):
#     # contact_id = fields.Int(required=True, load_only=True)
#     contact = fields.Nested(PlainContactSchema(), dump_only=True)
#
#
# class ContactSchema(PlainContactSchema):
#     phone = fields.List(fields.Nested(PlainPhoneSchema()))
#     address = fields.List(fields.Nested(PlainAddressSchema()))
