from marshmallow import Schema, fields, validate

class OrderItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    product_id = fields.Integer(dump_only=True)
    quantity = fields.Integer(dump_only=True)
    price = fields.Decimal(places=2, dump_only=True)
    subtotal = fields.Decimal(places=2, dump_only=True)
    product = fields.Nested('ProductSchema', dump_only=True)

class OrderSchema(Schema):
    id = fields.Integer(dump_only=True)
    total_amount = fields.Decimal(places=2, dump_only=True)
    status = fields.String(dump_only=True)
    shipping_address = fields.String(required=True)
    shipping_city = fields.String(required=True)
    shipping_postal_code = fields.String(required=True, validate=validate.Length(max=10))
    created_at = fields.DateTime(dump_only=True)
    items = fields.List(fields.Nested(OrderItemSchema), dump_only=True)

class OrderCreateSchema(Schema):
    shipping_address = fields.String(required=True)
    shipping_city = fields.String(required=True)
    shipping_postal_code = fields.String(required=True, validate=validate.Length(max=10))

class OrderResponseSchema(Schema):
    success = fields.Boolean()
    message = fields.String()
    data = fields.Nested(OrderSchema)

class OrderListResponseSchema(Schema):
    success = fields.Boolean()
    message = fields.String()
    data = fields.List(fields.Nested(OrderSchema))
    pagination = fields.Dict(keys=fields.String(), values=fields.Integer()) 