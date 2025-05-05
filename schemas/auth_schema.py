from marshmallow import Schema, fields, validate, validates, ValidationError
import re
from marshmallow_enum import EnumField
from model.userModel import GenderEnum

class RegisterSchema(Schema):
    name = fields.String(validate=validate.Length(min=3, max=100))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))
    
    phone = fields.String(validate=validate.Length(min=10, max=20))
    user_image = fields.String()
    user_imageId = fields.String()

    address_street = fields.String()
    address_city = fields.String()
    address_district = fields.String()
    address_subdistrict = fields.String()
    address_zipcode = fields.String(validate=validate.Length(max=10))
    address_country = fields.String(load_default="Indonesia")

    gender = EnumField(GenderEnum, by_value=True) 

    @validates("password")
    def validate_password(self, value):
        # Minimal 8 karakter, setidaknya 1 huruf besar, 1 angka
        if not re.match(r"^(?=.*[A-Z])(?=.*\d).{8,}$", value):
            raise ValidationError(
                "Password harus minimal 8 karakter dan mengandung minimal 1 huruf besar dan 1 angka"
            )

    @validates("phone")
    def validate_phone(self, value):
        if value and not re.match(r"^\+?[\d\s-]{10,}$", value):
            raise ValidationError("Format nomor telepon tidak valid")

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class AuthResponseSchema(Schema):
    access_token = fields.String()
    token_type = fields.String()
    user = fields.Dict() 

class UpdateUserSchema(Schema):
    name = fields.String(validate=validate.Length(min=3, max=100))
    email = fields.Email()

    phone = fields.String(validate=validate.Length(min=10, max=20))
    address_street = fields.String()
    address_city = fields.String()
    address_district = fields.String()
    address_subdistrict = fields.String()
    address_zipcode = fields.String(validate=validate.Length(max=10))
    address_country = fields.String()

    gender = EnumField(GenderEnum, by_value=True)

class UserSchemaResponse(Schema):
    user_id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)
    email = fields.String(dump_only=True)
    user_image = fields.String(dump_only=True)
    user_imageId = fields.String(dump_only=True)
    address_street = fields.String(dump_only=True)
    address_city = fields.String(dump_only=True)
    address_district = fields.String(dump_only=True)
    address_subdistrict = fields.String(dump_only=True)
    address_zipcode = fields.String(dump_only=True)
    address_country = fields.String(dump_only=True)
    phone = fields.String(dump_only=True)
    status = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    gender = fields.String(dump_only=True)

