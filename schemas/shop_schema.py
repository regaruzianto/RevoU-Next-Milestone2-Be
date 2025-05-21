from marshmallow import Schema, fields, validate, ValidationError, validates


class ShopSchema(Schema):
    shop_id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    shop_name = fields.String(required=True, validate=validate.Length(min=3, max=100))
    shop_address_city = fields.String()
    shop_phone = fields.String(validate=validate.Length(min=10, max=20))
    description = fields.String()
    shop_image = fields.String()
    shop_imageId = fields.String()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


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