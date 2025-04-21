from marshmallow import Schema, fields, validate

class ProductSchema(Schema):
    product_id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=3, max=200))
    description = fields.String()
    price = fields.Decimal(required=True, validate=validate.Range(min=0))
    stock = fields.Integer(validate=validate.Range(min=0))
    image_url = fields.URL(allow_none=True)
    category = fields.String(required=True, validate=validate.Length(min=2, max=100))
    status = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class ProductQuerySchema(Schema):
    product_id = fields.Integer()
    category = fields.String()
    min_price = fields.Decimal()
    max_price = fields.Decimal()
    sort = fields.String(validate=validate.OneOf(['price_asc', 'price_desc', 'newest', 'oldest']))
    page = fields.Integer(validate=validate.Range(min=1), load_default=1)
    per_page = fields.Integer(validate=validate.Range(min=1, max=100), load_default=20)

class ProductResponseSchema(Schema):
    status = fields.String()
    message = fields.String()
    data = fields.Nested(ProductSchema)
    
class ProductListResponseSchema(Schema):
    status = fields.String()
    message = fields.String()
    data = fields.List(fields.Nested(ProductSchema))
    pagination = fields.Dict(keys=fields.String(), values=fields.Integer()) 