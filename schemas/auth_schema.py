from marshmallow import Schema, fields, validate, validates, ValidationError
import re

class RegisterSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=3, max=100))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))
    
    phone = fields.String(validate=validate.Length(min=10, max=20))
    user_image = fields.String()
    address_street = fields.String()
    address_city = fields.String()
    address_district = fields.String()
    address_subdistrict = fields.String()
    address_zipcode = fields.String(validate=validate.Length(max=10))
    address_country = fields.String(load_default="Indonesia")

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