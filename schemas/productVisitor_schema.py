from marshmallow import schema, fields, validate
from datetime import datetime

class ProductVisitorSchema(schema.Schema):
    product_visitor_id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    product_id = fields.Integer()
    shop_id = fields.Integer()
    visit_date = fields.DateTime(dump_only=True)

    

class ProductVisitorQuerySchema(schema.Schema):
    product_id = fields.Integer(required=True)
    visit_date = fields.Date(format='%Y-%m-%d')
    sort = fields.String(validate=validate.OneOf(['newest', 'oldest']))
    page = fields.Integer(validate=validate.Range(min=1), load_default=1)
    per_page = fields.Integer(validate=validate.Range(min=1, max=100), load_default=20)

    address_country = fields.String()
    address_city = fields.String()
    gender = fields.String( validate=validate.OneOf(["male", "female"]))


class ShopVisitorQuerySchema(schema.Schema):
    shop_id = fields.Integer(required=True)
    visit_date = fields.Date(format='%Y-%m-%d')
    sort = fields.String(validate=validate.OneOf(['newest', 'oldest']))
    page = fields.Integer(validate=validate.Range(min=1), load_default=1)
    per_page = fields.Integer(validate=validate.Range(min=1, max=100), load_default=20)

    address_country = fields.String()
    address_city = fields.String()
    gender = fields.String( validate=validate.OneOf(["male", "female"]))
