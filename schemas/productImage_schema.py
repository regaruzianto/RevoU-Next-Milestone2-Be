from marshmallow import Schema, fields, validate

class ProductImageSchema(Schema):
    
    productImage_id = fields.Integer(dump_only=True)
    product_id = fields.Integer(required=True)
    image_url = fields.String(required=True)
    file_id = fields.String(required=True)

