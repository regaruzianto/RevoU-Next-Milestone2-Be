from marshmallow import fields, Schema, validate
from datetime import datetime

class VisitorSchema(Schema):
    visitor_id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    visit_date = fields.DateTime(dump_only=True)

    # nested
    user = fields.Nested('UserSchemaResponse', dump_only=True)
    

class UserVisitorQuerySchema(Schema):
    visit_date = fields.Date(format='%Y-%m-%d')
    address_country = fields.String()
    address_city = fields.String()
    gender = fields.String( validate=validate.OneOf(["male", "female"]))
    sort = fields.String(validate=validate.OneOf(['newest', 'oldest']))
    page = fields.Integer(validate=validate.Range(min=1), load_default=1)
    per_page = fields.Integer(validate=validate.Range(min=1, max=100), load_default=20)



