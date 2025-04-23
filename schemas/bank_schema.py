from marshmallow import Schema, fields, validate


class BankSchema(Schema):
    account_id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    account_name = fields.String(required=True, validate=validate.Length(min=3, max=100))
    account_number = fields.Integer(required=True)
    code = fields.String(required=True)


class BankCreateSchema(Schema):
    account_name = fields.String(required=True, validate=validate.Length(min=3, max=100))
    account_number = fields.Integer(required=True)
    code = fields.String(required=True)

  
