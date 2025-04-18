from marshmallow import Schema, fields, validate

class CartItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True, validate=validate.Range(min=1, max=10))
    created_at = fields.DateTime(dump_only=True)
    
    # Nested product info
    product = fields.Nested('ProductSchema', dump_only=True)

class CartItemCreateSchema(Schema):
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True, validate=validate.Range(min=1, max=10))

class CartItemUpdateSchema(Schema):
    quantity = fields.Integer(required=True, validate=validate.Range(min=1, max=10))

class CartResponseSchema(Schema):
    success = fields.Boolean()
    message = fields.String()
    data = fields.List(fields.Nested(CartItemSchema))
    total_items = fields.Integer()
    total_amount = fields.Decimal(places=2) 