from marshmallow import Schema, fields, validate, ValidationError, validates


class ShopCreateSchema(Schema):

    user_id = fields.Integer()
    shop_name = fields.String(required=True, validate=validate.Length(min=3, max=100))

    shop_address_city = fields.String()
    shop_phone = fields.String(validate=validate.Length(min=10, max=20))
    description = fields.String()

class ShopUpdateSchema(Schema):
    shop_name = fields.String(validate=validate.Length(min=3, max=100))
    shop_address_city = fields.String()
    shop_phone = fields.String(validate=validate.Length(min=10, max=20))
    description = fields.String()